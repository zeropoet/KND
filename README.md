# KND v5

[View the live site](https://zeropoet.github.io/KND/)

KND is a character brand built around kindness as something lived, worn, and shared.

Version 5 expands the system from a homepage into a small brand world: apparel, sports, kids, shop, and the core brand direction all share the same smile-led identity while giving each market its own rhythm, imagery, and product logic.

The current direction keeps the original restraint, but opens it up with more warmth, joy, product presence, and Mediterranean light. The brand should be felt before it has to explain itself.

The shop is now present as a working concept layer. It gives the brand a tangible product surface while keeping the deeper product, archive, fulfillment, and account pathways ready for later decisions.

## Pages

- `index.html` - homepage and primary brand expression.
- `apparel.html` - apparel opportunities, product directions, and lifestyle photography.
- `sports.html` - sports partnership opportunities, team colorways, and product-in-scene photography.
- `kids.html` - KND Kids market direction, playful product language, colorways, sizing, and mark extensions.
- `shop.html` - shop concept system with products, descriptions, size/color/bundle options, and quiet operational readiness.
- `brand-direction.html` - logo archive, smile lockup direction, and photography archive.
- `data/catalog.json` - editable product, bundle, commerce mode, and ledger source for the shop.
- `data/commerce.json` - custom commerce architecture, checkout modes, cart contract, and launch phases.
- `data/operations.json` - drops, inventory pools, archive records, attestation states, fulfillment states, and account model.
- `scripts/shop.js` - renders the shop from the catalog source.
- `docs/commerce-architecture.md` - current commerce architecture decision.
- `docs/qa-accessibility.md` - launch QA and accessibility notes.

## Current Direction

- The KND smile remains the emotional center of the system, but it should appear with intention rather than repetition.
- The homepage now favors a cleaner editorial sequence with fewer repeated lockups.
- `KINDNESS WINS` and the square-period `KND.` appear as supporting marks in the system, with Sports carrying `KINDNESS WINS` through a product-led closing moment.
- KND Kids extends the smile system into brighter colorways, softer scale, and optimistic product language.
- The KND Shop should look simple on the surface while staying ready for product records, fulfillment states, and future customer accounts.
- Product details should stay easy to revise until late launch decisions lock. Update `data/catalog.json` first, and let the shop render from that source.
- The square-period `KND.` lockup is the upper-left navigation mark, giving the site a clear brand read from the first touchpoint.
- Photography should feel premium, coherent, joyful, communal, and naturally warm.
- Product should be visible inside photographed scenes, not only as isolated product shots.
- Page descriptions should give imagery room to breathe. Use open image space or place text above hero photography when overlays compete with the subject.
- No one should feel singled out in group photography.
- Photo captions are intentionally avoided.
- Team color can enter through sports product moments without overwhelming the charcoal-and-cream brand center.
- This is a working brand system, built to keep evolving as launch priorities become clearer.
- Product choices are intentionally flexible while launch priorities continue to sharpen.

## Brand Notes

KND should feel:

- Clear at first glance.
- Warmer the longer you sit with it.
- Easy to wear.
- Easy to give.
- Strong without becoming severe.
- Joyful without becoming loud.
- Playful without becoming chaotic.

The brand direction is not about over-explaining kindness. It is about giving recognition a place to land.

Across the brand, moments that once felt invisible should now reveal kindness.

## Brand Evolution

The main KND identity stays direct, architectural, and type-led. Born from Helvetica Neue, its square period and precise corners give the system weight, clarity, and a standard to return to.

KND Kids softens that same structure without replacing it. The palette becomes brighter and more playful, the KND corners become deliberately rounded, and the square period becomes a circle. These shifts should feel subtle but meaningful: kindness can move into a new market with more brightness, color, and softness while still being unmistakably KND.

Future launch changes should build from this idea: the brand can move with care, warmth, and subtlety without losing its center.

## Visual System

The design language uses:

- Warm cream ground.
- Restrained black and charcoal type.
- Documentary photography in real environments.
- Premium product details.
- Shop product concepts that feel calm, tangible, and easy to understand.
- Generous whitespace around logos and photography.
- Occasional color through team-inspired and kid-led capsules.
- Smile mark expressions including `KND`, `KINDNESS WINS`, kids colorways, and sports colorways.
- Kids mark expressions can soften palette, corners, and punctuation while preserving the core KND structure.
- An incognito square mark that can carry the standard without always spelling out the word.

## Asset Rules

- Archive every visual asset change in a dated folder before removing or replacing it on the live site.
- Use `assets/archive/YYYY-MM-DD/` for snapshots, with the date reflecting the site change or archive date.
- Keep current pages/styles pointed at the active production assets in `assets/`, while preserving prior visual directions in the archive for reference.
- Treat generated shop product imagery as concept assets until final product, manufacturing, and brand-specific details are locked.
- Do not show image borders from screenshots or mockups.
- Avoid visible photo captions.
- Preserve warm cream backgrounds where product images need a field.
- Prefer group scenes where KND products are worn, held, carried, or used naturally.
- Keep KND letter spacing consistent across SVG identities and lockups.

## Shop Catalog

The shop is data-driven so product decisions can stay flexible until final launch details arrive.

- Edit products, variants, availability, pricing placeholders, fulfillment rules, bundles, commerce modes, and visibility in `data/catalog.json`.
- Edit checkout mode behavior, cart/order contracts, commerce adapters, and launch phases in `data/commerce.json`.
- Edit drops, inventory pools, archive records, attestation, fulfillment states, and account/provenance modeling in `data/operations.json`.
- Use `visibility: "public"` for visible products and bundles.
- Use `visibility: "hidden"` or `visibility: "archive"` to keep an item in the source without rendering it publicly.
- Use commerce modes to keep purchase behavior reconfigurable: `concept`, `request`, `reserve`, `checkout`, `hidden`, or `archive`.
- Use `price: null` while pricing is undecided.
- Add `checkoutUrl` only when a product is ready to point at a live checkout path.
- Keep product IDs stable once shared externally, even if names, images, colors, sizes, or bundle rules change.

## Commerce Architecture

KND is using a custom headless commerce model before choosing a final checkout provider.

- The frontend remains static and brand-led.
- Product and operational truth live in structured JSON.
- Request and reserve modes can work before final checkout exists.
- Stripe Checkout or Payment Links can become the first payment adapter once prices, shipping, tax, returns, and fulfillment rules are locked.
- A CMS remains optional until content operations are too frequent for direct catalog edits.
- The architecture decision is documented in `docs/commerce-architecture.md`.

## Image Performance

Production pages use generated responsive image variants for large PNG artwork.

- Source artwork remains in `assets/*.png`.
- Generated AVIF, WebP, and JPEG variants live in `assets/responsive/`.
- The generated manifest lives at `assets/responsive/manifest.json`.
- Run `scripts/generate-image-variants.py` after adding or replacing PNG artwork.
- Run `scripts/apply-responsive-images.py` after regenerating variants to refresh page markup.
- Above-the-fold images are preloaded and eager-loaded; lower page imagery is lazy-loaded.
- Product images rendered from `data/catalog.json` use the same responsive manifest through `scripts/shop.js`.

## Production Metadata

The site includes basic launch metadata and crawler files.

- `robots.txt` points crawlers to `sitemap.xml`.
- `sitemap.xml` lists the public pages for the current GitHub Pages URL.
- `site.webmanifest`, `favicon.ico`, and `assets/icons/` provide browser and app icons.
- `404.html` is the branded not-found page for static hosting.
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
- `http://localhost:8765/sports.html`
- `http://localhost:8765/kids.html`
- `http://localhost:8765/shop.html`
- `http://localhost:8765/brand-direction.html`
