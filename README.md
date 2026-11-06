# HWJ Valets

Marketing website for HWJ Valets, a mobile car valeting and detailing business based in Colchester, covering Essex and parts of Suffolk.

Static HTML/CSS site, no build step or framework. Pages:

- `index.html`: homepage with services, gallery, about, contact details and enquiry form
- `book.html`: booking landing page served at `/book` - hands off to the booking system at `hwj-valets.vercel.app/book`
- `privacy-policy.html`: privacy information for enquiries
- `thanks.html`: enquiry form landing page, marked noindex

## Contact and social details

- Phone: 07926 517296
- Email: harry@hwjvalets.co.uk
- Facebook: https://www.facebook.com/people/HWJ-Valets/61579054444028/
- Instagram: https://www.instagram.com/hwjvalets/
- Service area: based in Colchester, covering Essex and parts of Suffolk

## Content sourced from

All copy, service packages, contact details and photos come from HWJ Valets' supplied materials and public social profiles:

- Business bio, phone, email, coverage area and review details: HWJ Valets materials and public profiles
- Service package descriptions: real promotional flyers and supplied package wording
- "Premium Detail" write-up: a real Facebook post about an Audi A5 job
- Gallery photos: real job photos, including the Stage 1 paint correction images in `images/corsa-paint1.jpg` and `images/corsa-paint-close.jpg`
- Logo: supplied directly, resized into `images/logo.png` plus favicon assets

Package prices are shown as starting prices only and may vary by vehicle size, condition and the work required. Every package links through to a WhatsApp quote request, matching HWJ Valets' existing "Call or WhatsApp to book" pattern.

## Form handling

The enquiry form posts to [FormSubmit.co](https://formsubmit.co) at `https://formsubmit.co/harry@hwjvalets.co.uk`, uses the table template, and redirects successful submissions to `https://hwjvalets.co.uk/thanks.html`.

FormSubmit requires a one-time activation email for `harry@hwjvalets.co.uk` before live enquiries are delivered. Do not send a real test submission or activate the address without the business owner's approval.

## Google Tag Manager, consent and Google Ads setup

- Google Tag Manager container snippets (head + noscript body) are installed on every page: index, thanks, privacy-policy, 404 and book. The container ID is `GTM-KP9CNRDW`.
- Cookie consent banner with Google Consent Mode v2: the default state denies `ad_storage`, `ad_user_data`, `ad_personalization` and `analytics_storage` before any tag loads. Accept / Reject / Customise updates consent via `gtag('consent', 'update', ...)` and stores the choice in the `hwj_cookie_consent` cookie for 12 months. `url_passthrough` is enabled so gclid attribution survives without cookies; `wait_for_update: 500`.
- Phone number 07926 517296 appears as visible text (header, hero, contact section, footer and book page) as `tel:+447926517296` tap-to-call links.
- "Book online" buttons link to `/book` from the menu, hero, contact section, footer, thanks page and 404 page.
- "Get a quote" buttons (all four service cards and the 404 page) link straight to the booking system at `https://hwj-valets.vercel.app/book`.
- `/book` is served by `book.html` at the repo root, so the URL is exactly `https://hwjvalets.co.uk/book` with no redirect. It is the ad landing page on the business's own domain and hands visitors off to the booking system at `https://hwj-valets.vercel.app/book`, carrying the gclid and any hash tag through. The tag after `#` (e.g. `/book#deep.google-ads`) and any `?gclid=...` before it both stay available to page scripts (`location.hash` / `location.search`); the page shows the detected tag on screen.
- Mobile speed: referenced JPEGs re-encoded (quality 80, metadata stripped), `width`/`height` attributes added to images, hero and gallery images lazy-loaded.

## Known gaps / TODO

- Analytics: Google Tag Manager with Google Consent Mode v2 is now installed on every page, plus the cookie consent banner described above. The container ID is `GTM-KP9CNRDW`. Visitor counting also uses cookieless Cloudflare Web Analytics.
- Booking system: runs on Vercel at `https://hwj-valets.vercel.app/book`. `book.html` at `/book` is the landing page that hands off to it (carrying gclid + hash). If the booking system should move onto hwjvalets.co.uk itself, send the booking files and it can be wired up here instead.
- More real job photos, such as extra before/after sets, exterior details and vans, would strengthen the gallery over time.

## Local preview

```bash
python3 -m http.server 8000
```

## Deploy

GitHub Pages should deploy from `main`. The `CNAME` file is present for `hwjvalets.co.uk`; keep the custom domain and HTTPS configuration enabled in GitHub Pages.
