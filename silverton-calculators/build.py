#!/usr/bin/env python3
"""
Build script for the Silverton Builders Merchants specialist calculator pages.

Generates, from one set of templates:

  cms-snippets/<slug>.html      Body-only blocks (relative URLs) to paste into the
                                K8 CMS page at /page/<slug>.
  preview/<slug>.html           Full standalone HTML pages (absolute URLs) for
                                local QA at 390 x 844 and browser testing.

@@BASE@@ in a template becomes "" (relative) in the snippet and
"https://www.silvertonbuildersmerchants.com" in the preview. In previews,
links to the four calculator pages are rewritten to the local preview files so
the preview is self-navigable.

Usage:  python3 build.py     (from this directory)
"""
import pathlib
import re

from tpl_brick import BRICK
from tpl_stone import STONE
from tpl_paving import PAVING
from tpl_hub import HUB

ROOT = pathlib.Path(__file__).resolve().parent
LIVE = "https://www.silvertonbuildersmerchants.com"

# ---------------------------------------------------------------------------
# Shared CSS = the original calculator CSS (unchanged, both duplicate rule
# blocks kept in their original order so the cascade is identical) plus the
# styles for the new guide/shop/FAQ sections on the specialist pages.
# ---------------------------------------------------------------------------
CALC_CSS = """
\tbody {
\t\tfont-family: 'Poppins', sans-serif;
\t\tbackground-color: #ffffff;
\t\tmargin: 0;
\t\tpadding: 0;
\t\tcolor: #18452e;
\t}

\t@media (max-width: 992px) {
\t\t/* Adjust this breakpoint as needed */
\t\t.fixed-box {
\t\t\tposition: static;
\t\t\t/* Change to static so it appears underneath the calculator */
\t\t\twidth: auto;
\t\t\t/* Adjust width as needed */
\t\t\tmargin-top: 20px;
\t\t\t/* Add margin to separate it from the calculator */
\t\t\tmargin-bottom: 20px;
\t\t\t/* Add margin to separate it from other content */
\t\t\ttext-align: center;
\t\t}
\t}

\t.calculator-container {
\t\tmax-width: 700px;
\t\tbackground-color: #ffffff;
\t\tborder-radius: 20px;
\t\tpadding: 15px;
\t\tbox-shadow: 0 0 10px rgba(0, 0, 0, 0);
\t\toverflow: hidden;
\t\tposition: relative;
\t\tmargin: 20px auto;
\t}

\t.materials-heading {
\t\ttext-align: center;
\t\tfont-size: 24px;
\t\tmargin-bottom: 0px;
\t}

\t.materials-disclaimer {
\t\tbackground-color: #f0f0f0;
\t\tborder-radius: 10px;
\t\tpadding: 10px;
\t\tmargin-bottom: 20px;
\t\ttext-align: center;
\t\tmax-width: 100%;
\t\t/* Limiting the width */
\t\toverflow-x: auto;
\t\t/* Adding horizontal scrollbar if needed */
\t}

\t.materials-disclaimer p {
\t\tcolor: #666;
\t\tfont-size: 14px;
\t}

\t.calculator-buttons {
\t\tdisplay: flex;
\t\tjustify-content: space-between;
\t\tmargin-bottom: 20px;
\t\tflex-wrap: wrap;
\t}

\t.calculator-buttons .tab {
\t\tflex: 0 0 calc(50% - 10px);
\t\tbackground-color: #18452e;
\t\tcolor: #ffffff;
\t\tborder: none;
\t\tpadding: 25px 0;
\t\tcursor: pointer;
\t\tborder-radius: 10px;
\t\ttext-transform: uppercase;
\t\ttransition: background-color 0.3s ease;
\t\tfont-weight: 500;
\t\tmargin-bottom: 10px;
\t\tfont-family: 'Poppins', sans-serif;
\t\tfont-size: 16px;
\t\ttext-align: center;
\t}

\t.calculator-buttons .tab.active {
\t\tcolor: #daaf3b;
\t}

\t.calculator-buttons .tab:hover {
\t\tbackground-color: #3c6e4d;
\t}

\t.tabcontent {
\t\twidth: 100%;
\t\tdisplay: none;
\t\tpadding: 20px;
\t\tborder-radius: 10px;
\t\tbackground-color: #f9f9f9;
\t\tmargin-top: 10px;
\t\ttext-align: center;
\t}

\t.tabcontent.active {
\t\tdisplay: block;
\t}

\t.result {
\t\tfont-size: 18px;
\t\tmargin-top: 15px;
\t\tmargin-bottom: 15px;
\t}

\t.grey-box {
\t\tbackground-color: #f0f0f0;
\t\tpadding: 10px;
\t\tborder-radius: 10px;
\t\tmargin-top: 20px;
\t\tmargin-bottom: 20px;
\t\ttext-align: center;
\t\tmax-width: 100%;
\t\t/* Limiting the width */
\t\toverflow-x: auto;
\t\t/* Adding horizontal scrollbar if needed */
\t}

\t.button-calculate {
\t\tbackground-color: #18452e;
\t\tcolor: #fff;
\t\tborder: none;
\t\tpadding: 2px 15px;
\t\tcursor: pointer;
\t\tborder-radius: 10px;
\t\ttext-transform: uppercase;
\t\ttransition: background-color 0.3s ease;
\t\tfont-weight: 500;
\t\tmargin-bottom: 10px;
\t\tfont-family: 'Poppins', sans-serif;
\t\tfont-size: 16px;
\t\ttext-align: center;
\t}

\t.button-calculate:hover {
\t\tbackground-color: #3c6e4d;
\t}

\t.small-text {
\t\tfont-size: smaller;
\t}

\t.grey-container {
\t\tbackground-color: #f0f0f0;
\t\tpadding: 10px;
\t\t/* Add padding */
\t\tborder-radius: 10px;
\t\tmargin-top: 20px;
\t\tmargin-right: 20px;
\t\ttext-align: center;
\t\tmax-width: 100%;
\t\t/* Limiting the width */
\t\toverflow-x: auto;
\t\t/* Adding horizontal scrollbar if needed */
\t}

\t.switch.active {
\t\tcolor: #ffffff;
\t\tbackground-color: #2ecc71;
\t}

\t.calculator-options {
\t\tdisplay: flex;
\t\tjustify-content: space-between;
\t\twidth: 60%;
\t\tmargin: 0 auto;
\t}

\t.calculator-options .switch {
\t\tflex: 1;
\t\ttext-align: center;
\t\tcursor: pointer;
\t\tbackground-color: #f0f0f0;
\t\tborder-radius: 5px;
\t\tpadding: 10px;
\t\ttransition: background-color 0.3s ease;
\t}

\t.calculator-options .switch.active {
\t\tbackground-color: #daaf3b;
\t\tcolor: #ffffff;
\t}

\t.calculator-buttons .wide-tab {
\t\tflex-grow: 2;
\t\t/* Makes the tab span the width of two buttons */
\t}

\t.calculator-buttons {
\t\tdisplay: flex;
\t\t/* Ensures buttons are laid out in a row */
\t\tgap: 10px;
\t\t/* Optional spacing between buttons */
\t}

\t.tab {
\t\tpadding: 10px 20px;
\t\t/* Adjusts button size */
\t\tflex-grow: 1;
\t\t/* Ensures other buttons occupy equal space */
\t\ttext-align: center;
\t\tborder: 1px solid #ccc;
\t\tbackground-color: #f4f4f4;
\t\tcursor: pointer;
\t}

\t.tab.active {
\t\tbackground-color: #18452e;
\t\tfont-weight: bold;
\t}
"""

GUIDE_CSS = """
\t/* ===== Styles for the guide, shop links and FAQ sections on the
\t   specialist calculator pages (added 2026 — does not affect the
\t   original calculator controls above). ===== */
\t.calc-guide {
\t\tfont-family: 'Poppins', sans-serif;
\t\tcolor: #333733;
\t\ttext-align: left;
\t}

\t.calc-guide p {
\t\tline-height: 1.65;
\t\tfont-size: 15px;
\t\tmargin: 0 0 14px;
\t}

\t.calc-guide h2 {
\t\tcolor: #18452e;
\t\tfont-size: 21px;
\t\tmargin: 26px 0 12px;
\t\ttext-align: left;
\t}

\t.calc-guide h3 {
\t\tcolor: #18452e;
\t\tfont-size: 17px;
\t\tmargin: 0 0 10px;
\t\ttext-align: left;
\t}

\t.calc-guide ol,
\t.calc-guide ul {
\t\tline-height: 1.65;
\t\tfont-size: 15px;
\t\tpadding-left: 22px;
\t\tmargin: 0 0 14px;
\t\ttext-align: left;
\t}

\t.calc-guide li {
\t\tmargin-bottom: 8px;
\t}

\t.calc-guide img {
\t\tmax-width: 100%;
\t\theight: auto;
\t}

\t.calc-h1 {
\t\tcolor: #18452e;
\t\tfont-size: 26px;
\t\ttext-align: center;
\t\tmargin: 6px 0 4px;
\t\tfont-weight: 600;
\t}

\t.calc-back {
\t\tmargin-bottom: 4px;
\t}

\t.calc-back a {
\t\tcolor: #18452e;
\t\tfont-weight: 600;
\t\ttext-decoration: none;
\t\tfont-size: 14px;
\t}

\t.calc-back a:hover {
\t\ttext-decoration: underline;
\t}

\t.calc-cards {
\t\tdisplay: grid;
\t\tgrid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
\t\tgap: 12px;
\t\tmargin: 14px 0 18px;
\t\tpadding: 0;
\t}

\t.calc-card {
\t\tbackground: #ffffff;
\t\tborder: 1px solid #e2e6e2;
\t\tborder-radius: 10px;
\t\tpadding: 14px 16px;
\t\ttext-decoration: none;
\t\tdisplay: block;
\t}

\t.calc-card:hover {
\t\tborder-color: #daaf3b;
\t}

\t.calc-card strong {
\t\tdisplay: block;
\t\tcolor: #18452e;
\t\tfont-size: 15.5px;
\t\tmargin-bottom: 5px;
\t\tfont-weight: 600;
\t}

\t.calc-card span {
\t\tdisplay: block;
\t\tcolor: #5a615a;
\t\tfont-size: 13.5px;
\t\tline-height: 1.5;
\t}

\t.calc-shop {
\t\tmargin-top: 22px;
\t\ttext-align: left;
\t}

\t.calc-products {
\t\tfont-size: 14px;
\t\tcolor: #444a44;
\t\tline-height: 1.9;
\t\tmargin: 0 0 4px;
\t}

\t.calc-products a {
\t\tcolor: #18452e;
\t\tfont-weight: 600;
\t}

\t.assumptions {
\t\tbackground: #f0f0f0;
\t\tborder-radius: 10px;
\t\tpadding: 16px 20px;
\t}

\t.assumptions ul {
\t\tmargin: 0;
\t}

\t.faq-item {
\t\tbackground: #f9f9f9;
\t\tborder: 1px solid #e2e6e2;
\t\tborder-radius: 10px;
\t\tmargin-bottom: 10px;
\t\toverflow: hidden;
\t}

\t.faq-item summary {
\t\tcursor: pointer;
\t\tpadding: 13px 16px;
\t\tfont-weight: 600;
\t\tcolor: #18452e;
\t\tfont-size: 15px;
\t}

\t.faq-item[open] summary {
\t\tborder-bottom: 1px solid #e2e6e2;
\t}

\t.faq-item p {
\t\tpadding: 12px 16px 14px;
\t\tmargin: 0;
\t}

\t.calc-more-link {
\t\ttext-align: center;
\t\tmargin: 16px 0 2px;
\t\tfont-size: 14.5px;
\t}

\t.calc-hub-links h2 {
\t\tmargin-top: 0;
\t}

\t@media (max-width: 480px) {
\t\t.calc-cards {
\t\t\tgrid-template-columns: 1fr;
\t\t}

\t\t.calc-guide h2 {
\t\t\tfont-size: 19px;
\t\t}
\t}
"""

# ---------------------------------------------------------------------------
# Shared tracking layer — loaded on the hub and every specialist page.
# Pushes GA4-ready events to the dataLayer (works with the site's GTM setup):
#   calculator_start, calculator_complete, calculator_error,
#   product_or_category_click  — all carrying calculator_type.
# ---------------------------------------------------------------------------
TRACKING_JS = """<script>
\t/* ===== Calculator tracking — pushes to the GTM dataLayer. See tracking.md ===== */
\t(function () {
\t\twindow.SilvertonCalc = {
\t\t\tstarted: {},
\t\t\tTYPE_BY_CONTAINER: {
\t\t\t\tbrickBlockCalculator: 'brick_and_block',
\t\t\t\tareaVolumeCalculator: 'decorative_stone',
\t\t\t\ttileCalculator: 'roof_tiles',
\t\t\t\tpavingCalculator: 'paving'
\t\t\t},
\t\t\ttypeForLink: function (link) {
\t\t\t\tvar owner = link.closest ? link.closest('.tabcontent,[data-calculator-type]') : null;
\t\t\t\tif (!owner) { return 'unknown'; }
\t\t\t\treturn (owner.dataset && owner.dataset.calculatorType) || this.TYPE_BY_CONTAINER[owner.id] || 'unknown';
\t\t\t},
\t\t\tpush: function (data) {
\t\t\t\twindow.dataLayer = window.dataLayer || [];
\t\t\t\twindow.dataLayer.push(data);
\t\t\t},
\t\t\tstart: function (type) {
\t\t\t\tif (this.started[type]) { return; }
\t\t\t\tthis.started[type] = true;
\t\t\t\tthis.push({ event: 'calculator_start', calculator_type: type });
\t\t\t},
\t\t\tcomplete: function (type, mode) {
\t\t\t\tvar payload = { event: 'calculator_complete', calculator_type: type };
\t\t\t\tif (mode) { payload.calculator_mode = mode; }
\t\t\t\tthis.push(payload);
\t\t\t},
\t\t\terror: function (type, message) {
\t\t\t\tthis.push({ event: 'calculator_error', calculator_type: type, error_message: message });
\t\t\t}
\t\t};

\t\t/* product_or_category_click — delegated so links rendered inside
\t\t   calculator results are tracked too. */
\t\tdocument.addEventListener('click', function (ev) {
\t\t\tvar link = ev.target && ev.target.closest ? ev.target.closest('a[href]') : null;
\t\t\tif (!link) { return; }
\t\t\tvar url;
\t\t\ttry { url = new URL(link.href, window.location.href); } catch (e) { return; }
\t\t\tvar linkType = null;
\t\t\tif (url.pathname.indexOf('/category/') === 0) { linkType = 'category'; }
\t\t\telse if (url.pathname.indexOf('/product/') === 0) { linkType = 'product'; }
\t\t\tif (!linkType) { return; }
\t\t\twindow.SilvertonCalc.push({
\t\t\t\tevent: 'product_or_category_click',
\t\t\t\tcalculator_type: window.SilvertonCalc.typeForLink(link),
\t\t\t\tlink_url: url.href,
\t\t\t\tlink_text: (link.textContent || '').replace(/\\s+/g, ' ').trim().slice(0, 100),
\t\t\t\tlink_type: linkType
\t\t\t});
\t\t});
\t})();
</script>"""

# ---------------------------------------------------------------------------
# Preview chrome (standalone pages only — the CMS supplies its own header,
# footer, breadcrumb and H1 on the live site).
# ---------------------------------------------------------------------------
PREVIEW_CSS = """
\t.pv-header { background: #18452e; color: #fff; padding: 14px 18px; font-family: 'Poppins', sans-serif; }
\t.pv-header-inner { max-width: 1000px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
\t.pv-brand { color: #fff; font-weight: 700; font-size: 18px; text-decoration: none; letter-spacing: .02em; }
\t.pv-brand span { color: #daaf3b; }
\t.pv-nav a { color: #cfe0d6; text-decoration: none; font-size: 14px; margin-left: 16px; }
\t.pv-nav a:hover { color: #fff; }
\t.pv-breadcrumb { background: #f2f4f2; border-bottom: 1px solid #e2e6e2; padding: 9px 18px; font-size: 13.5px; font-family: 'Poppins', sans-serif; color: #4c554c; }
\t.pv-breadcrumb-inner { max-width: 1000px; margin: 0 auto; }
\t.pv-breadcrumb a { color: #18452e; text-decoration: none; }
\t.pv-h1 { font-family: 'Poppins', sans-serif; color: #18452e; font-size: 28px; text-align: center; max-width: 700px; margin: 26px auto 0; padding: 0 15px; font-weight: 600; }
\t.pv-footer { background: #18452e; color: #cfe0d6; margin-top: 50px; padding: 26px 18px; font-size: 13.5px; line-height: 1.7; font-family: 'Poppins', sans-serif; }
\t.pv-footer-inner { max-width: 760px; margin: 0 auto; }
\t.pv-footer a { color: #daaf3b; text-decoration: none; }
\t.pv-note { font-size: 12px; color: #9db5a5; }
\tbody.pv-preview { padding-top: 0; }
"""

SNIPPET_HEADER = """<!-- {page_name} — copy this ENTIRE file and paste it into the CMS page body for /page/{slug}. Nothing to run or build: it is plain HTML. -->
<style>{calc_css}{guide_css}</style>
"""


def build_preview_head(page):
    return f"""\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>{page['title']}</title>
\t<meta name="description" content="{page['description']}">
\t<link rel="canonical" href="{LIVE}/page/{page['slug']}">
\t<meta name="robots" content="noindex">
\t<meta property="og:type" content="website">
\t<meta property="og:site_name" content="Silverton Builders Merchants">
\t<meta property="og:title" content="{page['title']}">
\t<meta property="og:description" content="{page['description']}">
\t<meta property="og:url" content="{LIVE}/page/{page['slug']}">
\t<meta property="og:image" content="{page['og_image']}">
\t<meta name="twitter:card" content="summary_large_image">
\t<link rel="preconnect" href="https://fonts.googleapis.com">
\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
\t<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
\t<style>{CALC_CSS}{GUIDE_CSS}{PREVIEW_CSS}</style>"""


def inject_tracking(body):
    """Insert the shared tracking layer immediately before the first page
    script so SilvertonCalc exists when the calculator script runs."""
    idx = body.find("<script>")
    assert idx != -1, "page template has no script tag"
    return body[:idx] + TRACKING_JS + "\n" + body[idx:]


def build_preview_page(page):
    body = inject_tracking(page["body"])
    # Local navigation between preview pages.
    for slug, fname in PREVIEW_LINKS.items():
        body = body.replace(f"@@BASE@@/page/{slug}", fname)
    body = body.replace("@@BASE@@", LIVE)

    crumbs = "".join(
        f'\t\t<a href="{url}">{name}</a> &rsaquo; ' for name, url in page["crumbs"][:-1]
    )
    crumbs += f"<strong>{page['crumbs'][-1][0]}</strong>"

    return f"""<!doctype html>
<html lang="en-GB">
<head>
{build_preview_head(page)}
</head>
<body class="pv-preview">
\t<header class="pv-header">
\t\t<div class="pv-header-inner">
\t\t\t<a class="pv-brand" href="{LIVE}/">SILVERTON <span>BUILDERS MERCHANTS</span></a>
\t\t\t<nav class="pv-nav">
\t\t\t\t<a href="{LIVE}/">Live site</a>
\t\t\t\t<a href="materials-calculator-hub.html">Calculator hub</a>
\t\t\t\t<a href="index.html">Preview index</a>
\t\t\t</nav>
\t\t</div>
\t</header>
\t<nav class="pv-breadcrumb"><div class="pv-breadcrumb-inner">{crumbs}</div></nav>
\t<h1 class="pv-h1">{page['h1']}</h1>
\t<main>
{body}
\t</main>
\t<footer class="pv-footer">
\t\t<div class="pv-footer-inner">
\t\t\t<p><strong>Silverton Builders Merchants Ltd</strong> &middot; Devereux Farm, Walton Road, Kirby-le-Soken, Frinton-on-Sea, Essex CO13 0DA</p>
\t\t\t<p>Webshop support: <a href="tel:01255446920">01255 446920</a> &middot; <a href="mailto:info@silverton.uk.com">info@silverton.uk.com</a> &middot; <a href="{LIVE}/page/branches/branch-finder">Branch finder</a></p>
\t\t\t<p class="pv-note">Local preview build for QA — this file is not part of silvertonbuildersmerchants.com. Deployment-ready blocks are in <code>cms-snippets/</code>; metadata and tracking setup are documented in <code>metadata.md</code> and <code>tracking.md</code>.</p>
\t\t</div>
\t</footer>
</body>
</html>
"""


def build_snippet(page):
    body = inject_tracking(page["body"]).replace("@@BASE@@", "")
    header = SNIPPET_HEADER.format(
        page_name=page["page_name"],
        slug=page["slug"],
        h1_text=page["h1"],
        calc_css=CALC_CSS,
        guide_css=GUIDE_CSS,
    )
    return header + body + "\n"


PAGES = [BRICK, STONE, PAVING]
HUB_PAGE = HUB

PREVIEW_LINKS = {
    "brick-and-block-calculator": "brick-and-block-calculator.html",
    "decorative-stone-calculator": "decorative-stone-calculator.html",
    "paving-calculator": "paving-calculator.html",
    "materials-calculator": "materials-calculator-hub.html",
}


def main():
    snip_dir = ROOT / "cms-snippets"
    prev_dir = ROOT / "preview"
    snip_dir.mkdir(exist_ok=True)
    prev_dir.mkdir(exist_ok=True)

    for page in PAGES + [HUB_PAGE]:
        slug = page["slug"]
        snippet_name = page.get("snippet_name", f"{slug}.html")
        (snip_dir / snippet_name).write_text(build_snippet(page), encoding="utf-8")
        (prev_dir / page["preview_name"]).write_text(build_preview_page(page), encoding="utf-8")
        print(f"built {snippet_name} + preview/{page['preview_name']}")

    index = PREVIEW_INDEX
    (prev_dir / "index.html").write_text(index, encoding="utf-8")
    print("built preview/index.html")

    # Basic sanity checks on generated output.
    for f in sorted(snip_dir.glob("*.html")) + sorted(prev_dir.glob("*.html")):
        if f.name == "index.html":
            continue
        text = f.read_text(encoding="utf-8")
        assert "@@BASE@@" not in text, f"unreplaced token in {f}"
        assert "SilvertonCalc" in text, f"tracking layer missing in {f}"
    print("sanity checks passed")


PREVIEW_INDEX = f"""<!doctype html>
<html lang="en-GB">
<head>
\t<meta charset="utf-8">
\t<meta name="viewport" content="width=device-width, initial-scale=1">
\t<title>Calculator pages — local preview | Silverton Builders Merchants</title>
\t<meta name="robots" content="noindex">
\t<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
\t<style>
\t\tbody {{ font-family: 'Poppins', sans-serif; color: #333733; margin: 0; background: #fbfcfb; }}
\t\t.wrap {{ max-width: 720px; margin: 0 auto; padding: 40px 18px 60px; }}
\t\th1 {{ color: #18452e; font-size: 26px; }}
\t\tp {{ line-height: 1.65; }}
\t\t.cards {{ display: grid; gap: 14px; margin-top: 24px; }}
\t\t.card {{ background: #fff; border: 1px solid #e2e6e2; border-radius: 12px; padding: 18px 20px; text-decoration: none; display: block; }}
\t\t.card:hover {{ border-color: #daaf3b; }}
\t\t.card strong {{ color: #18452e; font-size: 17px; display: block; margin-bottom: 6px; }}
\t\t.card span {{ color: #5a615a; font-size: 14px; line-height: 1.55; display: block; }}
\t\t.note {{ font-size: 13px; color: #6a736a; background: #f0f2f0; border-radius: 10px; padding: 12px 16px; margin-top: 26px; }}
\t</style>
</head>
<body>
\t<div class="wrap">
\t\t<h1>Silverton calculator pages — local preview</h1>
\t\t<p>Standalone previews of the new specialist calculator pages and the updated hub. Test each one at 390 &times; 844 (iPhone-sized) for the mobile acceptance check. The deployment-ready CMS blocks are in <code>../cms-snippets/</code>.</p>
\t\t<div class="cards">
\t\t\t<a class="card" href="materials-calculator-hub.html"><strong>Materials Calculator — updated hub</strong><span>The existing master page kept as a hub, now with links to each specialist calculator and tracking events. /page/materials-calculator</span></a>
\t\t\t<a class="card" href="brick-and-block-calculator.html"><strong>Brick &amp; Block Calculator</strong><span>Bricks, blocks, sand and cement for single or double skin walls. /page/brick-and-block-calculator</span></a>
\t\t\t<a class="card" href="decorative-stone-calculator.html"><strong>Decorative Stone Calculator</strong><span>Gravel and decorative stone coverage by area or depth, in bulk, mini bulk and small bags. /page/decorative-stone-calculator</span></a>
\t\t\t<a class="card" href="paving-calculator.html"><strong>Paving Calculator</strong><span>Slab counts for patios and paths, including patio pack coverage. /page/paving-calculator</span></a>
\t\t</div>
\t\t<p class="note">These preview files hotlink images and category/product links to the live silvertonbuildersmerchants.com site, so links out of the calculators work exactly as they will in production. Product and category links open the live site — use the browser back button to return.</p>
\t</div>
</body>
</html>
"""

if __name__ == "__main__":
    main()
