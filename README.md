# BlockParty

Brooklyn block-party equipment rentals. Source repo for blockpartysupply.co.

## Site

Static marketing site, generated from `tools/site-generator/build.py`. The repo root
is the publishable output (plain HTML/CSS, no build step required to deploy) —
point any static host (GitHub Pages, Netlify, etc.) at the repo root, branch `main`.

Pages:

- `index.html` — homepage
- `about.html` — origin story / About
- `how-it-works.html` — 3-step process
- `rentals/index.html` — packages & full catalog
- `rentals/*.html` — six individual rental item pages (cornhole, giant Jenga,
  human beer pong, slushie machine, basketball hoop, ball pit)
- `faq.html` — FAQ (FAQPage JSON-LD)
- `404.html`

Structured data: `LocalBusiness` on the homepage, `Service` + `FAQPage` JSON-LD
on each rental item page, `FAQPage` JSON-LD on `faq.html`, `ItemList` on the
catalog page.

## Regenerating the site

Source content, templates, and styling live under `tools/site-generator/`.
To rebuild after a content change:

```bash
cd tools/site-generator
python3 build.py
cp -r dist/. ../../
```

Pricing and package contents are sourced from the project's final pricing
and copy documents — do not hand-edit prices in the generated HTML; edit
`tools/site-generator/build.py` and regenerate.
