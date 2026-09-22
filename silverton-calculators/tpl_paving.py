# -*- coding: utf-8 -*-
"""Paving Calculator — specialist page template (@@BASE@@ tokens)."""

PAVING = {
    "slug": "paving-calculator",
    "snippet_name": "paving-calculator.html",
    "preview_name": "paving-calculator.html",
    "page_name": "Paving Calculator",
    "h1": "Paving Calculator",
    "title": "Paving Calculator: How Many Slabs Do I Need? | Silverton",
    "description": "Calculate how many paving slabs you need for a patio or path, with custom slab sizes and patio pack coverage. Free paving calculator from Silverton Builders Merchants.",
    "og_image": "https://www.silvertonbuildersmerchants.com/images/ocw/p000001-extra-large.jpg",
    "crumbs": [
        ("Home", "https://www.silvertonbuildersmerchants.com/"),
        ("Materials Calculator", "https://www.silvertonbuildersmerchants.com/page/materials-calculator"),
        ("Paving Calculator", None),
    ],
    "body": r"""
<div class="calc-page">

<div class="calculator-container calc-guide">
	<p class="calc-back"><a href="@@BASE@@/page/materials-calculator">&larr; All materials calculators</a></p>
	<p>Planning a new patio or path? Our paving calculator works out how many slabs you will need from the width and length of the area. Choose your own slab size in millimetres &mdash; 600 x 600mm slabs are pre-filled &mdash; or tick <strong>I want to use Patio Packs</strong> if you are buying a mixed-size project pack, where one of each slab size covers approximately 1.17m&sup2;. Once you know your quantities, browse porcelain, natural stone and concrete paving from Silverton Builders Merchants, with free local delivery across Essex, Suffolk, Norfolk and Cambridgeshire when you spend over &pound;20.</p>
</div>

<div class="calculator-container" style="text-align: center;"><img src="@@BASE@@/file/Dimensions.png" alt="Diagram showing how to measure the width and length of a patio area in metres" style="max-width: 100%;"></div>

<div class="calculator-container" style="text-align: center;">
	<div class="tabcontent active" id="pavingCalculator" data-calculator-type="paving" style="display: block;">

		<h3>Paving Calculator</h3>
		<label for="pavingWidth">Width (m):</label>
		<input type="number" id="pavingWidth" name="pavingWidth" value="1" min="0">
		<br>
		<br>
		<label for="pavingLength">Length (m):</label>
		<input type="number" id="pavingLength" name="pavingLength" value="1" min="0">
		<br>
		<br>
		<div>
			<input type="checkbox" id="usePatioPacksCheckbox" value="on">
			<label for="usePatioPacksCheckbox">I want to use Patio Packs</label>
		</div>
		<br>
		<br>
		<div id="customSizeInputs">
			<label for="slabWidth">Slab Width (mm):</label>
			<input type="number" id="slabWidth" name="slabWidth" value="600" min="0">
			<br>
			<br>
			<label for="slabHeight">Slab Height (mm):</label>
			<input type="number" id="slabHeight" name="slabHeight" value="600" min="0">
		</div>
		<br>
		<br>
		<button class="button-calculate" onclick="runPavingCalc()" type="button">Calculate</button>
		<div class="grey-container" id="pavingResult">
			<div class="result">Area: <strong>1.00 m&sup2;</strong>
				<br>Slabs Needed: <strong>3 slabs needed.</strong>
				<div class="grey-box" style="margin-top: -10px; font-size: 0.8em;"><em>𝓲 &nbsp; Result does not include joint.</em></div></div>
			<div class="grey-box" style="margin-top: -10px; font-size: 15px;"><em><a href="@@BASE@@/category/landscaping-and-gardening/paving">Click here to browse <strong>Paving Slabs</strong></a></em></div></div>

		<div class="calc-shop">
			<h3>Shop paving</h3>
			<div class="calc-cards">
				<a class="calc-card" href="@@BASE@@/category/landscaping-and-gardening/paving"><strong>All paving</strong><span>Every slab we stock, including setts and accessories.</span></a>
				<a class="calc-card" href="@@BASE@@/category/landscaping-and-gardening/paving/porcelain"><strong>Porcelain paving</strong><span>Clean, contemporary, low-maintenance slabs.</span></a>
				<a class="calc-card" href="@@BASE@@/category/landscaping-and-gardening/paving/natural-stone"><strong>Natural stone paving</strong><span>Sandstone, limestone and slate with real texture.</span></a>
				<a class="calc-card" href="@@BASE@@/category/landscaping-and-gardening/paving/concrete"><strong>Concrete paving</strong><span>Affordable peak, textured and utility slabs.</span></a>
			</div>
			<p class="calc-products">Popular right now: <a href="@@BASE@@/product/category/p000001">Bradstone Sandstone Mixed Sizes &mdash; Fossil Buff</a> &middot; <a href="@@BASE@@/product/category/p900466">Sandstone Kandla Grey 900 x 600</a> &middot; <a href="@@BASE@@/product/category/p900624">Black Limestone 900 x 600mm</a> &mdash; plus <a href="@@BASE@@/category/landscaping-and-gardening/joint-compounds">joint compounds</a> and <a href="@@BASE@@/category/landscaping-and-gardening/paving/paving-accessories">paving accessories</a> to finish the job.</p>
		</div>

		<p class="calc-note">If you have any questions or think something is wrong, <a href="@@BASE@@/page/customer-services/contact-us">give us a call</a> on <a href="tel:01255446920"><strong>01255 446920</strong></a>. This calculator provides estimations so the actual measurements and material quantity should be verified.</p>
	</div>
</div>

<div class="calculator-container calc-guide">
	<h2>How to use the paving calculator</h2>
	<ol>
		<li>Enter the <strong>width</strong> and <strong>length</strong> of your patio or path, in metres.</li>
		<li>For single-size slabs, enter the <strong>slab width</strong> and <strong>height</strong> in millimetres (600 x 600mm is pre-filled).</li>
		<li>If you are buying a mixed-size <strong>patio pack</strong>, tick <strong>I want to use Patio Packs</strong> instead &mdash; the custom size fields are hidden.</li>
		<li>Press <strong>Calculate</strong> to see the area in square metres and the number of slabs needed.</li>
		<li>For L-shaped or irregular areas, split the space into rectangles, calculate each one separately and add the results together.</li>
	</ol>
</div>

<div class="calculator-container calc-guide">
	<h2>What the paving calculator assumes</h2>
	<div class="assumptions">
		<ul>
			<li>Slab counts divide the area by the face area of one slab, assuming slabs are laid <strong>edge to edge with no joint gap</strong>.</li>
			<li><strong>Patio pack mode</strong> assumes one of each slab size covers <strong>1.17m&sup2;</strong>. The mix of sizes in delivered packs may vary, but the total meterage is correct.</li>
			<li>The default slab size is <strong>600 x 600mm</strong> &mdash; change it to match your product.</li>
			<li>No <strong>wastage allowance</strong> is included. Add 5&ndash;10% for cuts and breakage, and more for diagonal layouts or irregular shapes.</li>
			<li>Areas are treated as simple <strong>rectangles</strong>; break irregular spaces into rectangles and calculate each separately.</li>
		</ul>
	</div>

	<h2>Frequently asked questions</h2>
	<details class="faq-item">
		<summary>How many 600 x 600mm slabs do I need per square metre?</summary>
		<p>A 600 x 600mm slab covers 0.36m&sup2;, so allow three slabs per square metre. The calculator rounds up to whole slabs for you.</p>
	</details>
	<details class="faq-item">
		<summary>What is a patio pack?</summary>
		<p>A patio or project pack contains a fixed mix of slab sizes. The calculator assumes one of each size covers about 1.17m&sup2;, so it tells you how many of each size you need.</p>
	</details>
	<details class="faq-item">
		<summary>How much extra paving should I allow for wastage?</summary>
		<p>Add 5&ndash;10% for cuts and breakage on straightforward layouts. Allow more for diagonal patterns, curves or irregularly shaped areas.</p>
	</details>
	<details class="faq-item">
		<summary>Does the calculator allow for joints between slabs?</summary>
		<p>No &mdash; the result assumes slabs laid edge to edge. Joint gaps mean you need slightly fewer slabs, so the calculator errs on the safe side.</p>
	</details>
	<details class="faq-item">
		<summary>What else do I need to lay a patio?</summary>
		<p>A compacted sub-base, a bedding mortar and jointing compound, plus a plate compactor and basic laying tools. See our <a href="@@BASE@@/category/landscaping-and-gardening/paving/paving-accessories">paving accessories</a> and <a href="@@BASE@@/category/landscaping-and-gardening/joint-compounds">joint compounds</a> ranges.</p>
	</details>
	<details class="faq-item">
		<summary>Porcelain or natural stone paving &mdash; which is better?</summary>
		<p>Porcelain is low maintenance with a clean, contemporary finish; natural stone has more texture and character. Our blog post, <a href="@@BASE@@/articles/blog/31/porcelain-vs-natural-stone-paving-which-is-right-for-you">Porcelain vs Natural Stone Paving</a>, compares the two in detail.</p>
	</details>

	<h2>Other materials calculators</h2>
	<div class="calc-cards">
		<a class="calc-card" href="@@BASE@@/page/materials-calculator"><strong>All materials calculators</strong><span>The Silverton calculator hub, with every tool in one place.</span></a>
		<a class="calc-card" href="@@BASE@@/page/brick-and-block-calculator"><strong>Brick &amp; block calculator</strong><span>Bricks, blocks, sand and cement for single or double skin walls.</span></a>
		<a class="calc-card" href="@@BASE@@/page/decorative-stone-calculator"><strong>Decorative stone calculator</strong><span>Gravel and stone coverage by area or depth, in every bag size.</span></a>
	</div>
</div>

</div>
<!-- /calc-page -->

<script>
	/* ===== Paving Calculator — calculation rules identical to the master
	   calculator: area in m², custom slabs divided by face area with no joint
	   allowance, patio packs at 1.17m² per size. New: input validation, the
	   custom size fields now hide when Patio Packs is ticked (the toggle
	   existed on the master page but was never wired up), and GA4 tracking. ===== */
	var CALC_TYPE = 'paving';

	function readNumber(id) {
		var value = parseFloat(document.getElementById(id).value);
		return (isFinite(value) && value > 0) ? value : null;
	}

	function showCalcError(message) {
		document.getElementById('pavingResult').innerHTML =
			'<div class="grey-box" style="color:#a33;"><b>Please check your inputs.</b><br>' + message + '</div>';
	}

	function toggleCustomSizeInputs() {
		var usePatioPacksCheckbox = document.getElementById("usePatioPacksCheckbox");
		var customSizeInputs = document.getElementById("customSizeInputs");

		if (usePatioPacksCheckbox.checked) {
			customSizeInputs.style.display = "none";
		} else {
			customSizeInputs.style.display = "block";
		}
	}

	function calculatePaving() {
		var width = readNumber('pavingWidth');
		var length = readNumber('pavingLength');
		if (width === null || length === null) {
			var msg = 'Enter a width and length in metres, greater than zero.';
			showCalcError(msg);
			return { ok: false, message: msg };
		}

		var usePatioPacksCheckbox = document.getElementById("usePatioPacksCheckbox");

		var totalArea = width * length;
		var slabs;
		var resultText;
		var mode = usePatioPacksCheckbox.checked ? 'patio_packs' : 'custom_size';

		if (usePatioPacksCheckbox.checked) {
			// Calculate total meters needed by dividing the area by 1.17
			slabs = totalArea / 1.17;
			resultText = `Approx ${Math.ceil(slabs)} of each size required.`;
		} else {
			// Calculate slabs based on custom size inputs
			var slabWidth = readNumber('slabWidth');
			var slabHeight = readNumber('slabHeight');
			if (slabWidth === null || slabHeight === null) {
				var sizeMsg = 'Enter a slab width and height in millimetres, greater than zero.';
				showCalcError(sizeMsg);
				return { ok: false, message: sizeMsg };
			}
			slabs = totalArea / ((slabWidth / 1000) * (slabHeight / 1000)); // convert mm to meters
			resultText = `${Math.ceil(slabs)} slabs needed.`;
		}

		var resultHtml = `<div class="result">Area: <b>${totalArea.toFixed(2)} m²</b><br>Slabs Needed: <b>${resultText}</b>`;
		var disclaimerHtml = '';
		if (usePatioPacksCheckbox.checked) {
			disclaimerHtml = `<div class="grey-box" style="font-size: 0.8em;"><i>𝓲  Slab calculation based on 1 of each slab equating to 1.17m² - ordered slab distribution of sizes may vary but meterage will be correct.</i></div>`;
		}
		disclaimerHtml += `<div class="grey-box" style="margin-top: -10px; font-size: 0.8em;"><i>𝓲   Result does not include joint.</i></div></div>`;
		disclaimerHtml += `<div class="grey-box" style="margin-top: -10px; font-size: 15px;"><i><a href="@@BASE@@/category/landscaping-and-gardening/paving">Click here to browse <b>Paving Slabs</b></a></i></div></div>`;
		document.getElementById('pavingResult').innerHTML = resultHtml + disclaimerHtml;
		return { ok: true, mode: mode };
	}

	function runPavingCalc() {
		SilvertonCalc.start(CALC_TYPE);
		var result = calculatePaving();
		if (result.ok) {
			SilvertonCalc.complete(CALC_TYPE, result.mode);
		} else {
			SilvertonCalc.error(CALC_TYPE, result.message);
		}
	}

	/* Wiring — mirrors the master: the initial result is calculated on load
	   (without tracking), inputs refresh as you type, and the Patio Packs
	   checkbox recalculates immediately. */
	var pavingInputs = document.querySelectorAll('#pavingCalculator input[type="number"]');
	for (var i = 0; i < pavingInputs.length; i++) {
		pavingInputs[i].addEventListener('input', runPavingCalc);
	}
	document.getElementById('usePatioPacksCheckbox').addEventListener('change', function () {
		toggleCustomSizeInputs();
		runPavingCalc();
	});

	// Initial calculation (no tracking event — nothing has been interacted with yet)
	calculatePaving();
</script>
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "FAQPage",
	"mainEntity": [
		{
			"@type": "Question",
			"name": "How many 600 x 600mm slabs do I need per square metre?",
			"acceptedAnswer": { "@type": "Answer", "text": "A 600 x 600mm slab covers 0.36m², so allow three slabs per square metre. The calculator rounds up to whole slabs for you." }
		},
		{
			"@type": "Question",
			"name": "What is a patio pack?",
			"acceptedAnswer": { "@type": "Answer", "text": "A patio or project pack contains a fixed mix of slab sizes. The calculator assumes one of each size covers about 1.17m², so it tells you how many of each size you need." }
		},
		{
			"@type": "Question",
			"name": "How much extra paving should I allow for wastage?",
			"acceptedAnswer": { "@type": "Answer", "text": "Add 5–10% for cuts and breakage on straightforward layouts. Allow more for diagonal patterns, curves or irregularly shaped areas." }
		},
		{
			"@type": "Question",
			"name": "Does the calculator allow for joints between slabs?",
			"acceptedAnswer": { "@type": "Answer", "text": "No — the result assumes slabs laid edge to edge. Joint gaps mean you need slightly fewer slabs, so the calculator errs on the safe side." }
		},
		{
			"@type": "Question",
			"name": "What else do I need to lay a patio?",
			"acceptedAnswer": { "@type": "Answer", "text": "A compacted sub-base, a bedding mortar and jointing compound, plus a plate compactor and basic laying tools." }
		},
		{
			"@type": "Question",
			"name": "Porcelain or natural stone paving — which is better?",
			"acceptedAnswer": { "@type": "Answer", "text": "Porcelain is low maintenance with a clean, contemporary finish; natural stone has more texture and character." }
		}
	]
}
</script>
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "BreadcrumbList",
	"itemListElement": [
		{ "@type": "ListItem", "position": 1, "name": "Home", "item": "@@BASE@@/" },
		{ "@type": "ListItem", "position": 2, "name": "Materials Calculator", "item": "@@BASE@@/page/materials-calculator" },
		{ "@type": "ListItem", "position": 3, "name": "Paving Calculator" }
	]
}
</script>
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "WebApplication",
	"name": "Paving Calculator",
	"url": "@@BASE@@/page/paving-calculator",
	"applicationCategory": "UtilityApplication",
	"operatingSystem": "Any",
	"browserRequirements": "Requires JavaScript",
	"offers": { "@type": "Offer", "price": "0", "priceCurrency": "GBP" },
	"publisher": { "@type": "Organization", "name": "Silverton Builders Merchants", "url": "@@BASE@@/" }
}
</script>
""",
}
