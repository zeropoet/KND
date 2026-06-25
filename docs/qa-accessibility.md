# QA And Accessibility Notes

Last local pass: June 13, 2026.

## Implemented

- Added skip links on every page.
- Added `main#main-content` targets with `tabindex="-1"` for reliable skip-link landing.
- Added global `:focus-visible` styling.
- Added reduced-motion handling for users who prefer less motion.
- Improved secondary text contrast by darkening the `stone` token.
- Improved accent text contrast by darkening the `joy-rose` token.
- Added a subtle Kids hero overlay to improve text contrast over photography.
- Added product and bundle names to commerce action accessible labels.

## Local Audit Results

Custom browser audit covered:

- `index.html`
- `apparel.html`
- `kids.html`
- `sports.html`
- `brand-direction.html`
- `shop.html`
- `404.html`

Checked at mobile and desktop widths:

- One `h1` per page.
- One `main` landmark per page.
- Skip link present on every page.
- No duplicate IDs.
- No missing image alt text.
- No empty accessible links.
- No horizontal overflow.
- No catalog render errors.
- No console warnings or errors.
- Shop product action labels include product names.

## Contrast

Token contrast checks:

- `stone` on `paper`: 5.04
- `stone` on `paper-deep`: 4.58
- `joy-rose` on `paper`: 5.60
- `joy-rose` on `paper-deep`: 5.09

## Visual Crop Review

Mobile screenshots were spot-checked for:

- Kids hero
- Shop hero
- Apparel hero
- Sports hero
- 404 page

No blocking crop issues were found.

## Launch Lighthouse Pass

Run Lighthouse after the final deployment URL and hosting headers are settled.

Recommended checks:

- Performance
- Accessibility
- Best Practices
- SEO
- Mobile viewport
- Desktop viewport

The current local environment does not include Lighthouse or axe-core.
