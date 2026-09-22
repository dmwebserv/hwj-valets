# Calculator tracking (GA4 via GTM dataLayer)

Every calculator page (the hub and each specialist page) loads a small shared
tracking layer that pushes events to `window.dataLayer` — the same layer the
site's Google Tag Manager container already uses. No cookies, no external
calls; everything is wired for GTM to forward to GA4.

## Events

| Event | Fires when | Parameters |
| --- | --- | --- |
| `calculator_start` | The visitor's first interaction with a calculator (typing in a field or pressing Calculate). Once per calculator per page view. | `calculator_type` |
| `calculator_complete` | A calculation renders a valid result (auto-recalculation while typing or the Calculate button). | `calculator_type`, `calculator_mode` |
| `calculator_error` | A calculation is attempted with invalid input (empty/zero measurements, missing custom size). A friendly message replaces the result. | `calculator_type`, `error_message` |
| `product_or_category_click` | A click on any `/category/…` or `/product/…` link on the page — including links rendered inside results. Other links (e.g. hub ↔ specialist navigation) are not counted. | `calculator_type`, `link_url`, `link_text`, `link_type` |

### `calculator_type` values

| Value | Calculator |
| --- | --- |
| `brick_and_block` | Brick & Block Calculator (hub tab + specialist page) |
| `decorative_stone` | Decorative Stone Calculator (hub "Area & Volume" tab + specialist page) |
| `paving` | Paving Calculator (hub tab + specialist page) |

### `calculator_mode` values (on `calculator_complete`)

| Calculator | Modes |
| --- | --- |
| `brick_and_block` | `single_skin`, `double_skin` |
| `decorative_stone` | `area`, `volume` |
| `paving` | `patio_packs`, `custom_size` |

### `error_message` values

Short, stable strings: `Enter a wall length and height in metres, greater
than zero.`, `Enter a custom brick or block width and height in millimetres,
greater than zero.`, `Enter a width and length in metres, greater than zero.`,
`Enter a depth in millimetres, greater than zero.`, `Enter a slab width and
height in millimetres, greater than zero.`

## GTM setup (one-time)

The site already runs GTM (the calculators' `data-gtm-form-interact-field-id`
attributes confirm it), so the events only need triggers and a GA4 event tag:

1. **Create Data Layer variables** (Variables → New → Data Layer Variable):
   `calculator_type`, `calculator_mode`, `error_message`, `link_url`,
   `link_text`, `link_type` (Data Layer Variable Name = the parameter name).
2. **Create one Custom Event trigger per event name**: `calculator_start`,
   `calculator_complete`, `calculator_error`, `product_or_category_click`
   (Trigger Type: Custom Event, "Use regex matching" off).
3. **Create one GA4 Event tag per trigger** (or one tag with a trigger
   group): Tag Type: Google Analytics: GA4 Event, Measurement ID = the site's
   GA4 config; Event Name = the same custom event name; Event Parameters =
   pass through the Data Layer variables from step 1 (`calculator_type`,
   `calculator_mode` / `error_message` / `link_url`, `link_text`,
   `link_type`).
4. Preview in GTM (Preview mode on the live site), interact with each
   calculator, and confirm the four events appear in the Preview tab and in
   GA4 Realtime.

## GA4 setup

- The events arrive as custom events with the names above — no GA4
  configuration change is needed for them to be collected.
- **Key events (conversions):** consider marking `calculator_complete` and
  `product_or_category_click` as key events (Admin → Events → toggle "Mark as
  key event").
- **Custom dimensions** (Admin → Custom definitions → Event-scoped) if you
  want to slice by them in reports:
  - `calculator_type` (e.g. "Calculators — starts/completes by type")
  - `calculator_mode` (e.g. "single vs double skin", "patio packs vs custom")
  - `link_type` (category vs product clicks)
- Useful explorations:
  - Completions by `calculator_type` → which calculators drive engagement.
  - `product_or_category_click` by `calculator_type` → which calculators
    send shoppers into the catalogue.
  - `calculator_error` count by type → input UX problems.

## Behaviour notes

- **No events on page load.** The paving calculators pre-calculate a default
  result on load (as they always have); tracking starts only when the visitor
  interacts.
- **On the hub**, typing into one calculator refreshes all of them (original
  page behaviour) but events are attributed only to the calculator the
  visitor is actually using.
- The unreachable Tile Calculator markup retained on the hub never fires
  events (no tab links to it, matching the live master).
- `product_or_category_click` uses event delegation, so category links that
  appear inside a freshly rendered result (e.g. "Click here to browse
  bricks") are tracked without any extra wiring.

## Testing without GTM

Open any preview page (or the live page), use the calculator, then in the
browser console:

```js
dataLayer.filter(e => e.event.indexOf('calculator') === 0 || e.event === 'product_or_category_click')
```

You should see the start/complete (or error) sequence with the correct
`calculator_type`.
