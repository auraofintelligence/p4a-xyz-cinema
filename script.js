const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
navToggle?.addEventListener('click', () => {
  const open = nav?.classList.toggle('is-open') ?? false;
  navToggle.setAttribute('aria-expanded', String(open));
});

const reveals = document.querySelectorAll('.reveal');
const showReveal = (el) => el.classList.add('is-visible');

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      showReveal(entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0, rootMargin: '0px 0px -6% 0px' });
  reveals.forEach((el) => observer.observe(el));
} else {
  reveals.forEach(showReveal);
}

const normaliseNavPath = (value) => {
  const url = new URL(value, location.href);
  return url.pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
};
const path = normaliseNavPath(location.href);
document.querySelectorAll('[data-nav] a').forEach((link) => {
  const href = link.getAttribute('href');
  if (!href || href.includes('#')) return;
  if (normaliseNavPath(href) === path) link.setAttribute('aria-current', 'page');
});

if (document.body?.dataset.page === 'site-map') {
  document.querySelectorAll('.map-jump a[href^="#"], .hero-actions a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const hash = link.getAttribute('href');
      if (!hash || hash === '#') return;
      const target = document.getElementById(hash.slice(1));
      if (!target) return;
      event.preventDefault();
      history.pushState(null, '', hash);
      const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    });
  });
}

document.querySelectorAll('a[href]').forEach((link) => {
  const href = link.getAttribute('href');
  if (!href) return;

  let url;
  try {
    url = new URL(href, location.href);
  } catch {
    return;
  }

  const isWebLink = url.protocol === 'http:' || url.protocol === 'https:';
  if (!isWebLink) return;

  const isSameOrigin = url.origin === location.origin;
  const currentPathParts = location.pathname.split('/').filter(Boolean);
  const targetPathParts = url.pathname.split('/').filter(Boolean);
  const currentRepo = location.hostname.endsWith('github.io') ? currentPathParts[0] : '';
  const leavesCurrentGithubRepo = Boolean(
    currentRepo &&
    isSameOrigin &&
    targetPathParts[0] &&
    targetPathParts[0] !== currentRepo
  );
  if (isSameOrigin && !leavesCurrentGithubRepo) return;

  link.setAttribute('target', '_blank');
  const rel = new Set((link.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
  rel.add('noopener');
  rel.add('noreferrer');
  link.setAttribute('rel', Array.from(rel).join(' '));
});

const ausPostCalculatorUrl = 'https://auspost.com.au/parcels-mail/calculate-postage-delivery-times/#/';
const fulfilmentOptions = {
  pickup_dunwich: {
    label: 'Pickup - Dunwich / Minjerribah',
    provider: 'local_pickup',
    originPostcode: '4183',
    originLabel: 'Dunwich, North Stradbroke Island / Minjerribah',
    shippingMode: 'pickup',
    note: 'Pickup from Dunwich local printer. Shipping is not charged in this demo.'
  },
  ship_from_dunwich: {
    label: 'Post from Dunwich printer',
    provider: 'auspost_api_planned',
    originPostcode: '4183',
    originLabel: 'Dunwich, North Stradbroke Island / Minjerribah',
    shippingMode: 'postage',
    note: 'Postage should be calculated from Dunwich 4183 using Australia Post PAC API once keys are configured.'
  },
  local_handoff: {
    label: 'Local branch handoff / quote',
    provider: 'branch_handoff_quote',
    originPostcode: '4183',
    originLabel: 'Dunwich, North Stradbroke Island / Minjerribah',
    shippingMode: 'quote',
    note: 'Branch or volunteer kit fulfilment should be quoted manually with the organiser.'
  }
};
const supplierCollectionUrls = {
  Purple: 'https://www.thetshirtmill.com.au/create?c=3097422&color=37,-7',
  Lavender: 'https://www.thetshirtmill.com.au/create?c=3097422&color=27,-7'
};
const discountTiers = [
  { min: 1, rate: 0, label: '1-4 items', note: 'single price' },
  { min: 5, rate: 0.05, label: '5+ items', note: '5% off' },
  { min: 10, rate: 0.10, label: '10+ items', note: '10% off' },
  { min: 20, rate: 0.15, label: '20+ items', note: '15% off' },
  { min: 30, rate: 0.20, label: '30+ items', note: '20% off' },
  { min: 50, rate: 0.25, label: '50+ items', note: '25% floor' }
];

const gildanSizeGuide = [
  { size: 'XS', width: '', length: '', sleeve: '' },
  { size: 'S', width: '51', length: '69', sleeve: '85' },
  { size: 'M', width: '56', length: '71', sleeve: '88' },
  { size: 'L', width: '61', length: '74', sleeve: '90' },
  { size: 'XL', width: '66', length: '76', sleeve: '93' },
  { size: '2XL', width: '71', length: '79', sleeve: '95' },
  { size: '3XL', width: '76', length: '81', sleeve: '98' },
  { size: '4XL', width: '81', length: '84', sleeve: '100' },
  { size: '5XL', width: '86', length: '86', sleeve: '103' }
];

const gearProducts = [
  {
    id: 'gildan-adult-hooded-sweatshirt',
    label: 'Gildan Adult Hooded Sweatshirt',
    supplierProductId: '306598281',
    supplierProductCode: '',
    supplierUrl: 'https://www.thetshirtmill.com.au/blank_product/306598281/Adult-Hooded-Sweatshirt?c=3097422',
    manufacturer: 'GILDAN',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 52.95,
    floorPrice: 39.71,
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    variants: [{ label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#5a3380', image: '../assets/gear-products/gildan-adult-hoodie.webp' }],
    sizeGuide: gildanSizeGuide,
    sizeGuideNote: 'Supplier Gildan size guide captured from product page; blank cells were not visible in the screenshot.',
    note: 'Lowest starting cost, classic pullover fit.'
  },
  {
    id: 'ramo-adult-poly-cotton-fleece-sloppy-joe',
    label: 'RAMO Adult Poly Cotton Fleece Sloppy Joe',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 57.45,
    floorPrice: 43.09,
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    variants: [
      { label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#5f159d', image: '../assets/gear-products/ramo-sloppy-joe.webp' },
      { label: 'Lavender', supplierColourName: 'Lavender', supplierColourFilter: '27', hex: '#c6a7f0', image: '../assets/gear-products/lavender-sloppy-joe.webp' }
    ],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Crewneck option for lighter purple deployment gear.'
  },
  {
    id: 'unisex-adults-pull-over-hoodie',
    label: 'Unisex Adults Pull Over Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Purple,
    manufacturer: '',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 59.99,
    floorPrice: 44.99,
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '7XL'],
    variants: [{ label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#482071', image: '../assets/gear-products/unisex-pullover.webp' }],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Wide size range, good one-at-a-time test base.'
  },
  {
    id: 'ramo-mens-kangaroo-pocket-hoodie',
    label: 'RAMO Mens Kangaroo Pocket Hoodie',
    supplierProductId: '277286481',
    supplierProductCode: 'TP212H',
    supplierUrl: 'https://www.thetshirtmill.com.au/blank_product/277286481/Mens-Kangaroo-Pocket-Hoodies?c=3097422',
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 62.35,
    floorPrice: 46.76,
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL'],
    variants: [
      { label: 'Purple', supplierColourName: 'Grape', supplierColourFilter: '-7', hex: '#650ca0', image: '../assets/gear-products/ramo-kangaroo-pocket-grape-front.webp' },
      { label: 'Lavender', supplierColourName: 'Lavender', supplierColourFilter: '27', hex: '#c6a7f0', image: '../assets/gear-products/ramo-kangaroo-pocket-lavender-front.webp' }
    ],
    sizeGuide: {
      sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL'],
      measurements: [
        { label: 'Half Chest (cm)', values: { S: '59', M: '61', L: '63', XL: '65', '2XL': '67', '3XL': '69', '4XL': '71', '5XL': '73', '6XL': '75', '7XL': '77' } }
      ]
    },
    sizeGuideNote: 'RAMO TP212H supplier page captured on 6 May 2026. Purple storefront option maps to supplier colour Grape.',
    note: 'RAMO TP212H. Purple maps to supplier Grape; Lavender is also verified.'
  },
  {
    id: 'ramo-mens-brushed-heavy-zip-fleece-hoodie',
    label: 'RAMO Mens Brushed Heavy Zip Fleece Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 65.00,
    floorPrice: 48.75,
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    variants: [{ label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#522188', image: '../assets/gear-products/ramo-heavy-zip.webp' }],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Zip option for people who hate pullovers.'
  },
  {
    id: 'ramo-mens-zip-hoodie-with-pocket',
    label: 'RAMO Mens Zip Hoodie with Pocket',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 77.20,
    floorPrice: 57.90,
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL'],
    variants: [
      { label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#501c8d', image: '../assets/gear-products/ramo-zip-pocket.webp' },
      { label: 'Lavender', supplierColourName: 'Lavender', supplierColourFilter: '27', hex: '#c6a7f0', image: '../assets/gear-products/lavender-zip-pocket.webp' }
    ],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Higher-cost zip hoodie, still purple-family.'
  },
  {
    id: 'ramo-mens-brushed-heavy-fleece-hoodie',
    label: 'RAMO Mens Brushed Heavy Fleece Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 82.39,
    floorPrice: 61.79,
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    variants: [{ label: 'Purple', supplierColourName: 'Purple', supplierColourFilter: '-7', hex: '#50208b', image: '../assets/gear-products/ramo-heavy-fleece.webp' }],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Premium heavy fleece test option.'
  },
  {
    id: 'comfort-colors-color-blast-crewneck',
    label: 'Comfort Colors Color Blast Crewneck',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: supplierCollectionUrls.Lavender,
    manufacturer: 'COMFORT COLORS',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    singlePrice: 100.71,
    floorPrice: 75.53,
    sizes: ['S', 'M', 'L', 'XL', '2XL'],
    variants: [{ label: 'Lavender', supplierColourName: 'Lavender', supplierColourFilter: '27', hex: '#b9a9ef', image: '../assets/gear-products/comfort-colorblast.webp' }],
    sizeGuide: null,
    sizeGuideNote: 'Available sizes captured from supplier card. Measurement table still needs supplier verification.',
    note: 'Expensive lavender crewneck, only if the market asks.'
  }
];

document.querySelectorAll('[data-gear-order]').forEach((form) => {
  const product = form.querySelector('[data-gear-product]');
  const colour = form.querySelector('[data-gear-colour]');
  const size = form.querySelector('[data-gear-size]');
  const quantity = form.querySelector('[data-gear-quantity]');
  const shipping = form.querySelector('[data-gear-shipping]');
  const orderMode = form.querySelector('[data-gear-order-mode]');
  const fulfilment = form.querySelector('[data-gear-fulfilment]');
  const support = form.querySelector('[data-gear-support]');
  const style = form.querySelector('[data-gear-style]');
  const buyerName = form.querySelector('[data-gear-name]');
  const buyerEmail = form.querySelector('[data-gear-email]');
  const postcode = form.querySelector('[data-gear-postcode]');
  const shippingNote = form.querySelector('[data-shipping-note]');
  const bulkFields = form.querySelector('[data-bulk-fields]');
  const branchName = form.querySelector('[data-gear-branch-name]');
  const volunteerCount = form.querySelector('[data-gear-volunteers]');
  const addonInputs = form.querySelectorAll('[data-gear-addon]');
  const bulkNotes = form.querySelector('[data-gear-bulk-notes]');
  const summary = form.querySelector('[data-gear-summary]');
  const mail = form.querySelector('[data-gear-mail]');
  const preview = form.querySelector('[data-order-preview]');
  const demoCheckout = form.querySelector('[data-demo-checkout]');
  const shelf = document.querySelector('[data-product-shelf]');
  const selectedImage = document.querySelector('[data-selected-image]');
  const selectedTitle = document.querySelector('[data-selected-title]');
  const selectedNote = document.querySelector('[data-selected-note]');
  const selectedCost = document.querySelector('[data-selected-cost]');
  const selectedFloor = document.querySelector('[data-selected-floor]');
  const summaryTotal = document.querySelector('[data-summary-total]');
  const sizeGuide = document.querySelector('[data-size-guide]');
  const sizeGuideNote = document.querySelector('[data-size-guide-note]');
  const colourButtons = document.querySelector('[data-colour-buttons]');
  const colourStatus = document.querySelector('[data-colour-status]');
  const presetButtons = form.querySelectorAll('[data-support-preset]');
  const dollars = new Intl.NumberFormat('en-AU', { style: 'currency', currency: 'AUD' });
  const storeColours = Array.from(new Map(gearProducts.flatMap((item) => item.variants).map((variant) => [variant.label, { label: variant.label, hex: variant.hex, supplierCollectionUrl: supplierCollectionUrls[variant.label] || '' }])).values());
  let activeShelfColour = storeColours[0]?.label || 'Purple';
  const cardColourChoices = new Map();

  const roundMoney = (value) => Number((Math.round((Number(value) + Number.EPSILON) * 100) / 100).toFixed(2));

  const getDiscountTier = (qty) => discountTiers.reduce((active, tier) => qty >= tier.min ? tier : active, discountTiers[0]);

  const getSelectedProduct = () => gearProducts.find((item) => item.id === product?.value) || gearProducts[0];

  const getVariantForColour = (item, colourLabel) => item.variants.find((variant) => variant.label === colourLabel);

  const getSelectedVariant = () => {
    const selected = getSelectedProduct();
    return selected.variants.find((item) => item.label === colour?.value) || selected.variants[0];
  };

  const getCardDisplayVariant = (item) => {
    const localChoice = cardColourChoices.get(item.id);
    return getVariantForColour(item, localChoice) || getVariantForColour(item, activeShelfColour) || item.variants[0];
  };

  const populateProductSelect = () => {
    if (!product) return;
    product.innerHTML = gearProducts.map((item) => `<option value="${item.id}">${item.label}</option>`).join('');
  };

  const populateDependentSelects = (preferredColour = activeShelfColour) => {
    const selected = getSelectedProduct();
    if (colour) {
      const currentColour = preferredColour || colour.value;
      colour.innerHTML = selected.variants.map((variant) => `<option value="${variant.label}">${variant.label}</option>`).join('');
      colour.value = selected.variants.some((variant) => variant.label === currentColour) ? currentColour : selected.variants[0].label;
    }
    if (size) {
      const currentSize = size.value;
      size.innerHTML = selected.sizes.map((item) => `<option>${item}</option>`).join('');
      size.value = selected.sizes.includes(currentSize) ? currentSize : selected.sizes[Math.min(2, selected.sizes.length - 1)];
    }
  };

  const updateColourButtonState = () => {
    colourButtons?.querySelectorAll('[data-colour-choice]').forEach((button) => {
      const active = button.getAttribute('data-colour-choice') === activeShelfColour;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
  };

  const renderColourButtons = () => {
    if (!colourButtons) return;
    colourButtons.innerHTML = storeColours.map((variant) => `<button class="colour-choice" type="button" data-colour-choice="${variant.label}" style="--colour: ${variant.hex}" aria-pressed="${variant.label === activeShelfColour ? 'true' : 'false'}">${variant.label}</button>`).join('');
    colourButtons.querySelectorAll('[data-colour-choice]').forEach((button) => {
      button.addEventListener('click', () => {
        const nextColour = button.getAttribute('data-colour-choice') || activeShelfColour;
        activeShelfColour = nextColour;
        gearProducts.forEach((item) => {
          if (getVariantForColour(item, nextColour)) cardColourChoices.set(item.id, nextColour);
        });
        const selected = getSelectedProduct();
        if (!getVariantForColour(selected, nextColour)) {
          const nextProduct = gearProducts.find((item) => getVariantForColour(item, nextColour));
          if (nextProduct && product) product.value = nextProduct.id;
        }
        populateDependentSelects(nextColour);
        renderShelf();
        updateSummary();
      });
    });
    updateColourButtonState();
  };

  const renderShelf = () => {
    if (!shelf) return;
    const visibleProducts = gearProducts.filter((item) => getVariantForColour(item, activeShelfColour));
    if (colourStatus) {
      const productWord = visibleProducts.length === 1 ? 'base' : 'bases';
      colourStatus.textContent = `Showing ${visibleProducts.length} ${activeShelfColour.toLowerCase()} ${productWord} with verified supplier images. Product colour buttons are selectable, not decorative.`;
    }
    shelf.innerHTML = visibleProducts.map((item) => {
      const activeVariant = getCardDisplayVariant(item);
      const selected = getSelectedProduct().id === item.id && getSelectedVariant().label === activeVariant.label;
      const variantButtons = item.variants.map((variant) => {
        const variantSelected = activeVariant.label === variant.label;
        const supplierText = variant.supplierColourName && variant.supplierColourName !== variant.label ? `Supplier: ${variant.supplierColourName}` : `Supplier: ${variant.label}`;
        return `<button class="product-colour-option${variantSelected ? ' is-active' : ''}" type="button" data-product-card="${item.id}" data-product-card-colour="${variant.label}" style="--colour: ${variant.hex}" aria-pressed="${variantSelected ? 'true' : 'false'}" title="${supplierText}">${variant.label}</button>`;
      }).join('');
      return `<article class="product-card${selected ? ' is-selected' : ''}" data-product-card-shell="${item.id}">
        <button class="product-card-main" type="button" data-product-card="${item.id}" data-product-card-colour="${activeVariant.label}" aria-pressed="${selected ? 'true' : 'false'}">
          <img src="${activeVariant.image}" alt="${activeVariant.label} ${item.label}">
          <strong>${item.label}</strong>
          <small>${dollars.format(item.singlePrice)} single / ${dollars.format(item.floorPrice)} 50+ floor</small>
        </button>
        <div class="verified-colours" aria-label="Verified selectable colours">${variantButtons}</div>
      </article>`;
    }).join('');
  };

  const renderSizeGuide = () => {
    const selected = getSelectedProduct();
    if (sizeGuideNote) sizeGuideNote.textContent = selected.sizeGuideNote;
    if (!sizeGuide) return;

    if (!selected.sizeGuide) {
      sizeGuide.innerHTML = `<div class="available-sizes">${selected.sizes.map((item) => `<span>${item}</span>`).join('')}</div>`;
      return;
    }

    if (Array.isArray(selected.sizeGuide)) {
      sizeGuide.innerHTML = `<table>
        <thead><tr><th>Size</th>${selected.sizeGuide.map((row) => `<th>${row.size}</th>`).join('')}</tr></thead>
        <tbody>
          <tr><th>Width</th>${selected.sizeGuide.map((row) => `<td>${row.width || '-'}</td>`).join('')}</tr>
          <tr><th>Length</th>${selected.sizeGuide.map((row) => `<td>${row.length || '-'}</td>`).join('')}</tr>
          <tr><th>Sleeve</th>${selected.sizeGuide.map((row) => `<td>${row.sleeve || '-'}</td>`).join('')}</tr>
        </tbody>
      </table>`;
      return;
    }

    const guideSizes = selected.sizeGuide.sizes || selected.sizes;
    const measurements = selected.sizeGuide.measurements || [];
    sizeGuide.innerHTML = `<table>
      <thead><tr><th>Size</th>${guideSizes.map((item) => `<th>${item}</th>`).join('')}</tr></thead>
      <tbody>
        ${measurements.map((row) => `<tr><th>${row.label}</th>${guideSizes.map((item) => `<td>${row.values[item] || '-'}</td>`).join('')}</tr>`).join('')}
      </tbody>
    </table>`;
  };

  const updateSelectedProductDisplay = () => {
    const selected = getSelectedProduct();
    const variant = getSelectedVariant();
    const qty = Math.max(1, Number(quantity?.value || 1));
    const tier = getDiscountTier(qty);
    const unitCost = roundMoney(selected.singlePrice * (1 - tier.rate));

    if (selectedImage) {
      selectedImage.src = variant.image;
      selectedImage.alt = `${variant.label} ${selected.label}`;
    }
    if (selectedTitle) selectedTitle.textContent = selected.label;
    if (selectedNote) selectedNote.textContent = `${variant.label}. ${selected.note}`;
    if (selectedCost) selectedCost.textContent = dollars.format(unitCost);
    if (selectedFloor) selectedFloor.textContent = `${dollars.format(selected.floorPrice)} 50+ floor`;
    updateColourButtonState();
    renderSizeGuide();
  };

  const selectProduct = (id, requestedColour = activeShelfColour) => {
    const selectedProduct = gearProducts.find((item) => item.id === id) || gearProducts[0];
    const nextVariant = getVariantForColour(selectedProduct, requestedColour) || getVariantForColour(selectedProduct, activeShelfColour) || selectedProduct.variants[0];
    if (product) product.value = selectedProduct.id;
    cardColourChoices.set(selectedProduct.id, nextVariant.label);
    populateDependentSelects(nextVariant.label);
    renderColourButtons();
    renderShelf();
    updateSummary();
  };

  const getOrder = () => {
    const selected = getSelectedProduct();
    const variant = getSelectedVariant();
    const qty = Math.max(1, Number(quantity?.value || 1));
    const fulfilmentChoice = fulfilmentOptions[fulfilment?.value] || fulfilmentOptions.pickup_dunwich;
    const tier = getDiscountTier(qty);
    const unitSupplierSingle = roundMoney(selected.singlePrice);
    const unitDiscount = roundMoney(unitSupplierSingle * tier.rate);
    const unitCustomerCost = roundMoney(unitSupplierSingle - unitDiscount);
    const itemCostSubtotal = roundMoney(unitCustomerCost * qty);
    const supportPerItem = Math.max(0, Number(support?.value || 0));
    const supportTotal = roundMoney(supportPerItem * qty);
    const shippingEstimate = fulfilmentChoice.shippingMode === 'pickup' ? 0 : Math.max(0, Number(shipping?.value || 0));
    const total = roundMoney(itemCostSubtotal + supportTotal + shippingEstimate);
    const addons = Array.from(addonInputs).filter((item) => item.checked).map((item) => item.value);

    return {
      action: 'createCheckout',
      schema_version: 'p4a_gear_order_v1',
      order: {
        source: 'p4a_xyz_deployment_gear_demo',
        order_mode: orderMode?.value || 'single',
        website_product_id: selected.id,
        product_label: selected.label,
        supplier_name: 'Dunwich local shirt printer first; supplier catalogue reference',
        supplier_product_id: selected.supplierProductId,
        supplier_product_code: selected.supplierProductCode || '',
        supplier_product_url: selected.supplierUrl,
        supplier_category: selected.category,
        supplier_manufacturer: selected.manufacturer,
        supplier_process: selected.process,
        supplier_colour_label: variant.label,
        supplier_colour_name: variant.supplierColourName || variant.label,
        supplier_colour_filter: variant.supplierColourFilter,
        supplier_collection_url: supplierCollectionUrls[variant.label] || selected.supplierUrl,
        supplier_image_path: variant.image,
        size: size?.value || selected.sizes[0],
        quantity: qty,
        quantity_discount_min: tier.min,
        quantity_discount_rate: tier.rate,
        quantity_discount_label: tier.note,
        unit_supplier_single_aud: unitSupplierSingle,
        unit_discount_aud: unitDiscount,
        unit_customer_cost_aud: unitCustomerCost,
        item_cost_subtotal_aud: itemCostSubtotal,
        support_per_item_aud: roundMoney(supportPerItem),
        support_total_aud: supportTotal,
        fulfilment_method: fulfilment?.value || 'pickup_dunwich',
        fulfilment_label: fulfilmentChoice.label,
        fulfilment_origin_label: fulfilmentChoice.originLabel,
        shipping_estimate_aud: roundMoney(shippingEstimate),
        shipping_provider: fulfilmentChoice.provider,
        shipping_mode: fulfilmentChoice.shippingMode,
        shipping_origin_postcode: fulfilmentChoice.originPostcode,
        shipping_destination_postcode: postcode?.value || '',
        auspost_calculator_url: ausPostCalculatorUrl,
        auspost_api_status: fulfilmentChoice.shippingMode === 'postage' ? 'planned_pac_api' : 'not_required_for_selected_fulfilment',
        parcel_weight_kg: roundMoney(Math.max(0.5, qty * 0.75)),
        parcel_length_cm: 35,
        parcel_width_cm: 28,
        parcel_height_cm: Math.min(45, Math.max(8, qty * 6)),
        logo_style: style?.value || 'P4A chest mark',
        branch_name: branchName?.value || '',
        volunteer_count: Math.max(0, Number(volunteerCount?.value || 0)),
        addon_interest: addons,
        bulk_notes: bulkNotes?.value || '',
        buyer_name: buyerName?.value || '',
        buyer_email: buyerEmail?.value || '',
        order_total_aud: total,
        currency: 'AUD',
        fulfilment_status: 'demo_payload',
        fulfilment_note: fulfilmentChoice.note
      }
    };
  };

  const updateSummary = () => {
    const payload = getOrder();
    const order = payload.order;
    const bulkMode = order.order_mode === 'branch_bundle';
    if (bulkFields) bulkFields.hidden = !bulkMode;
    if (shipping) {
      shipping.disabled = order.shipping_mode === 'pickup';
      if (order.shipping_mode === 'pickup') shipping.value = '0';
    }
    if (shippingNote) {
      shippingNote.innerHTML = order.shipping_mode === 'pickup'
        ? 'Pickup is from Dunwich, North Stradbroke Island / Minjerribah. No postage is added for pickup.'
        : `Postage starts from Dunwich 4183. Live mode should call the Australia Post Postage Assessment Calculation API; the <a href="${ausPostCalculatorUrl}">calculator</a> stays as a fallback estimate.`;
    }
    if (summary) {
      const branchText = bulkMode ? ` Branch/bulk enquiry: ${order.branch_name || 'unnamed group'}, ${order.volunteer_count} volunteers.` : '';
      summary.textContent = `Unit after discount ${dollars.format(order.unit_customer_cost_aud)} + support/item ${dollars.format(order.support_per_item_aud)} = ${dollars.format(order.unit_customer_cost_aud + order.support_per_item_aud)} each. Quantity ${order.quantity}. ${order.fulfilment_label}. Shipping ${dollars.format(order.shipping_estimate_aud)}. Total ${dollars.format(order.order_total_aud)}.${branchText}`;
    }
    if (summaryTotal) summaryTotal.textContent = dollars.format(order.order_total_aud);
    updateSelectedProductDisplay();

    if (mail) {
      const subject = encodeURIComponent('P4A purple hoodie order');
      const body = encodeURIComponent(`Hi P4A,

I want to pilot a P4A purple hoodie order using the cost-plus-support model.

Product: ${order.product_label}
Colour: ${order.supplier_colour_label}
Supplier colour name: ${order.supplier_colour_name}
Size: ${order.size}
Quantity: ${order.quantity}
Unit supplier cost after discount: ${dollars.format(order.unit_customer_cost_aud)}
Support per item: ${dollars.format(order.support_per_item_aud)}
Fulfilment: ${order.fulfilment_label}
Shipping estimate: ${dollars.format(order.shipping_estimate_aud)}
Order mode: ${order.order_mode}
Branch/group: ${order.branch_name || '[not branch order]'}
Volunteer count: ${order.volunteer_count}
Future swag interest: ${order.addon_interest.length ? order.addon_interest.join(', ') : '[none yet]'}
Bulk notes: ${order.bulk_notes || '[none]'}
Total: ${dollars.format(order.order_total_aud)}

Name: ${order.buyer_name || '[buyer name]'}
Email: ${order.buyer_email || '[buyer email]'}
Postcode: ${order.shipping_destination_postcode || '[postcode]'}
`);
      mail.setAttribute('href', `mailto:hello@p4a.xyz?subject=${subject}&body=${body}`);
    }

    presetButtons.forEach((button) => {
      button.classList.toggle('is-active', Number(button.getAttribute('data-support-preset')) === order.support_per_item_aud);
    });
  };

  populateProductSelect();
  populateDependentSelects(activeShelfColour);
  renderColourButtons();
  renderShelf();
  shelf?.addEventListener('click', (event) => {
    const trigger = event.target.closest('[data-product-card]');
    if (!trigger) return;
    const targetProductId = trigger.getAttribute('data-product-card') || gearProducts[0].id;
    const targetColour = trigger.getAttribute('data-product-card-colour') || activeShelfColour;
    const isCardColourButton = trigger.matches('[data-product-card-colour].product-colour-option');

    if (isCardColourButton) {
      cardColourChoices.set(targetProductId, targetColour);
      if (getSelectedProduct().id === targetProductId) {
        populateDependentSelects(targetColour);
        updateSummary();
      } else {
        renderShelf();
      }
      return;
    }

    selectProduct(targetProductId, cardColourChoices.get(targetProductId) || targetColour);
  });
  presetButtons.forEach((button) => {
    button.addEventListener('click', () => {
      if (support) support.value = button.getAttribute('data-support-preset') || '0';
      updateSummary();
    });
  });
  demoCheckout?.addEventListener('click', () => {
    if (!preview) return;
    preview.textContent = JSON.stringify(getOrder(), null, 2);
    preview.classList.add('is-visible');
  });
  product?.addEventListener('change', () => selectProduct(product.value, colour?.value || activeShelfColour));
  colour?.addEventListener('input', () => {
    cardColourChoices.set(getSelectedProduct().id, colour.value);
    renderColourButtons();
    renderShelf();
    updateSummary();
  });
  [size, quantity, shipping, orderMode, fulfilment, support, style, buyerName, buyerEmail, postcode, branchName, volunteerCount, bulkNotes].forEach((input) => input?.addEventListener('input', updateSummary));
  addonInputs.forEach((input) => input.addEventListener('change', updateSummary));
  updateSummary();
});

(() => {
  const body = document.body;
  if (!body) return;

  const actions = document.createElement('nav');
  actions.className = 'floating-actions';
  actions.setAttribute('aria-label', 'Quick page links');

  const topButton = document.createElement('button');
  topButton.className = 'floating-top-button';
  topButton.type = 'button';
  topButton.textContent = 'Top';
  topButton.setAttribute('aria-label', 'Back to top');
  topButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
  actions.appendChild(topButton);
  body.appendChild(actions);

  const syncFloatingActions = () => {
    actions.classList.toggle('is-visible', window.scrollY > 220);
  };

  syncFloatingActions();
  window.addEventListener('scroll', syncFloatingActions, { passive: true });
})();

(() => {
  const countdowns = Array.from(document.querySelectorAll('[data-countdown]'));
  const timerModules = Array.from(document.querySelectorAll('[data-timer-module]'));
  const mapTargets = Array.from(document.querySelectorAll('[data-map-state]'));
  const stateTargets = Array.from(document.querySelectorAll('[data-state]'));
  if (!countdowns.length && !mapTargets.length && !stateTargets.length) return;

  const dayMs = 86400000;
  const two = (value) => String(value).padStart(2, '0');
  const isByElection = (card) => {
    const scope = (card.getAttribute('data-election-scope') || '').toLowerCase();
    const kind = (card.getAttribute('data-election-kind') || '').toLowerCase();
    return scope.includes('by-election') || kind.includes('by-election');
  };

  const getCardTime = (card) => {
    const countdown = card.querySelector('[data-countdown]');
    const rawDate = card.getAttribute('data-election-date') || countdown?.getAttribute('data-countdown') || '';
    const target = new Date(rawDate);
    const stamp = target.getTime();
    if (Number.isNaN(stamp)) {
      return { invalid: true, diff: 0, abs: 0, stamp: Number.MAX_SAFE_INTEGER, state: 'invalid' };
    }

    const diff = stamp - Date.now();
    const abs = Math.abs(diff);
    const rawSinceDate = card.getAttribute('data-days-since-date') || '';
    const sinceTarget = rawSinceDate ? new Date(rawSinceDate) : target;
    const sinceStamp = sinceTarget.getTime();
    const sinceValid = !Number.isNaN(sinceStamp);
    const sinceDiff = sinceValid ? Date.now() - sinceStamp : 0;
    const sinceAbs = sinceValid ? Math.abs(sinceDiff) : 0;
    return {
      invalid: false,
      diff,
      abs,
      stamp,
      state: diff >= 0 ? 'future' : 'past',
      sinceInvalid: !sinceValid,
      sinceDiff,
      sinceAbs,
      sinceStamp: sinceValid ? sinceStamp : Number.MAX_SAFE_INTEGER
    };
  };

  const updateCardState = (card) => {
    const info = getCardTime(card);
    card.setAttribute('data-election-time-state', info.state);
    card.setAttribute('data-election-distance', String(info.abs));
    card.setAttribute('data-election-stamp', String(info.stamp));
    card.classList.toggle('is-by-election', isByElection(card));
    return info;
  };

  const renderDayMetrics = (card, info) => {
    if (!card) return;
    const untilWrap = card.querySelector('[data-days-until-wrap]');
    const sinceWrap = card.querySelector('[data-days-since-wrap]');
    const untilValue = card.querySelector('[data-days-until]');
    const sinceValue = card.querySelector('[data-days-since]');
    if (!untilValue && !sinceValue) return;

    const daysUntilEnabled = card.getAttribute('data-days-until-enabled') !== 'false';
    const daysSinceEnabled = card.getAttribute('data-days-since-enabled') !== 'false';
    if (untilWrap) untilWrap.hidden = !daysUntilEnabled;
    if (sinceWrap) sinceWrap.hidden = !daysSinceEnabled;

    if (info.invalid) {
      if (untilValue) untilValue.textContent = 'Check';
      if (sinceValue) sinceValue.textContent = 'Check';
      return;
    }

    const elapsedDays = info.sinceInvalid ? 0 : Math.floor(info.sinceAbs / dayMs);
    const remainingDays = Math.ceil(info.abs / dayMs);
    if (untilValue) {
      untilValue.textContent = info.diff >= 0 ? String(Math.max(0, remainingDays)) : '0';
    }
    if (sinceValue) {
      sinceValue.textContent = info.sinceInvalid ? 'Check' : String(Math.max(0, info.sinceDiff >= 0 ? elapsedDays : 0));
    }
  };

  const renderCountdown = (element) => {
    const card = element.closest('[data-election-card]');
    const module = element.closest('[data-timer-module]');
    const mode = module?.getAttribute('data-timer-mode') || 'clock';
    const info = card ? updateCardState(card) : getCardTime(element);
    renderDayMetrics(card, info);

    if (info.invalid) {
      element.textContent = 'Date needs checking';
      element.setAttribute('data-countdown-state', 'invalid');
      return;
    }

    const days = Math.floor(info.abs / dayMs);
    const futureDays = Math.ceil(info.abs / dayMs);
    const hours = Math.floor((info.abs % dayMs) / 3600000);
    const minutes = Math.floor((info.abs % 3600000) / 60000);
    const seconds = Math.floor((info.abs % 60000) / 1000);

    if (mode === 'days') {
      if (info.diff >= 0) {
        element.textContent = futureDays <= 0 ? 'Today' : `${futureDays} day${futureDays === 1 ? '' : 's'} until`;
      } else {
        element.textContent = days < 1 ? 'Today' : `${days} day${days === 1 ? '' : 's'} since`;
      }
      element.setAttribute('data-countdown-state', info.state);
      return;
    }

    if (info.diff >= 0) {
      element.textContent = days < 1 ? `${two(hours)}h ${two(minutes)}m ${two(seconds)}s` : `${days}d ${two(hours)}h ${two(minutes)}m`;
      element.setAttribute('data-countdown-state', 'future');
    } else {
      element.textContent = days < 1
        ? `Held ${two(hours)}h ${two(minutes)}m ago`
        : `Held ${days}d ${two(hours)}h ago`;
      element.setAttribute('data-countdown-state', 'past');
    }
  };

  const compareNext = (a, b) => {
    const aInfo = updateCardState(a);
    const bInfo = updateCardState(b);
    const aBucket = aInfo.state === 'future' ? 0 : 1;
    const bBucket = bInfo.state === 'future' ? 0 : 1;
    if (aBucket !== bBucket) return aBucket - bBucket;
    if (aInfo.state === 'future') return aInfo.stamp - bInfo.stamp;
    return bInfo.stamp - aInfo.stamp;
  };

  const compareCards = (sortMode) => (a, b) => {
    const aInfo = updateCardState(a);
    const bInfo = updateCardState(b);

    if (sortMode === 'byelections') {
      const byDiff = Number(isByElection(b)) - Number(isByElection(a));
      if (byDiff !== 0) return byDiff;
      return compareNext(a, b);
    }

    if (sortMode === 'farthest') {
      const aBucket = aInfo.state === 'future' ? 0 : 1;
      const bBucket = bInfo.state === 'future' ? 0 : 1;
      if (aBucket !== bBucket) return aBucket - bBucket;
      return bInfo.stamp - aInfo.stamp;
    }

    if (sortMode === 'state') {
      const stateDiff = (a.getAttribute('data-state') || '').localeCompare(b.getAttribute('data-state') || '');
      if (stateDiff !== 0) return stateDiff;
      return compareNext(a, b);
    }

    if (sortMode === 'days-since') {
      const aBucket = aInfo.sinceInvalid ? 1 : 0;
      const bBucket = bInfo.sinceInvalid ? 1 : 0;
      if (aBucket !== bBucket) return aBucket - bBucket;
      return bInfo.sinceAbs - aInfo.sinceAbs;
    }

    return compareNext(a, b);
  };

  const updateModule = (module) => {
    const board = module.querySelector('[data-timer-board]');
    if (!board) return;

    const sortMode = module.querySelector('[data-timer-sort]')?.value || 'next';
    const filterMode = module.getAttribute('data-timer-filter') || 'all';
    const cards = Array.from(board.querySelectorAll('[data-election-card]'));
    cards.sort(compareCards(sortMode)).forEach((card) => board.appendChild(card));

    let visibleCount = 0;
    cards.forEach((card) => {
      const info = updateCardState(card);
      const visible = filterMode === 'all'
        || (filterMode === 'upcoming' && info.state === 'future')
        || (filterMode === 'past' && info.state === 'past')
        || (filterMode === 'since' && card.getAttribute('data-days-since-enabled') !== 'false')
        || (filterMode === 'by-election' && isByElection(card));
      card.hidden = !visible;
      card.classList.toggle('is-filtered-out', !visible);
      if (visible) visibleCount += 1;
    });

    const empty = module.querySelector('[data-timer-empty]');
    if (empty) empty.hidden = visibleCount > 0;
  };

  const setModeButtonState = (module, mode) => {
    module.setAttribute('data-timer-mode', mode);
    module.querySelectorAll('[data-timer-mode]').forEach((button) => {
      const active = button.getAttribute('data-timer-mode') === mode;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', String(active));
    });
    countdowns.forEach(renderCountdown);
  };

  timerModules.forEach((module) => {
    module.setAttribute('data-timer-mode', 'clock');
    module.setAttribute('data-timer-filter', 'all');
    module.querySelector('[data-timer-sort]')?.addEventListener('change', (event) => {
      if (event.target.value === 'days-since') setModeButtonState(module, 'days');
      updateModule(module);
    });

    module.querySelectorAll('[data-timer-mode]').forEach((button) => {
      button.addEventListener('click', () => setModeButtonState(module, button.getAttribute('data-timer-mode') || 'clock'));
    });

    module.querySelectorAll('[data-timer-filter]').forEach((button) => {
      button.addEventListener('click', () => {
        const filter = button.getAttribute('data-timer-filter') || 'all';
        module.setAttribute('data-timer-filter', filter);
        module.querySelectorAll('[data-timer-filter]').forEach((item) => {
          const active = item === button;
          item.classList.toggle('is-active', active);
          item.setAttribute('aria-pressed', String(active));
        });
        if (filter === 'past' || filter === 'since') {
          setModeButtonState(module, 'days');
          const sorter = module.querySelector('[data-timer-sort]');
          if (filter === 'since' && sorter) sorter.value = 'days-since';
        }
        updateModule(module);
      });
    });

    updateModule(module);
  });

  const updateCountdowns = () => {
    countdowns.forEach(renderCountdown);
    timerModules.forEach(updateModule);
  };
  updateCountdowns();
  if (countdowns.length) setInterval(updateCountdowns, 1000);

  const setActiveState = (slug) => {
    if (!slug) return;
    mapTargets.forEach((target) => {
      target.classList.toggle('is-active', target.getAttribute('data-map-state') === slug);
    });
    stateTargets.forEach((target) => {
      target.classList.toggle('is-active-state', target.getAttribute('data-state') === slug);
    });
  };

  const bindStateActivation = (target, attribute) => {
    const slug = target.getAttribute(attribute);
    if (!slug) return;
    ['pointerenter', 'focusin', 'pointerdown', 'touchstart'].forEach((eventName) => {
      target.addEventListener(eventName, () => setActiveState(slug), { passive: true });
    });
  };

  mapTargets.forEach((target) => bindStateActivation(target, 'data-map-state'));
  stateTargets.forEach((target) => bindStateActivation(target, 'data-state'));

  const hashSlug = location.hash.replace('#', '').trim().toLowerCase();
  const initial = hashSlug || mapTargets[0]?.getAttribute('data-map-state') || stateTargets[0]?.getAttribute('data-state');
  setActiveState(initial);
})();

(() => {
  const builders = Array.from(document.querySelectorAll('[data-map-layer-builder]'));
  if (!builders.length) return;

  const layerCopy = {
    councils: {
      title: 'Local councils layer',
      copy: 'Future SVG or GeoJSON council boundaries should render here first, then each council opens its own self-similar local portal.'
    },
    electorates: {
      title: 'State electorates layer',
      copy: 'Electorate maps connect local issues to representation, by-elections, campaign pages and parliamentary responsibility.'
    },
    bioregions: {
      title: 'Bioregions layer',
      copy: 'Living-system maps compare catchments, coastlines, food systems, disaster corridors and ecological repair zones against legal boundaries.'
    },
    'first-nations': {
      title: 'First Nations maps layer',
      copy: 'Nation, Country and language maps need protocol and source humility; they guide learning without replacing cultural authority.'
    }
  };

  builders.forEach((builder) => {
    const setLayer = (layer) => {
      builder.querySelectorAll('[data-map-layer-choice]').forEach((button) => {
        const active = button.getAttribute('data-map-layer-choice') === layer;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      builder.querySelectorAll('[data-map-layer-panel]').forEach((panel) => {
        const active = panel.getAttribute('data-map-layer-panel') === layer;
        panel.hidden = !active;
        panel.classList.toggle('is-active', active);
      });
      const title = builder.querySelector('[data-map-layer-title]');
      const copy = builder.querySelector('[data-map-layer-copy]');
      if (title && layerCopy[layer]) title.textContent = layerCopy[layer].title;
      if (copy && layerCopy[layer]) copy.textContent = layerCopy[layer].copy;
    };

    builder.querySelectorAll('[data-map-layer-choice]').forEach((button) => {
      button.addEventListener('click', () => setLayer(button.getAttribute('data-map-layer-choice') || 'councils'));
    });
    setLayer('councils');
  });
})();

(() => {
  const modules = Array.from(document.querySelectorAll('[data-history-module]'));
  if (!modules.length) return;

  const text = (value) => (value || '').trim().toLowerCase();
  const getYear = (card) => {
    const year = Number(card.getAttribute('data-history-sort-year'));
    return Number.isFinite(year) ? year : Number.MAX_SAFE_INTEGER;
  };
  const getState = (card) => text(card.getAttribute('data-state'));
  const getPeriod = (card) => text(card.getAttribute('data-history-period'));
  const getTitle = (card) => text(card.getAttribute('data-history-title'));
  const getFirstTheme = (card) => text((card.getAttribute('data-history-themes') || '').split(',')[0]);

  const compareCards = (sortMode) => (a, b) => {
    if (sortMode === 'newest') return getYear(b) - getYear(a) || getState(a).localeCompare(getState(b)) || getTitle(a).localeCompare(getTitle(b));
    if (sortMode === 'state') return getState(a).localeCompare(getState(b)) || getYear(a) - getYear(b);
    if (sortMode === 'theme') return getFirstTheme(a).localeCompare(getFirstTheme(b)) || getYear(a) - getYear(b);
    if (sortMode === 'period') return getPeriod(a).localeCompare(getPeriod(b)) || getYear(a) - getYear(b);
    return getYear(a) - getYear(b) || getState(a).localeCompare(getState(b)) || getTitle(a).localeCompare(getTitle(b));
  };

  const matchesTheme = (card, theme) => {
    if (theme === 'all') return true;
    const themes = (card.getAttribute('data-history-themes') || '').split(',').map((item) => item.trim());
    return themes.includes(theme);
  };

  const updateHistoryModule = (module) => {
    const board = module.querySelector('[data-history-board]');
    if (!board) return;

    const sortMode = module.querySelector('[data-history-sort]')?.value || 'oldest';
    const levelMode = module.querySelector('[data-history-level]')?.value || 'basic';
    const themeMode = module.querySelector('[data-history-theme]')?.value || 'all';
    const search = text(module.querySelector('[data-history-search]')?.value);
    const cards = Array.from(board.querySelectorAll('[data-history-card]'));

    cards.sort(compareCards(sortMode)).forEach((card) => board.appendChild(card));

    let visibleCount = 0;
    cards.forEach((card) => {
      const cardLevel = text(card.getAttribute('data-history-level'));
      const levelVisible = levelMode === 'all' || cardLevel === levelMode;
      const themeVisible = matchesTheme(card, themeMode);
      const searchVisible = !search || text(card.textContent).includes(search);
      const visible = levelVisible && themeVisible && searchVisible;
      card.hidden = !visible;
      card.classList.toggle('is-filtered-out', !visible);
      if (visible) visibleCount += 1;
    });

    const count = module.querySelector('[data-history-count]');
    if (count) {
      const noun = visibleCount === 1 ? 'event' : 'events';
      count.textContent = `${visibleCount} of ${cards.length} history ${noun} shown`;
    }

    const empty = module.querySelector('[data-history-empty]');
    if (empty) empty.hidden = visibleCount > 0;
  };

  modules.forEach((module) => {
    ['data-history-sort', 'data-history-level', 'data-history-theme'].forEach((selector) => {
      module.querySelector(`[${selector}]`)?.addEventListener('change', () => updateHistoryModule(module));
    });
    module.querySelector('[data-history-search]')?.addEventListener('input', () => updateHistoryModule(module));
    updateHistoryModule(module);
  });
})();
