/*
 * ORIGINAL master calculator code, transcribed from the live page snippet.
 * Where the original defined a function twice, the later definition wins
 * (that is how it behaves on the live page), so only the effective versions
 * are included. Used by harness.js as the reference implementation — the new
 * specialist pages must produce byte-identical results (whitespace aside).
 */

function calculateAreaAV() {
	var width = parseFloat(document.getElementById('widthAV').value);
	var height = parseFloat(document.getElementById('heightAV').value);
	var area = width * height;
	document.getElementById('areaVolumeResult').innerHTML = "<br>Area: <span><strong>" + area.toFixed(2) + " square meters</strong></span>";
}

function calculateVolumeAV() {
	var width = parseFloat(document.getElementById('widthAV').value);
	var height = parseFloat(document.getElementById('heightAV').value);
	var depth = parseFloat(document.getElementById('depthAV').value);

	var volume = width * height * (depth / 1000); // Calculate volume in cubic meters
	var totalWeightKg = volume / 0.6; // Convert volume from cubic meters to tonnes

	var bulkBags = Math.floor(totalWeightKg / 0.85); // Calculate the number of bulk bags
	var remainingWeightForMiniBags = totalWeightKg - bulkBags * 0.85; // Calculate remaining weight after bulk bags
	var miniBags = Math.floor(remainingWeightForMiniBags / 0.425); // Calculate the number of mini bulk bags
	var remainingWeightForSmallBags = (remainingWeightForMiniBags - miniBags * 0.425) * 1000; // Calculate remaining weight after mini bulk bags, converted back to kilograms
	var smallBags = Math.ceil(remainingWeightForSmallBags / 20); // Calculate the number of small bags

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

	var bagsResult = bagCounts.join(', ').replace(/, ([^,]*)$/, ' and $1');

	var resultHtml = `
        <div class="result">Volume: <b>${volume.toFixed(2)} m³</b></div>
        <div class="result" style="margin-top: -10px;">Tonne: <b>${(volume / 0.6).toFixed(2)} T</b></div>
        <div style="text-align: center;">
            <div style="margin-bottom: 2px;"><b>For decorative stone coverage, you need a total of:</b></div>
            <div>${bagsResult}</div>
            <div style="font-size: 13px; margin-bottom: 10px; margin-top: 10px;">There are approx. 42 small decorative bags in a bulk bag</div>
                <div style="font-style: italic; margin-top: 10px;"><a href="/category/aggregates/decorative-stone">Click here to browse Decorative Stone</a></div>
        </div>
    `;

	document.getElementById('areaVolumeResult').innerHTML = resultHtml;
}

function calculateTiles() {
	var width = parseFloat(document.getElementById("tileWidth").value);
	var height = parseFloat(document.getElementById("tileHeight").value);
	var tileSize = document.getElementById("tileSize").value;
	var customTileWidth = parseFloat(document.getElementById("customTileWidth").value);
	var customTileHeight = parseFloat(document.getElementById("customTileHeight").value);

	if (tileSize === 'other') {
		var tileArea = customTileWidth * customTileHeight / 1000000; // Convert mm^2 to m^2
	} else {
		var dimensions = tileSize.split("x");
		var tileWidth = parseFloat(dimensions[0]);
		var tileHeight = parseFloat(dimensions[1]);
		var tileArea = tileWidth * tileHeight / 1000000; // Convert mm^2 to m^2
	}

	var totalTiles = (width * height) / tileArea;
	var resultHtml = `<div class="result">Tiles Needed: <b>${Math.ceil(totalTiles)}</b><br><div style="padding: 10px; max-width: 92%; overflow-x: auto;"><i style="font-size: 0.9em;">Please note that this value does not include allowance for overlapping due to the different needs per type of roof tile.</i></div></div>`;
	document.getElementById("tileResult").innerHTML = resultHtml;
}

function calculatePaving() {
	var width = parseFloat(document.getElementById("pavingWidth").value);
	var length = parseFloat(document.getElementById("pavingLength").value);
	var usePatioPacksCheckbox = document.getElementById("usePatioPacksCheckbox");

	var totalArea = width * length;
	var slabs;
	var resultText;

	if (usePatioPacksCheckbox.checked) {
		// Calculate total meters needed by dividing the area by 1.17
		slabs = totalArea / 1.17;
		resultText = `Approx ${Math.ceil(slabs)} of each size required.`;
	} else {
		// Calculate slabs based on custom size inputs
		var slabWidth = parseFloat(document.getElementById("slabWidth").value) / 1000; // convert mm to meters
		var slabHeight = parseFloat(document.getElementById("slabHeight").value) / 1000; // convert mm to meters
		slabs = totalArea / (slabWidth * slabHeight);
		resultText = `${Math.ceil(slabs)} slabs needed.`;
	}

	var resultHtml = `<div class="result">Area: <b>${totalArea.toFixed(2)} m²</b><br>Slabs Needed: <b>${resultText}</b>`;
	var disclaimerHtml = '';
	if (usePatioPacksCheckbox.checked) {
		disclaimerHtml = `<div class="grey-box" style="font-size: 0.8em;"><i>𝓲  Slab calculation based on 1 of each slab equating to 1.17m² - ordered slab distribution of sizes may vary but meterage will be correct.</i></div>`;
	}
	disclaimerHtml += `<div class="grey-box" style="margin-top: -10px; font-size: 0.8em;"><i>𝓲   Result does not include joint.</i></div></div>`;
	disclaimerHtml += `<div class="grey-box" style="margin-top: -10px; font-size: 15px;"><i><a href="/category/landscaping-and-gardening/paving">Click here to browse <b>Paving Slabs</b></a></i></div></div>`;
	document.getElementById("pavingResult").innerHTML = resultHtml + disclaimerHtml;
}

function toggleCustomSize() {
	var brickSize = document.getElementById("brickSize").value;
	var customSize = document.getElementById("customSize");
	if (brickSize === 'custom') {
		customSize.style.display = "block";
	} else {
		customSize.style.display = "none";
	}
}

function calculateBrickBlock() {
	var length = parseFloat(document.getElementById("length").value);
	var height = parseFloat(document.getElementById("height").value);
	var brickSize = document.getElementById("brickSize").value;
	var multiplier = 1;

	var doubleSkinLabel = document.getElementById("doubleSkinLabel");
	if (doubleSkinLabel.classList.contains('active')) {
		multiplier = 2;
	}

	var bricks, sand, cement;

	if (brickSize === 'house') {
		bricks = Math.ceil((length * height) * 60 * multiplier);
		sand = Math.ceil(bricks * 1);
		cement = Math.ceil(bricks / 6);
	} else if (brickSize === 'block') {
		bricks = Math.ceil((length * height) * 10 * multiplier);
		sand = Math.ceil((bricks / 10) * 20);
		cement = Math.ceil((bricks / 10) * 4);
	} else if (brickSize === 'custom') {
		var brickWidth = parseFloat(document.getElementById("brickWidth").value);
		var brickHeight = parseFloat(document.getElementById("brickHeight").value);
		bricks = Math.ceil((length * height) / ((brickWidth / 1000) * (brickHeight / 1000)) * multiplier);
		sand = Math.ceil(bricks * 1);
		cement = Math.ceil(bricks / 6);
	}

	var bulkBags = Math.floor(sand / 850); // Calculate number of bulk bags (850 kg)
	var miniBags = Math.floor((sand % 850) / 425); // Calculate number of mini bulk bags (425 kg)
	var smallBags = Math.ceil(((sand % 850) % 425) / 25); // Calculate number of small plastic bags (25 kg)

	var resultHtml = `
        <table style="width: 100%; margin: 0 auto; border-collapse: collapse;">
            <tr>
                <th style="border: 1px solid #ddd; padding: 8px;">Material</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Total Bags</th>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Bricks/Blocks</td>
                <td style="border: 1px solid #ddd; padding: 8px;"><b>${bricks}</b></td>
                <td style="border: 1px solid #ddd; padding: 8px;">-</td>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Sand (kg)</td>
                <td style="border: 1px solid #ddd; padding: 8px;">${sand}</td>
                <td style="border: 1px solid #ddd; padding: 8px;"><b>${bulkBags > 0 ? bulkBags + ' bulk bag(s)' : ''} ${miniBags > 0 ? miniBags + ' mini bag(s)' : ''} ${smallBags > 0 ? smallBags + ' small plastic bag(s)' : ''}</b></td>
            </tr>
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">Cement(kg)</td>
                <td style="border: 1px solid #ddd; padding: 8px;">${cement}</td>
                <td style="border: 1px solid #ddd; padding: 8px;"><b>${Math.ceil(cement / 25)} bag(s)</b></td>
            </tr>
        </table>
        <div class="grey-box" style="margin-bottom: -10px">
            <i>Total includes 10 mm mortar joint</i>
        </div>
        <div class="grey-box" style="margin-top: 0px;"><em>Click here to browse <b><a href="/category/building-supplies/bricks">bricks</a></b> or <b><a href="/category/building-supplies/blocks">blocks</a></b></em></div>`;
	document.getElementById("brickBlockResult").innerHTML = resultHtml;
}
