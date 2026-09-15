# GA4 setup for HWJ Valets (and future sites)

## Create your reusable Google Analytics account
1. Sign in at https://analytics.google.com with the Google account the business will retain.
2. Open **Admin** (bottom-left) and create one organisation-level **Account** (for example, `DM Web Services Sites`).
3. Keep **one GA4 Property per customer/site**. Do not put unrelated sites in one property: separate properties keep reporting, access and ownership clean.
4. For HWJ Valets, create a property named `HWJ Valets`, timezone `United Kingdom`, currency `GBP`.
5. In **Data collection and modification → Data streams**, add a Web stream for `https://hwjvalets.co.uk`.
6. Copy the Measurement ID shown (it starts `G-`).
7. In `analytics.js`, replace the single `G-XXXXXXXXXX` value with that ID.

The site will then load GA4 only after a visitor accepts analytics. It records page views plus `phone_click`, `whatsapp_click`, `email_click`, and `generate_lead` events.

## Mark useful conversions
After events have appeared in GA4 (usually within 24 hours), go to **Admin → Data display → Events / Key events** and mark these as key events:
- `generate_lead`
- `phone_click`
- `whatsapp_click`

Use **Reports → Realtime** to test after accepting analytics in a private browser window. Google Tag Assistant can also verify the tag.

## Adding future sites
Create a new GA4 property and Web stream for each site, copy `analytics.js`, and change only the Measurement ID and consent text/storage key. Give each customer access to only their own property via **Property access management**.
