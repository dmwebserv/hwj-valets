/*
 * QA harness for the Silverton calculator pages.
 *
 * What it does
 *  - Parses each delivered file (cms-snippets/ AND preview/) into a stub DOM
 *    (ids, classes, values, checked state, inline styles, tabcontent
 *    ownership) and evaluates the file's real <script> blocks in a Node vm.
 *  - Runs the same representative inputs through the ORIGINAL master code
 *    (master-original.js) and asserts the new pages render byte-identical
 *    results (whitespace and absolute-URL prefixes aside).
 *  - Asserts the exact expected numbers for representative inputs.
 *  - Asserts the GA4 dataLayer event sequences: calculator_start,
 *    calculator_complete, calculator_error, product_or_category_click —
 *    separately per calculator type, including on the hub.
 *  - Asserts no events fire on initial page load (no interaction yet).
 *
 * Usage:  node qa/harness.js   (from the silverton-calculators directory)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.resolve(__dirname, '..');
const LIVE = 'https://www.silvertonbuildersmerchants.com';

let passed = 0;
let failed = 0;
const failures = [];

function check(name, cond, detail) {
	if (cond) {
		passed++;
		console.log('  ok  ' + name);
	} else {
		failed++;
		failures.push(name + (detail ? '\n      ' + detail : ''));
		console.log('  FAIL ' + name + (detail ? '\n      ' + detail : ''));
	}
}

/* ------------------------------------------------------------------ */
/* Stub DOM                                                            */
/* ------------------------------------------------------------------ */

function makeEl(id) {
	const classes = new Set();
	const listeners = {};
	const el = {
		id,
		value: '',
		checked: false,
		innerHTML: '',
		textContent: '',
		href: '',
		style: {},
		dataset: {},
		_isTabcontent: false,
		_ownerEl: null,
		_isNumberInput: false,
		classList: {
			contains: (c) => classes.has(c),
			add: (c) => classes.add(c),
			remove: (c) => classes.delete(c),
		},
		addEventListener: (type, fn) => {
			(listeners[type] = listeners[type] || []).push(fn);
		},
		dispatch: (type) => {
			(listeners[type] || []).forEach((fn) => fn({ target: el }));
		},
		closest: (sel) => {
			if (/tabcontent|data-calculator-type/.test(sel)) { return el._ownerEl || null; }
			return null;
		},
		click: () => {},
	};
	el._classes = classes;
	el._listeners = listeners;
	el._snapshot = null;
	return el;
}

function seed(el, attrs) {
	const value = attrs.match(/\bvalue="([^"]*)"/);
	const cls = attrs.match(/\bclass="([^"]*)"/);
	const style = attrs.match(/\bstyle="([^"]*)"/);
	const calcType = attrs.match(/\bdata-calculator-type="([^"]*)"/);
	if (value) { el.value = value[1]; }
	if (cls) { cls[1].split(/\s+/).forEach((c) => c && el._classes.add(c)); }
	if (style) {
		style[1].split(';').forEach((pair) => {
			const idx = pair.indexOf(':');
			if (idx > -1) { el.style[pair.slice(0, idx).trim()] = pair.slice(idx + 1).trim(); }
		});
	}
	if (/\bchecked\b/.test(attrs)) { el.checked = true; }
	if (calcType) { el.dataset.calculatorType = calcType[1]; }
}

function snapshot(els) {
	for (const el of Object.values(els)) {
		el._snapshot = {
			value: el.value, checked: el.checked, innerHTML: el.innerHTML,
			style: { ...el.style }, classes: [...el._classes],
		};
	}
}

function restore(els) {
	for (const el of Object.values(els)) {
		const s = el._snapshot;
		if (!s) { continue; }
		el.value = s.value; el.checked = s.checked; el.innerHTML = s.innerHTML;
		el.style = { ...s.style };
		el._classes.clear();
		s.classes.forEach((c) => el._classes.add(c));
	}
}

/* Parse ids/classes/values/checked/styles/tabcontent ownership out of the
 * page markup. <script>, <style> and comment bodies are ignored. */
function parseDom(html) {
	const els = {};
	const cleaned = html
		.replace(/<!--[\s\S]*?-->/g, '')
		.replace(/<script\b[\s\S]*?<\/script>/g, '')
		.replace(/<style\b[\s\S]*?<\/style>/g, '');

	const stack = []; // open <div> elements: {id, el}
	const tagRe = /<(\/)?([a-zA-Z]+)((?:[^>"']|"[^"]*"|'[^']*')*)>/g;
	let m;
	while ((m = tagRe.exec(cleaned))) {
		const closing = !!m[1];
		const tag = m[2].toLowerCase();
		const attrs = m[3] || '';
		if (tag === 'div') {
			if (closing) { stack.pop(); continue; }
			const idM = attrs.match(/\bid="([^"]+)"/);
			const el = idM ? (els[idM[1]] = els[idM[1]] || makeEl(idM[1])) : null;
			if (el) { seed(el, attrs); }
			if (el && /(^|\s)tabcontent(\s|$)/.test(el._classes.size ? [...el._classes].join(' ') : '')) {
				el._isTabcontent = true;
			}
			stack.push({ id: idM ? idM[1] : null, el });
			continue;
		}
		if (closing || !attrs) { continue; }
		const idM = attrs.match(/\bid="([^"]+)"/);
		if (!idM || els[idM[1]]) { continue; }
		const el = makeEl(idM[1]);
		seed(el, attrs);
		if (tag === 'input' && /\btype="number"/.test(attrs)) { el._isNumberInput = true; }
		if (tag === 'select') {
			// Browsers default a <select> to its first <option>.
			const closeIdx = cleaned.indexOf('</select>', m.index);
			const optM = cleaned.slice(m.index, closeIdx === -1 ? undefined : closeIdx).match(/<option[^>]*\bvalue="([^"]*)"/);
			if (optM) { el.value = optM[1]; }
		}
		for (let i = stack.length - 1; i >= 0; i--) {
			if (stack[i].el && stack[i].el._isTabcontent) { el._ownerEl = stack[i].el; break; }
		}
		els[idM[1]] = el;
	}
	return els;
}

function extractScripts(html) {
	const scripts = [];
	const re = /<script>([\s\S]*?)<\/script>/g;
	let m;
	while ((m = re.exec(html))) { scripts.push(m[1]); }
	return scripts;
}

/* Build a vm context that behaves like a browser page for our purposes. */
function loadPage(file) {
	const html = fs.readFileSync(file, 'utf8');
	const els = parseDom(html);
	const docListeners = {};
	const documentStub = {
		getElementById: (id) => {
			if (!els[id]) { throw new Error('missing element #' + id); }
			return els[id];
		},
		querySelectorAll: (sel) => {
			if (!/input\[type="number"\]/.test(sel)) { return []; }
			const idScope = sel.match(/^#([\w-]+)\s/);
			return Object.values(els).filter((e) => e._isNumberInput &&
				(!idScope || (e._ownerEl && e._ownerEl.id === idScope[1])));
		},
		querySelector: () => ({ click() {} }),
		getElementsByClassName: (cls) =>
			Object.values(els).filter((e) => e._classes.has(cls)),
		addEventListener: (type, fn) => { docListeners[type] = fn; },
	};
	const win = { location: { href: LIVE + '/page/test' }, dataLayer: [] };
	const ctx = vm.createContext({
		document: documentStub,
		window: win,
		URL,
		console,
	});
	for (const code of extractScripts(html)) {
		vm.runInContext(code, ctx, { filename: file + ' <script>' });
	}
	// Browser shim: on a real page window properties are globals.
	vm.runInContext('if (typeof SilvertonCalc === "undefined" && window.SilvertonCalc) { SilvertonCalc = window.SilvertonCalc; }', ctx);
	snapshot(els);
	return { file, els, ctx, win, docListeners };
}

function resetTracking(page) {
	page.win.SilvertonCalc.started = {};
	page.win.dataLayer.length = 0;
}

function run(page, code) { return vm.runInContext(code, page.ctx); }

/* ------------------------------------------------------------------ */
/* Reference implementation (original master code)                     */
/* ------------------------------------------------------------------ */

const original = (() => {
	// The hub snippet reproduces the original tool markup 1:1, so its parsed
	// DOM gives the original code a faithful starting state.
	const html = fs.readFileSync(path.join(ROOT, 'cms-snippets/materials-calculator-hub.html'), 'utf8');
	const els = parseDom(html);
	const documentStub = {
		getElementById: (id) => {
			if (!els[id]) { throw new Error('missing element #' + id); }
			return els[id];
		},
		querySelectorAll: () => [],
		querySelector: () => ({ click() {} }),
		getElementsByClassName: () => [],
		addEventListener: () => {},
	};
	const ctx = vm.createContext({ document: documentStub, console });
	vm.runInContext(fs.readFileSync(path.join(__dirname, 'master-original.js'), 'utf8'), ctx);
	snapshot(els);
	return { els, ctx };
})();

function runOriginal(code) { return vm.runInContext(code, original.ctx); }

const norm = (html) => html.replace(new RegExp(LIVE, 'g'), '').replace(/\s+/g, ' ').trim();

/* ------------------------------------------------------------------ */
/* Test helpers                                                        */
/* ------------------------------------------------------------------ */

function setInputs(target, values) {
	for (const [id, v] of Object.entries(values)) {
		if (typeof v === 'boolean') { target.els[id].checked = v; }
		else { target.els[id].value = v; }
	}
}

function setSkin(target, skin) {
	target.els.singleSkinLabel._classes.delete('active');
	target.els.doubleSkinLabel._classes.delete('active');
	target.els[(skin === 'double' ? 'double' : 'single') + 'SkinLabel']._classes.add('active');
}

/* Compare a new page against the original master for the same inputs. */
function compareToOriginal(label, page, { inputs, skin, origFn, newFn, resultId, expect }) {
	restore(original.els);
	restore(page.els);
	if (skin) { setSkin(original, skin); setSkin(page, skin); }
	setInputs(original, inputs || {});
	setInputs(page, inputs || {});
	resetTracking(page);

	runOriginal(origFn + '()');
	const origHtml = original.els[resultId].innerHTML;

	run(page, newFn + '()');
	const newHtml = page.els[resultId].innerHTML;

	check(label + ' — result matches original master', norm(origHtml) === norm(newHtml),
		'original: ' + norm(origHtml).slice(0, 200) + '\n      new     : ' + norm(newHtml).slice(0, 200));

	for (const fragment of expect || []) {
		check(label + ' — contains "' + fragment + '"', norm(newHtml).indexOf(norm(fragment)) !== -1);
	}
}

function expectEvents(label, page, expected) {
	const events = page.win.dataLayer.map((e) =>
		e.event + (e.calculator_type ? ':' + e.calculator_type : '') +
		(e.calculator_mode ? '(' + e.calculator_mode + ')' : ''));
	const want = expected.map((e) =>
		e.event + (e.calculator_type ? ':' + e.calculator_type : '') +
		(e.calculator_mode ? '(' + e.calculator_mode + ')' : ''));
	check(label, JSON.stringify(events) === JSON.stringify(want),
		'got : ' + JSON.stringify(events) + '\n      want: ' + JSON.stringify(want));
}

function clickLink(page, link) {
	page.docListeners.click({ target: link });
}

/* ------------------------------------------------------------------ */
/* Representative input sets (also documented in README.md)            */
/* ------------------------------------------------------------------ */

const brickCases = [
	{ label: 'brick 5x2m standard brick single skin', inputs: { length: '5', height: '2' }, skin: 'single',
		expect: ['>600<', '1 mini bag(s) 7 small plastic bag(s)', '>100<', '4 bag(s)'] },
	{ label: 'block 5x2m standard block single skin', inputs: { length: '5', height: '2', brickSize: 'block' }, skin: 'single',
		expect: ['>100<', '>200<', '8 small plastic bag(s)', '>40<', '2 bag(s)'] },
	{ label: 'brick 5x2m custom 215x65 single skin', inputs: { length: '5', height: '2', brickSize: 'custom', brickWidth: '215', brickHeight: '65' }, skin: 'single',
		expect: ['>716<', '1 mini bag(s) 12 small plastic bag(s)', '>120<', '5 bag(s)'] },
	{ label: 'brick 5x2m standard brick double skin', inputs: { length: '5', height: '2' }, skin: 'double',
		expect: ['>1200<', '1 bulk bag(s) 14 small plastic bag(s)', '>200<', '8 bag(s)'] },
];

const stoneCases = [
	{ label: 'stone area 4x5m', inputs: { widthAV: '4', heightAV: '5' },
		expect: ['20.00 square meters'] },
];

const stoneVolumeCases = [
	{ label: 'stone volume 4x5m at 50mm', inputs: { widthAV: '4', heightAV: '5', depthAV: '50' },
		expect: ['Volume: <b>1.00 m³</b>', 'Tonne: <b>1.67 T</b>', '1 x bulk bag, 1 x mini bulk bag and 20 x small bags', 'There are approx. 42 small decorative bags in a bulk bag'] },
];

const pavingCases = [
	{ label: 'paving 4x5m 600x600 slabs', inputs: { pavingWidth: '4', pavingLength: '5', slabWidth: '600', slabHeight: '600' }, packs: false,
		expect: ['Area: <b>20.00 m²</b>', '56 slabs needed.'] },
	{ label: 'paving 4x5m patio packs', inputs: { pavingWidth: '4', pavingLength: '5' }, packs: true,
		expect: ['Area: <b>20.00 m²</b>', 'Approx 18 of each size required.', '1 of each slab equating to 1.17m²'] },
];

/* ------------------------------------------------------------------ */
/* Run the suite                                                       */
/* ------------------------------------------------------------------ */

const snippet = (f) => path.join(ROOT, 'cms-snippets', f);
const preview = (f) => path.join(ROOT, 'preview', f);

console.log('\n== Files under test ==');
const pages = {
	brickSnippet: loadPage(snippet('brick-and-block-calculator.html')),
	stoneSnippet: loadPage(snippet('decorative-stone-calculator.html')),
	pavingSnippet: loadPage(snippet('paving-calculator.html')),
	hubSnippet: loadPage(snippet('materials-calculator-hub.html')),
	brickPreview: loadPage(preview('brick-and-block-calculator.html')),
	stonePreview: loadPage(preview('decorative-stone-calculator.html')),
	pavingPreview: loadPage(preview('paving-calculator.html')),
	hubPreview: loadPage(preview('materials-calculator-hub.html')),
};

console.log('\n== No tracking events on initial page load ==');
for (const key of ['brickSnippet', 'stoneSnippet', 'pavingSnippet', 'hubSnippet', 'pavingPreview']) {
	check(key + ' — dataLayer empty after load', pages[key].win.dataLayer.length === 0,
		JSON.stringify(pages[key].win.dataLayer));
}

console.log('\n== Brick & Block: parity with original master + expected values ==');
for (const pageKey of ['brickSnippet', 'brickPreview', 'hubSnippet', 'hubPreview']) {
	const page = pages[pageKey];
	for (const c of brickCases) {
		compareToOriginal(pageKey + ' ' + c.label, page, {
			inputs: c.inputs, skin: c.skin,
			origFn: 'calculateBrickBlock', newFn: 'runBrickBlockCalc',
			resultId: 'brickBlockResult', expect: c.expect,
		});
	}
}

console.log('\n== Decorative stone: parity with original master + expected values ==');
for (const pageKey of ['stoneSnippet', 'stonePreview', 'hubSnippet', 'hubPreview']) {
	const page = pages[pageKey];
	for (const c of stoneCases) {
		compareToOriginal(pageKey + ' ' + c.label, page, {
			inputs: c.inputs,
			origFn: 'calculateAreaAV', newFn: 'handleAVButton',
			resultId: 'areaVolumeResult', expect: c.expect,
		});
	}
}

console.log('\n== Decorative stone volume (button path): parity + expected values ==');
for (const pageKey of ['stoneSnippet', 'stonePreview', 'hubSnippet', 'hubPreview']) {
	const page = pages[pageKey];
	for (const c of stoneVolumeCases) {
		compareToOriginal(pageKey + ' ' + c.label, page, {
			inputs: Object.assign({}, c.inputs, { volumeCheckboxAV: true }),
			origFn: 'calculateVolumeAV', newFn: 'handleAVButton',
			resultId: 'areaVolumeResult', expect: c.expect,
		});
	}
}

console.log('\n== Paving: parity with original master + expected values ==');
for (const pageKey of ['pavingSnippet', 'pavingPreview', 'hubSnippet', 'hubPreview']) {
	const page = pages[pageKey];
	for (const c of pavingCases) {
		compareToOriginal(pageKey + ' ' + c.label, page, {
			inputs: Object.assign({}, c.inputs, { usePatioPacksCheckbox: c.packs }),
			origFn: 'calculatePaving', newFn: 'runPavingCalc',
			resultId: 'pavingResult', expect: c.expect,
		});
	}
}

console.log('\n== Tracking events ==');

{
	const page = pages.brickSnippet;
	restore(page.els); resetTracking(page);
	setInputs(page, { length: '5', height: '2' });
	page.els.length.dispatch('input');
	expectEvents('brick: typing fires start + complete(single_skin)', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
	]);
	page.els.height.dispatch('input');
	expectEvents('brick: typing again fires complete only (start is once)', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
	]);
	setSkin(page, 'double');
	run(page, 'runBrickBlockCalc()');
	expectEvents('brick: double skin complete(double_skin)', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'double_skin' },
	]);
	setInputs(page, { length: '' });
	run(page, 'runBrickBlockCalc()');
	const last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('brick: invalid input fires calculator_error',
		last && last.event === 'calculator_error' && last.calculator_type === 'brick_and_block' && !!last.error_message,
		JSON.stringify(last));
	check('brick: error message shown in result box',
		page.els.brickBlockResult.innerHTML.indexOf('Please check your inputs') !== -1);
}

{ // stone page: area vs volume modes; volume requires the button
	const page = pages.stoneSnippet;
	restore(page.els); resetTracking(page);
	setInputs(page, { widthAV: '4', heightAV: '5', depthAV: '50', volumeCheckboxAV: true });
	page.els.widthAV.dispatch('input');
	expectEvents('stone: typing fires start + complete(area) — matches master quirk', page, [
		{ event: 'calculator_start', calculator_type: 'decorative_stone' },
		{ event: 'calculator_complete', calculator_type: 'decorative_stone', calculator_mode: 'area' },
	]);
	run(page, 'handleAVButton()');
	expectEvents('stone: Calculate button in volume mode fires complete(volume)', page, [
		{ event: 'calculator_start', calculator_type: 'decorative_stone' },
		{ event: 'calculator_complete', calculator_type: 'decorative_stone', calculator_mode: 'area' },
		{ event: 'calculator_complete', calculator_type: 'decorative_stone', calculator_mode: 'volume' },
	]);
	// toggle behaviour
	check('stone: volume field initially hidden', page.els.volumeInputAV.style.display === 'none');
	run(page, 'toggleVolumeInputAV()');
	check('stone: checkbox reveals depth field', page.els.volumeInputAV.style.display === 'block');
	check('stone: button relabels to Calculate Volume', page.els.calculateAreaButton.textContent === 'Calculate Volume');
	// invalid depth
	setInputs(page, { depthAV: '' });
	run(page, 'handleAVButton()');
	const last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('stone: invalid depth fires calculator_error',
		last && last.event === 'calculator_error' && last.calculator_type === 'decorative_stone',
		JSON.stringify(last));
}

{ // paving page: modes + error
	const page = pages.pavingSnippet;
	restore(page.els); resetTracking(page);
	setInputs(page, { pavingWidth: '4', pavingLength: '5' });
	page.els.pavingWidth.dispatch('input');
	expectEvents('paving: typing fires start + complete(custom_size)', page, [
		{ event: 'calculator_start', calculator_type: 'paving' },
		{ event: 'calculator_complete', calculator_type: 'paving', calculator_mode: 'custom_size' },
	]);
	page.els.usePatioPacksCheckbox.checked = true;
	page.els.usePatioPacksCheckbox.dispatch('change');
	expectEvents('paving: ticking Patio Packs fires complete(patio_packs)', page, [
		{ event: 'calculator_start', calculator_type: 'paving' },
		{ event: 'calculator_complete', calculator_type: 'paving', calculator_mode: 'custom_size' },
		{ event: 'calculator_complete', calculator_type: 'paving', calculator_mode: 'patio_packs' },
	]);
	check('paving: custom size fields hidden when Patio Packs ticked',
		page.els.customSizeInputs.style.display === 'none');
	setInputs(page, { pavingWidth: '' });
	run(page, 'runPavingCalc()');
	const last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('paving: invalid input fires calculator_error',
		last && last.event === 'calculator_error' && last.calculator_type === 'paving',
		JSON.stringify(last));
}

{ // hub: per-calculator attribution when every calculator is on one page
	const page = pages.hubSnippet;
	restore(page.els); resetTracking(page);
	setInputs(page, { length: '5', height: '2' });
	page.els.length.dispatch('input');
	expectEvents('hub: typing in Brick & Block fires brick events only', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
	]);
	setInputs(page, { widthAV: '4', heightAV: '5' });
	page.els.widthAV.dispatch('input');
	expectEvents('hub: typing in Decorative Stone fires stone events only', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
		{ event: 'calculator_start', calculator_type: 'decorative_stone' },
		{ event: 'calculator_complete', calculator_type: 'decorative_stone', calculator_mode: 'area' },
	]);
	setInputs(page, { pavingWidth: '4', pavingLength: '5' });
	page.els.pavingWidth.dispatch('input');
	expectEvents('hub: typing in Paving fires paving events only', page, [
		{ event: 'calculator_start', calculator_type: 'brick_and_block' },
		{ event: 'calculator_complete', calculator_type: 'brick_and_block', calculator_mode: 'single_skin' },
		{ event: 'calculator_start', calculator_type: 'decorative_stone' },
		{ event: 'calculator_complete', calculator_type: 'decorative_stone', calculator_mode: 'area' },
		{ event: 'calculator_start', calculator_type: 'paving' },
		{ event: 'calculator_complete', calculator_type: 'paving', calculator_mode: 'custom_size' },
	]);
}

console.log('\n== product_or_category_click (delegated link tracking) ==');

{
	const page = pages.brickSnippet;
	restore(page.els); resetTracking(page);
	const owner = page.els.brickBlockCalculator;
	const mkLink = (href, text) => {
		const link = {
			href, textContent: text,
			closest: (sel) => (/a\[href\]/.test(sel)
				? link
				: (/tabcontent|data-calculator-type/.test(sel) ? owner : null)),
		};
		return link;
	};
	clickLink(page, mkLink(LIVE + '/category/building-supplies/bricks', 'Click here to browse bricks or blocks'));
	let last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('brick page: category link click tracked',
		last && last.event === 'product_or_category_click' && last.calculator_type === 'brick_and_block' &&
		last.link_type === 'category' && last.link_url === LIVE + '/category/building-supplies/bricks',
		JSON.stringify(last));

	clickLink(page, mkLink(LIVE + '/product/category/b000105', 'Forterra Atherstone Stock Red Brick'));
	last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('brick page: product link click tracked as product',
		last && last.event === 'product_or_category_click' && last.link_type === 'product' &&
		last.link_text === 'Forterra Atherstone Stock Red Brick',
		JSON.stringify(last));

	const before = page.win.dataLayer.length;
	clickLink(page, mkLink(LIVE + '/page/materials-calculator', 'All materials calculators'));
	check('brick page: non-category/product links are not tracked',
		page.win.dataLayer.length === before);
}

{
	const page = pages.hubSnippet;
	restore(page.els); resetTracking(page);
	const pavingOwner = page.els.pavingCalculator;
	const link = {
		href: LIVE + '/category/landscaping-and-gardening/paving',
		textContent: 'Click here to browse Paving Slabs',
		closest: (sel) => (/a\[href\]/.test(sel) ? link : (/tabcontent/.test(sel) ? pavingOwner : null)),
	};
	clickLink(page, link);
	const last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('hub: in-result link attributed to the paving calculator',
		last && last.event === 'product_or_category_click' && last.calculator_type === 'paving' &&
		last.link_type === 'category',
		JSON.stringify(last));
}

{
	const page = pages.stoneSnippet;
	restore(page.els); resetTracking(page);
	const link = {
		href: LIVE + '/category/aggregates/decorative-stone',
		textContent: 'Click here to browse Decorative Stone',
		closest: (sel) => (/a\[href\]/.test(sel) ? link : (/tabcontent|data-calculator-type/.test(sel) ? page.els.areaVolumeCalculator : null)),
	};
	clickLink(page, link);
	const last = page.win.dataLayer[page.win.dataLayer.length - 1];
	check('stone page: result link tracked with decorative_stone type',
		last && last.event === 'product_or_category_click' && last.calculator_type === 'decorative_stone',
		JSON.stringify(last));
}

console.log('\n== Static markup checks ==');

function read(f) { return fs.readFileSync(f, 'utf8'); }

const pagesMeta = [
	['brick-and-block-calculator.html', 'brick_and_block', 'brick-and-block-calculator'],
	['decorative-stone-calculator.html', 'decorative_stone', 'decorative-stone-calculator'],
	['paving-calculator.html', 'paving', 'paving-calculator'],
];

for (const [file, type, slug] of pagesMeta) {
	const snip = read(snippet(file));
	const prev = read(preview(file));
	const snipNoComments = snip.replace(/<!--[\s\S]*?-->/g, '');

	check(file + ' snippet: only one calculator present',
		(snip.match(/class="tabcontent/g) || []).length === 1);
	check(file + ' snippet: single-card layout (one calc-page wrapper)',
		(snip.match(/class="calc-page"/g) || []).length === 1 && snip.indexOf('<!-- /calc-page -->') !== -1);
	const snipCssOnly = snip.replace(/<!--[\s\S]*?-->/g, '').replace(/\/\*[\s\S]*?\*\//g, '');
	check(file + ' snippet: CSS included (style block with calculator styles)',
		snip.indexOf('<style>') !== -1 && snip.indexOf('.calculator-container {') !== -1 &&
		snip.indexOf('.calc-card {') !== -1);
	check(file + ' snippet: no page-wide body override (site theme bg must show through)',
		!/\bbody\s*\{/.test(snipCssOnly));
	check(file + ' snippet: calculator fills the CMS column (no 700px cap)',
		snipCssOnly.indexOf('max-width: 700px') === -1);
	check(file + ' snippet: relative links for CMS', snip.indexOf('href="/category/') !== -1 && snip.indexOf(LIVE) === -1);
	check(file + ' snippet: FAQPage schema present', snip.indexOf('"@type": "FAQPage"') !== -1);
	check(file + ' snippet: breadcrumb schema present', snip.indexOf('"@type": "BreadcrumbList"') !== -1);
	check(file + ' snippet: no hardcoded H1 (CMS renders it; commented fallback is allowed)',
		/<h1/i.test(snipNoComments) === false);
	check(file + ' preview: self-referencing canonical',
		prev.indexOf('<link rel="canonical" href="' + LIVE + '/page/' + slug + '">') !== -1);
	check(file + ' preview: unique title + meta description',
		/<title>[^<]+<\/title>/.test(prev) && /<meta name="description" content="[^"]+">/.test(prev));
	check(file + ' preview: og tags present',
		prev.indexOf('property="og:title"') !== -1 && prev.indexOf('property="og:image"') !== -1);
	check(file + ' preview: ' + type + ' data attribute wired',
		prev.indexOf('data-calculator-type="' + type + '"') !== -1);
	check(file + ' preview: links back to hub',
		prev.indexOf('/page/materials-calculator') !== -1);
	check(file + ' preview: viewport meta for mobile QA',
		prev.indexOf('name="viewport" content="width=device-width, initial-scale=1"') !== -1);

	// Category and product links immediately after the result container
	const resultId = file.startsWith('brick') ? 'brickBlockResult' : (file.startsWith('decorative') ? 'areaVolumeResult' : 'pavingResult');
	const resultPos = prev.indexOf('id="' + resultId + '"');
	const shopPos = prev.indexOf('class="calc-shop"');
	check(file + ' preview: shop links block follows the result container', resultPos !== -1 && shopPos > resultPos && shopPos - resultPos < 3000);
	check(file + ' preview: product links included', prev.indexOf('/product/category/') !== -1);
}

const hubSnip = read(snippet('materials-calculator-hub.html'));
check('hub snippet: links to all three specialist pages',
	hubSnip.indexOf('/page/brick-and-block-calculator') !== -1 &&
	hubSnip.indexOf('/page/decorative-stone-calculator') !== -1 &&
	hubSnip.indexOf('/page/paving-calculator') !== -1);
check('hub snippet: does not duplicate specialist FAQ copy', hubSnip.indexOf('"@type": "FAQPage"') === -1);
check('hub snippet: all three tabs retained', (hubSnip.match(/class="tab /g) || []).length >= 2 && hubSnip.indexOf("openCalculator(event, 'pavingCalculator')") !== -1);
check('hub snippet: tile calculator retained (as on the live master)', hubSnip.indexOf('id="tileCalculator"') !== -1);

/* unique metadata across the three specialist previews */
const titles = pagesMeta.map(([f]) => (read(preview(f)).match(/<title>([^<]+)<\/title>/) || [])[1]);
const descs = pagesMeta.map(([f]) => (read(preview(f)).match(/name="description" content="([^"]+)"/) || [])[1]);
check('titles are unique', new Set(titles).size === 3, JSON.stringify(titles));
check('descriptions are unique', new Set(descs).size === 3, JSON.stringify(descs));

console.log('\n=============================================');
console.log(' ' + passed + ' passed, ' + failed + ' failed');
console.log('=============================================');
if (failed) {
	console.log('\nFailures:\n' + failures.join('\n'));
	process.exitCode = 1;
}
