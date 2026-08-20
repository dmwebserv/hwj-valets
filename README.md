# HWJ Valets

Marketing website for HWJ Valets, a mobile car valeting and detailing business covering Clacton, Colchester, Tendring and the surrounding areas.

Static HTML/CSS site, no build step or framework. Pages:

- `index.html` &mdash; homepage (services, gallery, about, contact/enquiry form)
- `privacy-policy.html`
- `thanks.html` &mdash; enquiry form landing page (noindex)

## Content sourced from

All copy, service packages, contact details and photos come from HWJ Valets' real Facebook page and marketing flyers (not invented):

- Business bio, phone, email, coverage area, follower/review counts: Facebook page
- Service package descriptions (Exterior Wash, Mini Valet, Deep Clean): real promotional flyers
- "Premium Detail" write-up: a real Facebook post about an Audi A5 job
- Gallery photos: real job photos, cropped out of the promotional flyers (`images/job-*.jpg`)
- Logo: supplied directly, resized into `images/logo.png` plus a generated favicon set

No prices are listed anywhere in HWJ's own materials, so none are invented here either &mdash; every package links through to a WhatsApp quote request instead, matching HWJ's existing "Call or WhatsApp to book" pattern.

## Known gaps / TODO

- **Domain**: no domain is registered yet. All canonical/OG URLs currently point at a placeholder `https://hwjvalets.co.uk` &mdash; update every `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, the JSON-LD `url`, `robots.txt` and `sitemap.xml` once a real domain is bought and a `CNAME` file is added.
- **Facebook link**: uses the share-link URL provided (`facebook.com/share/19BSMyPaAs/`) since no vanity URL was confirmed &mdash; swap for `facebook.com/HWJValets` (or whatever the real vanity handle is) once confirmed.
- **Contact form**: wired to [FormSubmit.co](https://formsubmit.co) posting to `hwjvalets@gmail.com`, same working pattern as the kcmcleaning/lwp-painting sites. FormSubmit requires a one-time confirmation click from that inbox the first time the form is submitted &mdash; make sure that happens before relying on it live.
- More real job photos (before/afters, exterior details, vans) would strengthen the gallery over time.

## Local preview

```
python3 -m http.server
```

## Deploy

Enable GitHub Pages on this repo (Settings &rarr; Pages &rarr; deploy from `main`). Add a `CNAME` file once a domain is registered.
