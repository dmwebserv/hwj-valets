# HWJ Valets

Marketing website for HWJ Valets, a mobile car valeting and detailing business based in Colchester, covering Essex and parts of Suffolk.

Static HTML/CSS site, no build step or framework. Pages:

- `index.html`: homepage with services, gallery, about, contact details and enquiry form
- `privacy-policy.html`: privacy information for enquiries and analytics
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

## Known gaps / TODO

- Replace the placeholder Google Analytics measurement ID in `analytics.js` once the GA4 property is ready.
- More real job photos, such as extra before/after sets, exterior details and vans, would strengthen the gallery over time.

## Local preview

```bash
python3 -m http.server 8000
```

## Deploy

GitHub Pages should deploy from `main`. The `CNAME` file is present for `hwjvalets.co.uk`; keep the custom domain and HTTPS configuration enabled in GitHub Pages.
