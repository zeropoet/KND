# KND Commerce Architecture

KND should launch with a custom headless commerce architecture.

The storefront can remain static, fast, and brand-led while product data, commerce modes, and operational records live in structured JSON. This keeps late product decisions cheap: names, imagery, colors, pricing, inventory policies, and bundle rules can change without refactoring the page.

## Decision

Use a custom data-driven storefront with modular adapters.

- Catalog source: `data/catalog.json`
- Commerce architecture: `data/commerce.json`
- Operations and provenance: `data/operations.json`
- Frontend renderer: `scripts/shop.js`
- Checkout adapter: deferred until price, tax, shipping, return, and fulfillment rules are locked
- Likely payment path: Stripe Checkout or Stripe Payment Links
- Optional CMS: add only after product operations stabilize

## Why Not Shopify First

Shopify is useful when product, inventory, fulfillment, tax, and checkout decisions are already stable. KND is not there yet. The product system is intentionally flexible, and the brand presentation matters more than a default commerce theme at this stage.

Shopify can still be considered later if operations become standard retail: fixed SKUs, fixed inventory, standard shipping, ordinary customer accounts, and conventional product pages.

## Why Not Full Custom App First

A full custom app would create backend and account complexity before the product rules are final. KND does need a custom model, but it does not yet need a heavy application surface.

The current direction gives KND the model now and lets the backend arrive only when transactions require it.

## Launch Path

1. Concept shop
   Products render from data with request and reserve actions.

2. Private drop
   Inventory pools, prices, reservations, and fulfillment rules lock for selected products.

3. Checkout
   A Stripe adapter receives cart lines and returns order events for reconciliation.

4. Accounts and provenance
   Customers can view order history, claimed units, family sizing, team stores, and attestation records.

## Data Boundary

The catalog describes what can be sold.

The commerce model describes how the customer can act.

The operations model describes what must be true after the customer acts.

Keeping those boundaries separate is what lets KND stay flexible without becoming fragile.
