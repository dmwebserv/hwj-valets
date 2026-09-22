# Silverton Builders Merchants — specialist calculator pages

Turns the single materials calculator page (`/page/materials-calculator`) into
three indexable specialist calculator pages plus an updated hub, with per-page
SEO copy and per-calculator GA4 tracking. Calculation rules are **identical**
to the live master page — verified automatically against the original code
(see QA below).

Built for https://www.silvertonbuildersmerchants.com (K8 Web Builder CMS).

## What's here

```
cms-snippets/                      Deployment-ready page bodies (relative URLs)
  brick-and-block-calculator.html    → /page/brick-and-block-calculator
  decorative-stone-calculator.html   → /page/decorative-stone-calculator
  paving-calculator.html             → /page/paving-calculator
  materials-calculator-hub.html      → replaces the block on /page/materials-calculator
preview/                           Standalone pages for browser QA (absolute URLs)
  index.html                         local index — open this first
  …one preview per snippet + the hub
tpl_*.py, build.py                 Source templates + generator (single source of truth)
qa/                                Automated test harness (node qa/harness.js)
metadata.md                        Titles, descriptions, canonicals, sitemap entries
tracking.md                        GA4/GTM event specification and setup steps
```

Edit the `tpl_*.py` files and run `python3 build.py` — never edit
`cms-snippets/` or `preview/` by hand, or your changes will be overwritten.

## Install (CMS)

1. **Create three new CMS pages** with these names/URLs (the CMS renders the
   page name as the H1 and breadcrumb, exactly as it does for the existing
   materials calculator page):
   - `Brick & Block Calculator` → `/page/brick-and-block-calculator`
   - `Decorative Stone Calculator` → `/page/decorative-stone-calculator`
   - `Paving Calculator` → `/page/paving-calculator`
2. **Paste each snippet** from `cms-snippets/` into the matching page body
   (everything below the instruction comment). Do not paste the comment.
3. **Set the page metadata** (title tag, meta description, canonical) from
   `metadata.md` if the CMS exposes SEO fields per page.
4. **Update the hub**: replace the existing calculator block on
   `/page/materials-calculator` with `cms-snippets/materials-calculator-hub.html`
   (body only). Everything else on that page (bag sizes, delivery vehicles
   accordions, page heading) stays as it is.
5. **Verify after publishing** (see checklist below).

## Requirement → where it is handled

| Requirement | Where |
| --- | --- |
| Stable indexable URLs, master kept as hub | Three new `/page/<name>-calculator` URLs; hub retained and linked both ways |
| Only the relevant tool per page | Each specialist snippet contains exactly one calculator |
| Unique title, H1, intro, instructions, assumptions, FAQs, category + product links | Per-page copy in each snippet; metadata in `metadata.md` |
| Calculation rules consistent with current calculators | Formulas copied verbatim; verified byte-for-byte against the original code by `qa/harness.js` |
| Links between hub and specialist pages | Hub: link cards + per-tool "full guide" links. Specialists: back-link + cross-links |
| Track start/complete/error/click by calculator type | Shared tracking layer pushes `calculator_start`, `calculator_complete`, `calculator_error`, `product_or_category_click` to the dataLayer with a `calculator_type` parameter — see `tracking.md` |

## Acceptance criteria → how to verify

- **Self-referencing canonical + unique metadata** — previews carry the exact
  tags; after publishing, view-source each URL and confirm the canonical and
  unique title/description. If the CMS does not emit canonicals automatically,
  add them from `metadata.md` via the CMS SEO field.
- **Results match the master tool** — already proven automatically: the
  harness runs the representative inputs below through the *original* master
  code and the new pages and asserts identical output. Re-run any time:
  `node qa/harness.js` (213 checks).
- **Usable at 390 × 844, no horizontal scrolling** — test with the previews
  (`preview/index.html`) in device mode. Layout is a single fluid 700px-max
  column; link cards collapse to one per row under 480px; result tables are
  width:100%.
- **Category and product routes immediately after the result** — each result
  container ends with the original in-result category links, followed directly
  by a "Shop …" card block with category and product routes.
- **Master does not duplicate specialist copy** — the hub only gained short
  link cards and one-line pointers; all intros/instructions/assumptions/FAQs
  live on the specialist pages only.

## Representative inputs (expected outputs, all pages)

| Calculator | Inputs | Expected |
| --- | --- | --- |
| Brick & Block | 5 × 2 m, standard brick, single skin | 600 bricks · 600 kg sand (1 mini + 7 small bags) · 100 kg cement (4 bags) |
| Brick & Block | 5 × 2 m, standard block, single skin | 100 blocks · 200 kg sand (8 small bags) · 40 kg cement (2 bags) |
| Brick & Block | 5 × 2 m, custom 215 × 65 mm, single | 716 bricks · 716 kg sand (1 mini + 12 small) · 120 kg cement (5 bags) |
| Brick & Block | 5 × 2 m, standard brick, double skin | 1200 bricks · 1200 kg sand (1 bulk + 14 small) · 200 kg cement (8 bags) |
| Decorative Stone | 4 × 5 m | 20.00 square meters |
| Decorative Stone | 4 × 5 m at 50 mm | 1.00 m³ · 1.67 T · 1 bulk + 1 mini bulk + 20 small bags |
| Paving | 4 × 5 m, 600 × 600 slabs | 20.00 m² · 56 slabs |
| Paving | 4 × 5 m, patio packs | 20.00 m² · Approx 18 of each size |

## Behaviours preserved from the live master (deliberate)

These look like bugs but are kept so results and UX match the current tool.
All are safe to fix later *everywhere at once* if the client wants:

- **Decorative stone volume results only refresh on the Calculate button.**
  Typing refreshes the area result (the original page's `calculateResults()`
  never called the volume function), so a volume result can be replaced by an
  area result while typing. Preserved on both hub and specialist page.
- **Skin changes (single/double) do not auto-recalculate** — hence the
  "press calculate again" note, retained from the master.
- **The hidden Tile Calculator markup is retained on the hub** with no tab
  linking to it, exactly as the master has it today.
- **Double spaces in the sand bag breakdown** when a middle bag size is empty
  (e.g. "1 bulk bag(s)  14 small plastic bag(s)") — that is the original
  template's rendering.

One deliberate fix: the **Patio Packs checkbox now hides the custom size
fields**. The master page defines `toggleCustomSizeInputs()` for exactly this
but never wired it up. Results are unaffected.

Small cleanups with no behavioural change: duplicate function definitions and
double-bound event listeners from the original page are consolidated, and
invalid inputs now show a friendly message (and fire `calculator_error`)
instead of rendering `NaN`.

## Product and category links

Chosen from live category listings on 2026-09-18 and verified to exist.
Product availability changes — re-check the product links periodically and
swap any that disappear (they are ordinary links; nothing else references
them). Category routes are stable.
