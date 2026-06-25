const catalogUrl = "data/catalog.json";
const commerceUrl = "data/commerce.json";
const operationsUrl = "data/operations.json";
const manifestUrl = "assets/responsive/manifest.json";

const productGrid = document.querySelector("[data-catalog-products]");
const bundleGrid = document.querySelector("[data-catalog-bundles]");
const catalogControls = document.querySelector("[data-catalog-controls]");
const catalogSummary = document.querySelector("[data-catalog-summary]");
const architecturePanel = document.querySelector("[data-commerce-architecture]");
const operationsModel = document.querySelector("[data-operations-model]");
const ledgerTable = document.querySelector("[data-catalog-ledger]");

let activeCategory = "All";
let activeCatalog = null;
let activeManifest = null;

const formatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0
});

const text = (value) => String(value ?? "");

const html = (value) =>
  text(value).replace(/[&<>"']/g, (character) => {
    const entities = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "\"": "&quot;",
      "'": "&#39;"
    };
    return entities[character];
  });

const attr = (value) => html(value);

const joinNames = (items) =>
  (items || [])
    .map((item) => (typeof item === "string" ? item : item.name))
    .filter(Boolean)
    .join(", ");

const visible = (item) => item.visibility !== "hidden" && item.visibility !== "archive";

const commerceLabel = (commerce) => {
  if (!commerce) return "Details pending";
  if (commerce.price != null) return formatter.format(commerce.price);
  return commerce.label || "Details pending";
};

const commerceClass = (commerce) => `commerce-action mode-${commerce?.mode || "concept"}`;

const priceLabel = (product) =>
  product.pricing?.amount != null
    ? formatter.format(product.pricing.amount)
    : product.pricing?.display || "Price pending";

const availabilityLabel = (item) =>
  item.availability?.label || item.availability?.state || "Availability pending";

const srcset = (entry, extension) =>
  entry?.variants?.[extension]
    ?.map((variant) => `${variant.src} ${variant.width}w`)
    .join(", ");

const renderImage = (image, manifest) => {
  const imageStyle = image?.position ? ` style="object-position: ${attr(image.position)}"` : "";
  const entry = manifest?.[image?.src];
  if (!entry) {
    return `<img src="${attr(image?.src)}" alt="${attr(image?.alt)}" loading="lazy" decoding="async"${imageStyle}>`;
  }

  const jpg = entry.variants.jpg.at(-1).src;
  return `
    <picture>
      <source type="image/avif" srcset="${attr(srcset(entry, "avif"))}" sizes="(max-width: 860px) 100vw, 33vw">
      <source type="image/webp" srcset="${attr(srcset(entry, "webp"))}" sizes="(max-width: 860px) 100vw, 33vw">
      <img src="${attr(jpg)}" srcset="${attr(srcset(entry, "jpg"))}" sizes="(max-width: 860px) 100vw, 33vw" width="${attr(entry.width)}" height="${attr(entry.height)}" alt="${attr(image?.alt)}" loading="lazy" decoding="async" data-original-src="${attr(image?.src)}"${imageStyle}>
    </picture>
  `;
};

const renderColorOptions = (colors) => {
  if (!colors?.length) return "";

  return `
    <div class="option-row" aria-label="Color options">
      ${colors
        .map(
          (color) => `
            <span class="swatch" style="--swatch: ${attr(color.value)}" title="${attr(color.name)}">
              <span class="visually-hidden">${html(color.name)}</span>
            </span>
          `
        )
        .join("")}
    </div>
  `;
};

const renderSizeOptions = (sizes) => {
  if (!sizes?.length) return "";

  return `
    <div class="size-row" aria-label="Size options">
      ${sizes.map((size) => `<span>${html(size)}</span>`).join("")}
    </div>
  `;
};

const renderVariantPreview = (product) => {
  const variants = product.variants || [];
  const colors = new Set(variants.map((variant) => variant.color));
  const sizes = new Set(variants.map((variant) => variant.size));

  return `
    <div class="variant-preview" aria-label="Variant summary">
      <span>${variants.length} variants</span>
      <span>${sizes.size} sizes</span>
      <span>${colors.size} colors</span>
    </div>
  `;
};

const renderCatalogControls = (catalog) => {
  if (!catalogControls) return;
  const categories = catalog.filters?.categories || ["All"];
  catalogControls.innerHTML = categories
    .map(
      (category) => `
        <button type="button" class="catalog-filter${category === activeCategory ? " is-active" : ""}" data-category="${attr(category)}" aria-pressed="${category === activeCategory}">
          ${html(category)}
        </button>
      `
    )
    .join("");
};

const categoryMatches = (product) =>
  activeCategory === "All" || product.category === activeCategory || product.type === activeCategory.toLowerCase();

const renderCatalogSummary = (products) => {
  if (!catalogSummary) return;
  const variantCount = products.reduce((total, product) => total + (product.variants?.length || 0), 0);
  catalogSummary.innerHTML = `
    <span>${products.length} products</span>
    <span>${variantCount} variants</span>
    <span>Everyday, family, and team moments</span>
  `;
};

const renderProduct = (product, manifest) => `
  <article class="shop-product-card" data-product-id="${attr(product.id)}">
    <figure>
      ${renderImage(product.image, manifest)}
    </figure>
    <div class="shop-product-body">
      <div>
        <p class="product-code">${html(product.id)}</p>
        <h3>${html(product.name)}</h3>
        <p>${html(product.summary)}</p>
        ${renderVariantPreview(product)}
      </div>
      <dl class="product-meta">
        <div>
          <dt>Status</dt>
          <dd>${html(product.status)}</dd>
        </div>
        <div>
          <dt>Availability</dt>
          <dd>${html(availabilityLabel(product))}</dd>
        </div>
        <div>
          <dt>Price</dt>
          <dd>${html(priceLabel(product))}</dd>
        </div>
        <div>
          <dt>Sizes</dt>
          <dd>${html(joinNames(product.options?.sizes))}</dd>
        </div>
        <div>
          <dt>Colors</dt>
          <dd>${html(joinNames(product.options?.colors))}</dd>
        </div>
        <div>
          <dt>Bundles</dt>
          <dd>${html(joinNames(product.options?.bundles))}</dd>
        </div>
        <div>
          <dt>Mark</dt>
          <dd>${html(product.mark?.treatment || "Exact SVG source")}</dd>
        </div>
      </dl>
      <div class="commerce-row">
        ${renderColorOptions(product.options?.colors)}
        ${renderSizeOptions(product.options?.sizes)}
        <a class="${commerceClass(product.commerce)}" href="${attr(product.commerce?.checkoutUrl || "#ops-title")}" data-commerce-mode="${attr(product.commerce?.mode)}" aria-label="${attr(`${commerceLabel(product.commerce)} for ${product.name}`)}">
          ${html(commerceLabel(product.commerce))}
        </a>
      </div>
    </div>
  </article>
`;

const renderProducts = () => {
  if (!activeCatalog || !activeManifest) return;
  const products = activeCatalog.products.filter(visible).filter(categoryMatches);
  productGrid.innerHTML = products.map((product) => renderProduct(product, activeManifest)).join("");
  renderCatalogControls(activeCatalog);
  renderCatalogSummary(products);
};

const renderBundle = (bundle) => `
  <article data-bundle-id="${attr(bundle.id)}">
    <p class="product-code">${html(bundle.id)}</p>
    <h3>${html(bundle.name)}</h3>
    <p>${html(bundle.summary)}</p>
    <p class="bundle-state">${html(availabilityLabel(bundle))}</p>
    <a class="${commerceClass(bundle.commerce)}" href="#ops-title" data-commerce-mode="${attr(bundle.commerce?.mode)}" aria-label="${attr(`${commerceLabel(bundle.commerce)} for ${bundle.name}`)}">
      ${html(commerceLabel(bundle.commerce))}
    </a>
  </article>
`;

const renderArchitecture = (commerce) => {
  const layers = commerce.layers
    .map(
      (layer) => `
        <article>
          <span class="ops-label">${html(layer.state)}</span>
          <h3>${html(layer.label)}</h3>
          <p>${html(layer.purpose)}</p>
          <p class="architecture-surface">${html(layer.surface)}</p>
        </article>
      `
    )
    .join("");

  architecturePanel.innerHTML = `
    <div class="architecture-copy">
      <p class="product-code">${html(commerce.architecture.id)}</p>
      <h3>${html(commerce.architecture.name)}</h3>
      <p>${html(commerce.architecture.decision)}</p>
      <dl class="architecture-meta">
        <div>
          <dt>Current Mode</dt>
          <dd>${html(commerce.architecture.currentMode)}</dd>
        </div>
        <div>
          <dt>Checkout</dt>
          <dd>${html(commerce.architecture.futureCheckoutProvider)}</dd>
        </div>
        <div>
          <dt>CMS</dt>
          <dd>${html(commerce.architecture.futureCmsProvider)}</dd>
        </div>
      </dl>
    </div>
    <div class="architecture-grid">
      ${layers}
    </div>
  `;
};

const renderOperationsModel = (operations) => {
  operationsModel.innerHTML = operations.models
    .map(
      (model) => `
        <article>
          <span class="ops-label">${html(model.label)}</span>
          <h3>${html(model.headline)}</h3>
          <p>${html(model.body)}</p>
        </article>
      `
    )
    .join("");
};

const renderLedger = (entries) => {
  const header = `
    <div role="row" class="ledger-row ledger-head">
      <span role="columnheader">Record</span>
      <span role="columnheader">Object</span>
      <span role="columnheader">State</span>
      <span role="columnheader">Public Surface</span>
    </div>
  `;

  const rows = (entries || [])
    .map(
      (entry) => `
        <div role="row" class="ledger-row">
          <span role="cell">${html(entry.record)}</span>
          <span role="cell">${html(entry.object)}</span>
          <span role="cell">${html(entry.state)}</span>
          <span role="cell">${html(entry.surface)}</span>
        </div>
      `
    )
    .join("");

  ledgerTable.innerHTML = header + rows;
};

Promise.all([
  fetch(catalogUrl).then((response) => {
    if (!response.ok) throw new Error(`Catalog request failed: ${response.status}`);
    return response.json();
  }),
  fetch(commerceUrl).then((response) => {
    if (!response.ok) throw new Error(`Commerce request failed: ${response.status}`);
    return response.json();
  }),
  fetch(operationsUrl).then((response) => {
    if (!response.ok) throw new Error(`Operations request failed: ${response.status}`);
    return response.json();
  }),
  fetch(manifestUrl).then((response) => {
    if (!response.ok) throw new Error(`Image manifest request failed: ${response.status}`);
    return response.json();
  })
])
  .then(([catalog, commerce, operations, manifest]) => {
    activeCatalog = catalog;
    activeManifest = manifest;
    renderProducts();
    bundleGrid.innerHTML = catalog.bundles.filter(visible).map(renderBundle).join("");
    renderArchitecture(commerce);
    renderOperationsModel(operations);
    renderLedger(operations.archiveRecords || catalog.ledgerPreview);
  })
  .catch((error) => {
    console.error(error);
    document.documentElement.classList.add("catalog-error");
  });

catalogControls?.addEventListener("click", (event) => {
  if (!(event.target instanceof Element)) return;
  const button = event.target.closest("[data-category]");
  if (!button) return;
  activeCategory = button.dataset.category || "All";
  renderProducts();
});
