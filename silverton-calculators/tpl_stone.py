# -*- coding: utf-8 -*-
"""Decorative Stone Calculator — specialist page template (@@BASE@@ tokens)."""

STONE = {
    "slug": "decorative-stone-calculator",
    "snippet_name": "decorative-stone-calculator.html",
    "preview_name": "decorative-stone-calculator.html",
    "page_name": "Decorative Stone Calculator",
    "h1": "Decorative Stone Calculator",
    "title": "Decorative Stone Calculator | Silverton Builders Merchants",
    "description": "Work out how much decorative stone or gravel you need by area and depth, with coverage in tonnes, bulk bags, mini bulk bags and small bags. Free calculator from Silverton.",
    "og_image": "https://www.silvertonbuildersmerchants.com/images/ocw/l000145-extra-large.jpg",
    "crumbs": [
        ("Home", "https://www.silvertonbuildersmerchants.com/"),
        ("Materials Calculator", "https://www.silvertonbuildersmerchants.com/page/materials-calculator"),
        ("Decorative Stone Calculator", None),
    ],
    "body": r"""
<div class="calculator-container">
	<div class="materials-disclaimer">

		<p>If you have any questions or think something is wrong, <a href="@@BASE@@/page/customer-services/contact-us">give us a call</a>:
			<br><a href="tel:01255446920"><strong>01255 446920</strong>.</a></p>

		<p><span style="color: #FF4C4C;">Note:</span> This calculator provides estimations so the actual measurements and material quantity should be verified.</p>
	</div>
</div>

<div class="calculator-container calc-guide">
	<p class="calc-back"><a href="@@BASE@@/page/materials-calculator">&larr; All materials calculators</a></p>
	<p>Our decorative stone calculator takes the guesswork out of ordering gravel, chippings and pebbles for your garden. Enter the width and length of the area you are covering to get the square meterage, or tick <strong>Calculate Volume</strong> and add a depth to see how many cubic metres, tonnes, bulk bags, mini bulk bags and small bags of decorative stone you will need. Whether you are freshening up borders, laying a new path or covering a driveway, order online from Silverton Builders Merchants for free local delivery across Essex, Suffolk, Norfolk and Cambridgeshire when you spend over &pound;20.</p>
</div>

<div class="calculator-container" style="text-align: center;"><img src="@@BASE@@/file/Dimensions.png" alt="Diagram showing how to measure the width, length and depth of an area in metres and millimetres" style="max-width: 100%;"></div>

<div class="calculator-container calc-guide">
	<h2>How to use the decorative stone calculator</h2>
	<ol>
		<li>Enter the <strong>width</strong> and <strong>length</strong> of the area you are covering, in metres.</li>
		<li>Press <strong>Calculate Area</strong> for the square meterage on its own.</li>
		<li>To work out how much stone to order, tick <strong>Calculate Volume</strong>, enter your <strong>depth</strong> in millimetres (30&ndash;50mm is typical for borders and paths) and press <strong>Calculate Volume</strong>.</li>
		<li>The result shows the <strong>volume in cubic metres</strong>, the approximate <strong>tonnage</strong>, and the number of <strong>bulk bags, mini bulk bags and small bags</strong> that make up that weight.</li>
		<li>For awkward shapes, split the area into rectangles, calculate each one and add the results together.</li>
	</ol>
</div>

<div class="calculator-container" style="text-align: center;">
	<div class="tabcontent active" id="areaVolumeCalculator" data-calculator-type="decorative_stone" style="display: block;">

		<h3>Area &amp; Volume Calculator</h3>
		<label for="widthAV">Width (m):</label>
		<input type="number" id="widthAV" name="widthAV" value="1" min="0">
		<br>
		<br>
		<label for="heightAV">Length (m):</label>
		<input type="number" id="heightAV" name="heightAV" value="1" min="0">
		<br>
		<br>
		<label>
			<input type="checkbox" id="volumeCheckboxAV" onclick="toggleVolumeInputAV()" value="on">&nbsp;Calculate Volume </label>
		<br>
		<br>
		<div class="volumeInput" id="volumeInputAV" style="display: none;">
			<label for="depthAV">Depth (mm):</label>
			<input type="number" id="depthAV" name="depthAV" value="1" min="0">
			<br>
			<br>
		</div>
		<button class="button-calculate" id="calculateAreaButton" onclick="handleAVButton()" type="button">Calculate Area</button>
		<br>
		<div class="grey-container" id="areaVolumeResult" style="font-size: 16px;">
			<br>
		</div>

		<div class="calc-shop">
			<h3>Shop decorative stone</h3>
			<div class="calc-cards">
				<a class="calc-card" href="@@BASE@@/category/aggregates/decorative-stone"><strong>Decorative stone &amp; gravel</strong><span>Chippings, cobbles and pebbles in granite, slate, marble and more.</span></a>
				<a class="calc-card" href="@@BASE@@/category/aggregates/bagged-aggregates"><strong>Bagged aggregates</strong><span>Bulk, mini bulk and small bags for every project size.</span></a>
				<a class="calc-card" href="@@BASE@@/category/landscaping-and-gardening/landscaping-fabric"><strong>Weed control membrane</strong><span>Separate stone from soil, improve drainage and reduce weeding.</span></a>
			</div>
			<p class="calc-products">Popular right now: <a href="@@BASE@@/product/category/l000145">Cotswold Buff Chippings 20mm &mdash; Bulk Bag</a> &middot; <a href="@@BASE@@/product/category/l000303">Polar White Chippings 20mm &mdash; Bulk Bag</a> &middot; <a href="@@BASE@@/product/category/l000229">Black Ice Chippings 20mm &mdash; Bulk Bag</a></p>
		</div>
	</div>
</div>

<div class="calculator-container calc-guide">
	<h2>What the decorative stone calculator assumes</h2>
	<div class="assumptions">
		<ul>
			<li>Volume is converted to tonnage at <strong>0.6 cubic metres per tonne</strong> (about 1.67 tonnes per m&sup3;), typical for decorative stone.</li>
			<li>A <strong>bulk bag holds roughly 0.85 tonnes (850kg)</strong>, a <strong>mini bulk bag 425kg</strong> and a <strong>small decorative bag 20kg</strong>.</li>
			<li>There are approximately <strong>42 small decorative bags in a bulk bag</strong>.</li>
			<li>Coverage is calculated at the <strong>depth you enter</strong>, laid loose on a level surface. 30&ndash;50mm suits most borders and paths; driveways usually need 50mm or more.</li>
			<li>No allowance is made for <strong>settlement or compaction</strong> &mdash; add 5&ndash;10% on driveways and busy areas.</li>
			<li>The calculator does not include <strong>weed membrane</strong>, which we recommend under decorative stone.</li>
		</ul>
	</div>

	<h2>Frequently asked questions</h2>
	<details class="faq-item">
		<summary>How deep should decorative stone be laid?</summary>
		<p>30&ndash;50mm is typical for borders and paths laid over a weed membrane. Driveways and heavily used areas usually need 50mm or more.</p>
	</details>
	<details class="faq-item">
		<summary>How much does a bulk bag of gravel cover?</summary>
		<p>A bulk bag holds roughly 0.85 tonnes &mdash; about half a cubic metre. At 50mm deep, that covers approximately 10 square metres.</p>
	</details>
	<details class="faq-item">
		<summary>How do I work out how much gravel I need?</summary>
		<p>Multiply the width by the length of the area to get square metres, then multiply by your depth in metres to get cubic metres. The calculator does this for you and converts the result into tonnes and bags.</p>
	</details>
	<details class="faq-item">
		<summary>Should I allow extra stone for settlement?</summary>
		<p>Yes &mdash; decorative stone settles after laying, so add 5&ndash;10% on driveways and busy areas, and rake the stone over occasionally to keep the coverage even.</p>
	</details>
	<details class="faq-item">
		<summary>Do I need a membrane under decorative stone?</summary>
		<p>We recommend a weed control membrane. It separates the stone from the soil, improves drainage and reduces weeding &mdash; see our <a href="@@BASE@@/category/landscaping-and-gardening/landscaping-fabric">landscaping fabric</a> range.</p>
	</details>
	<details class="faq-item">
		<summary>Do you deliver decorative stone?</summary>
		<p>Yes. Delivery is free locally across Essex, Suffolk, Norfolk and Cambridgeshire when you spend over &pound;20. Bulk bags are delivered by crane or tipper vehicle &mdash; call <a href="tel:01255446920">01255 446920</a> to check access.</p>
	</details>

	<h2>Other materials calculators</h2>
	<div class="calc-cards">
		<a class="calc-card" href="@@BASE@@/page/materials-calculator"><strong>All materials calculators</strong><span>The Silverton calculator hub, with every tool in one place.</span></a>
		<a class="calc-card" href="@@BASE@@/page/brick-and-block-calculator"><strong>Brick &amp; block calculator</strong><span>Bricks, blocks, sand and cement for single or double skin walls.</span></a>
		<a class="calc-card" href="@@BASE@@/page/paving-calculator"><strong>Paving calculator</strong><span>Slab quantities for patios and paths, including patio packs.</span></a>
	</div>
</div>

<script>
	/* ===== Decorative Stone (Area & Volume) Calculator — calculation rules
	   identical to the master calculator: volume in m³, tonnage at 0.6 m³ per
	   tonne, bulk bags at 0.85t, mini bulk bags at 0.425t and small decorative
	   bags at 20kg. New: input validation and GA4 tracking events. ===== */
	var CALC_TYPE = 'decorative_stone';

	function readNumber(id) {
		var value = parseFloat(document.getElementById(id).value);
		return (isFinite(value) && value > 0) ? value : null;
	}

	function showCalcError(message) {
		document.getElementById('areaVolumeResult').innerHTML =
			'<div class="grey-box" style="color:#a33;"><b>Please check your inputs.</b><br>' + message + '</div>';
	}

	function calculateAreaAV() {
		var width = readNumber('widthAV');
		var height = readNumber('heightAV');
		if (width === null || height === null) {
			var msg = 'Enter a width and length in metres, greater than zero.';
			showCalcError(msg);
			return { ok: false, message: msg };
		}
		var area = width * height;
		document.getElementById('areaVolumeResult').innerHTML = "<br>Area: <span><strong>" + area.toFixed(2) + " square meters</strong></span>";
		return { ok: true };
	}

	function calculateVolumeAV() {
		var width = readNumber('widthAV');
		var height = readNumber('heightAV');
		var depth = readNumber('depthAV');
		if (width === null || height === null) {
			var msg = 'Enter a width and length in metres, greater than zero.';
			showCalcError(msg);
			return { ok: false, message: msg };
		}
		if (depth === null) {
			var depthMsg = 'Enter a depth in millimetres, greater than zero.';
			showCalcError(depthMsg);
			return { ok: false, message: depthMsg };
		}

		var volume = width * height * (depth / 1000); // Calculate volume in cubic meters
		var totalWeightKg = volume / 0.6; // Convert volume from cubic meters to tonnes

		var bulkBags = Math.floor(totalWeightKg / 0.85); // Calculate the number of bulk bags
		var remainingWeightForMiniBags = totalWeightKg - bulkBags * 0.85; // Calculate remaining weight after bulk bags
		var miniBags = Math.floor(remainingWeightForMiniBags / 0.425); // Calculate the number of mini bulk bags
		var remainingWeightForSmallBags = (remainingWeightForMiniBags - miniBags * 0.425) * 1000; // Calculate remaining weight after mini bulk bags, converted back to kilograms
		var smallBags = Math.ceil(remainingWeightForSmallBags / 20); // Calculate the number of small bags

		// Build the result string for bag counts
		var bagCounts = [];

		if (bulkBags > 0) {
			bagCounts.push(bulkBags + ' x bulk bag' + (bulkBags > 1 ? 's' : ''));
		}

		if (miniBags > 0) {
			bagCounts.push(miniBags + ' x mini bulk bag' + (miniBags > 1 ? 's' : ''));
		}

		if (smallBags > 0) {
			bagCounts.push(smallBags + ' x small bag' + (smallBags > 1 ? 's' : ''));
		}

		// Combine bag counts into a single sentence
		var bagsResult = bagCounts.join(', ').replace(/, ([^,]*)$/, ' and $1');

		// Display the results
		var resultHtml = `
        <div class="result">Volume: <b>${volume.toFixed(2)} m³</b></div>
        <div class="result" style="margin-top: -10px;">Tonne: <b>${(volume / 0.6).toFixed(2)} T</b></div>
        <div style="text-align: center;">
            <div style="margin-bottom: 2px;"><b>For decorative stone coverage, you need a total of:</b></div>
            <div>${bagsResult}</div>
            <div style="font-size: 13px; margin-bottom: 10px; margin-top: 10px;">There are approx. 42 small decorative bags in a bulk bag</div>
                <div style="font-style: italic; margin-top: 10px;"><a href="@@BASE@@/category/aggregates/decorative-stone">Click here to browse Decorative Stone</a></div>
        </div>
    `;

		document.getElementById('areaVolumeResult').innerHTML = resultHtml;
		return { ok: true };
	}

	/* Matches the master: the checkbox reveals the depth field and relabels
	   the button, then refreshes the area result. */
	function toggleVolumeInputAV() {
		var volumeInput = document.getElementById("volumeInputAV");
		var calculateAreaButton = document.getElementById("calculateAreaButton");
		if (volumeInput.style.display === "none") {
			volumeInput.style.display = "block";
			calculateAreaButton.textContent = "Calculate Volume";
		} else {
			volumeInput.style.display = "none";
			calculateAreaButton.textContent = "Calculate Area";
		}
		recalculateArea();
	}

	function handleAVButton() {
		SilvertonCalc.start(CALC_TYPE);
		var volumeMode = document.getElementById('volumeCheckboxAV').checked;
		var result = volumeMode ? calculateVolumeAV() : calculateAreaAV();
		if (result.ok) {
			SilvertonCalc.complete(CALC_TYPE, volumeMode ? 'volume' : 'area');
		} else {
			SilvertonCalc.error(CALC_TYPE, result.message);
		}
	}

	/* Matches the master behaviour: typing refreshes the area result — press
	   the Calculate button to refresh a volume result. */
	function recalculateArea() {
		SilvertonCalc.start(CALC_TYPE);
		var result = calculateAreaAV();
		if (result.ok) {
			SilvertonCalc.complete(CALC_TYPE, 'area');
		} else {
			SilvertonCalc.error(CALC_TYPE, result.message);
		}
	}

	/* Wiring */
	var avInputs = document.querySelectorAll('#areaVolumeCalculator input[type="number"]');
	for (var i = 0; i < avInputs.length; i++) {
		avInputs[i].addEventListener('input', recalculateArea);
	}
</script>
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "FAQPage",
	"mainEntity": [
		{
			"@type": "Question",
			"name": "How deep should decorative stone be laid?",
			"acceptedAnswer": { "@type": "Answer", "text": "30–50mm is typical for borders and paths laid over a weed membrane. Driveways and heavily used areas usually need 50mm or more." }
		},
		{
			"@type": "Question",
			"name": "How much does a bulk bag of gravel cover?",
			"acceptedAnswer": { "@type": "Answer", "text": "A bulk bag holds roughly 0.85 tonnes — about half a cubic metre. At 50mm deep, that covers approximately 10 square metres." }
		},
		{
			"@type": "Question",
			"name": "How do I work out how much gravel I need?",
			"acceptedAnswer": { "@type": "Answer", "text": "Multiply the width by the length of the area to get square metres, then multiply by your depth in metres to get cubic metres. The calculator does this for you and converts the result into tonnes and bags." }
		},
		{
			"@type": "Question",
			"name": "Should I allow extra stone for settlement?",
			"acceptedAnswer": { "@type": "Answer", "text": "Yes — decorative stone settles after laying, so add 5–10% on driveways and busy areas, and rake the stone over occasionally to keep the coverage even." }
		},
		{
			"@type": "Question",
			"name": "Do I need a membrane under decorative stone?",
			"acceptedAnswer": { "@type": "Answer", "text": "We recommend a weed control membrane. It separates the stone from the soil, improves drainage and reduces weeding." }
		},
		{
			"@type": "Question",
			"name": "Do you deliver decorative stone?",
			"acceptedAnswer": { "@type": "Answer", "text": "Yes. Delivery is free locally across Essex, Suffolk, Norfolk and Cambridgeshire when you spend over £20. Bulk bags are delivered by crane or tipper vehicle — call 01255 446920 to check access." }
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
		{ "@type": "ListItem", "position": 3, "name": "Decorative Stone Calculator" }
	]
}
</script>
<script type="application/ld+json">
{
	"@context": "https://schema.org",
	"@type": "WebApplication",
	"name": "Decorative Stone Calculator",
	"url": "@@BASE@@/page/decorative-stone-calculator",
	"applicationCategory": "UtilityApplication",
	"operatingSystem": "Any",
	"browserRequirements": "Requires JavaScript",
	"offers": { "@type": "Offer", "price": "0", "priceCurrency": "GBP" },
	"publisher": { "@type": "Organization", "name": "Silverton Builders Merchants", "url": "@@BASE@@/" }
}
</script>
""",
}
