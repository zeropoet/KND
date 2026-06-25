# KND

[View the live site](https://zeropoet.github.io/KND/)

KND is a modern lifestyle brand making kindness visible, wearable, and culturally relevant.

This repository is one unified static site for the current KND direction. The experience moves through one shared navigation system across the homepage, Apparel, Kids, Sports, Brand, and Shop. Each page carries the same smile-led identity, warm editorial tone, product-in-life imagery, and practical commerce foundation.

## Site Map

- `index.html` - homepage and primary brand story.
- `apparel.html` - everyday product direction, apparel opportunities, and product-in-scene photography.
- `kids.html` - KND Kids product direction, softer mark language, colorways, and size range.
- `sports.html` - team, club, event, and community sports direction.
- `brand-direction.html` - logo system, smile lockup, brand principles, and visual references.
- `shop.html` - product moments, catalog filters, bundles, operations, and ledger preview.
- `404.html` - branded static-hosting not-found page.

## Direction

KND should feel clear at first glance and warmer the longer someone sits with it. The brand is not built around explaining kindness. It gives kindness a visible shape people can wear, share, recognize, and join.

The current site emphasizes:

- Lifestyle first, with product shown inside real apparel, kids, and sports moments.
- A simple smile-led mark system with enough warmth to feel human.
- Editorial pacing, generous photography, and restrained type.
- A shop surface that feels simple to browse while staying flexible behind the scenes.
- Consumer- and partner-facing language, not presentation notes.

## Brand System

The KND identity stays direct, architectural, and type-led. The square-period mark anchors the navigation and gives the site a clear brand read from the first touchpoint.

Supporting expressions include:

- `KND` wordmark.
- `KND.` square-period mark.
- KND smile lockup.
- `Kindness Wins` smile lockup.
- KND Kids softened marks and colorways.
- Sports and team-color product moments.

KND Kids can soften palette, corners, and punctuation while preserving the core KND structure. Sports can carry more energy and team color while keeping the brand center intact.

## Visual Language

Use:

- Warm cream ground.
- Restrained black and charcoal type.
- Serif display moments balanced by clean sans-serif utility text.
- Documentary-feeling photography in real environments.
- Product visible in use, not only isolated on a table.
- Group scenes where people feel included and no one is singled out.
- Open layouts that give imagery and statements room to breathe.
- Subtle product and logo framing when a panel needs definition.

Avoid:

- Copy that sounds like internal presentation notes instead of future-facing brand language.
- Over-explaining the mission.
- Heavy decorative effects.
- Photo captions.
- Product imagery that feels unfinished, cropped awkwardly, or disconnected from apparel, kids, and sports.

## Shop Data

The shop is data-driven so product decisions can stay flexible until launch details are final.

- Edit product cards, variants, pricing placeholders, product imagery, availability, and bundles in `data/catalog.json`.
- Edit checkout behavior, cart/order contracts, commerce adapters, and launch phases in `data/commerce.json`.
- Edit drops, inventory pools, product ledger records, attestation, fulfillment states, and account modeling in `data/operations.json`.
- `scripts/shop.js` renders the shop from those JSON sources.
- Use `visibility: "public"` for visible products and bundles.
- Use `visibility: "hidden"` to keep an item out of the public interface.
- Use commerce modes to keep purchase behavior reconfigurable: `concept`, `request`, `reserve`, `checkout`, or `hidden`.
- Keep product IDs stable once shared externally.

## Assets

Active source artwork lives in `assets/`. Generated responsive variants live in `assets/responsive/`.

- Source images should stay current and production-relevant.
- Do not keep old visual directions in the active source tree.
- Treat generated shop product imagery as concept assets until final product, manufacturing, and brand-specific details are locked.
- Preserve warm cream backgrounds where product images need a field.
- Prefer group scenes where KND products are worn, held, carried, or used naturally.
- Keep KND letter spacing consistent across SVG identities and lockups.

## Image Performance

Production pages use generated AVIF, WebP, and JPEG variants for large PNG artwork.

- Run `scripts/generate-image-variants.py` after adding or replacing PNG artwork.
- Run `scripts/apply-responsive-images.py` after regenerating variants to refresh page markup.
- The generated manifest lives at `assets/responsive/manifest.json`.
- Above-the-fold images are preloaded and eager-loaded.
- Lower page imagery is lazy-loaded.
- Product images rendered from `data/catalog.json` use the same responsive manifest through `scripts/shop.js`.

## Production Metadata

The site includes basic launch metadata and crawler files.

- `robots.txt` points crawlers to `sitemap.xml`.
- `sitemap.xml` lists the public pages for the current GitHub Pages URL.
- `site.webmanifest`, `favicon.ico`, and `assets/icons/` provide browser and app icons.
- Page-level canonical URLs, Open Graph tags, Twitter card tags, and JSON-LD are applied by `scripts/apply-production-meta.py`.
- Run `scripts/generate-icons.py` after changing the core icon direction.
- Update `SITE_URL` in `scripts/apply-production-meta.py` and `sitemap.xml` if the production domain changes.

## Local Preview

This is a static site. From the project root:

```bash
python3 -m http.server 8765
```

Then open:

- `http://localhost:8765/`
- `http://localhost:8765/apparel.html`
- `http://localhost:8765/kids.html`
- `http://localhost:8765/sports.html`
- `http://localhost:8765/brand-direction.html`
- `http://localhost:8765/shop.html`
