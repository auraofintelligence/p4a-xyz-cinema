const STRIPE_API_BASE = 'https://api.stripe.com/v1';
const SCHEMA_VERSION = 'p4a_gear_order_v1';
const CURRENCY = 'aud';
const AUSPOST_CALCULATOR_URL = 'https://auspost.com.au/parcels-mail/calculate-postage-delivery-times/#/';
const FULFILMENT_OPTIONS = {
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
const SUPPLIER_COLLECTION_URLS = {
  Purple: 'https://www.thetshirtmill.com.au/create?c=3097422&color=37,-7',
  Lavender: 'https://www.thetshirtmill.com.au/create?c=3097422&color=27,-7'
};

const SHEETS = {
  orders: 'Orders',
  items: 'OrderItems',
  products: 'Products',
  colours: 'ProductColours',
  sizes: 'ProductSizes',
  discounts: 'DiscountTiers',
  shipping: 'ShippingEstimates',
  events: 'Events'
};

const HEADERS = {
  Orders: [
    'order_id', 'created_at', 'updated_at', 'status', 'source', 'schema_version', 'order_mode',
    'stripe_session_id', 'stripe_checkout_url', 'buyer_name', 'buyer_email',
    'currency', 'order_total_aud', 'item_cost_subtotal_aud', 'support_total_aud',
    'fulfilment_method', 'fulfilment_label', 'fulfilment_origin_label',
    'shipping_estimate_aud', 'shipping_provider', 'shipping_mode', 'shipping_origin_postcode',
    'shipping_destination_postcode', 'auspost_calculator_url', 'fulfilment_status',
    'fulfilment_note', 'branch_name', 'volunteer_count', 'addon_interest', 'bulk_notes'
  ],
  OrderItems: [
    'order_id', 'line_number', 'website_product_id', 'product_label',
    'supplier_name', 'supplier_product_id', 'supplier_product_code', 'supplier_product_url',
    'supplier_category', 'supplier_manufacturer', 'supplier_process',
    'supplier_colour_label', 'supplier_colour_name', 'supplier_colour_filter',
    'supplier_collection_url', 'supplier_image_path',
    'size', 'quantity', 'quantity_discount_min', 'quantity_discount_rate',
    'quantity_discount_label', 'unit_supplier_single_aud', 'unit_discount_aud',
    'unit_customer_cost_aud', 'item_cost_subtotal_aud', 'support_per_item_aud',
    'support_total_aud', 'logo_style', 'order_mode', 'branch_name',
    'volunteer_count', 'addon_interest', 'bulk_notes'
  ],
  Products: [
    'website_product_id', 'product_label', 'supplier_name', 'supplier_product_id',
    'supplier_product_code', 'supplier_product_url', 'supplier_category', 'supplier_manufacturer',
    'supplier_process', 'single_unit_cost_aud', 'floor_unit_cost_aud',
    'floor_min_quantity', 'visible_on_store', 'notes'
  ],
  ProductColours: [
    'website_product_id', 'colour_label', 'supplier_colour_name',
    'supplier_colour_filter', 'supplier_collection_url', 'image_path',
    'verified_for_store', 'notes'
  ],
  ProductSizes: [
    'website_product_id', 'size_label', 'available', 'width_cm', 'length_cm',
    'sleeve_center_back_cm', 'guide_source', 'verified_measurements'
  ],
  DiscountTiers: ['min_quantity', 'discount_rate', 'discount_label', 'notes'],
  ShippingEstimates: [
    'order_id', 'created_at', 'provider', 'shipping_mode', 'fulfilment_method',
    'fulfilment_label', 'origin_label', 'origin_postcode',
    'destination_postcode', 'calculator_url', 'auspost_api_status',
    'entered_shipping_estimate_aud',
    'parcel_weight_kg', 'parcel_length_cm', 'parcel_width_cm', 'parcel_height_cm',
    'production_time_note', 'notes'
  ],
  Events: ['created_at', 'event_type', 'order_id', 'stripe_session_id', 'message']
};

const DISCOUNT_TIERS = [
  { min: 1, rate: 0, label: 'single price', notes: 'Applies to 1-4 items' },
  { min: 5, rate: 0.05, label: '5% off', notes: 'Supplier discount threshold' },
  { min: 10, rate: 0.10, label: '10% off', notes: 'Supplier discount threshold' },
  { min: 20, rate: 0.15, label: '15% off', notes: 'Supplier discount threshold' },
  { min: 30, rate: 0.20, label: '20% off', notes: 'Supplier discount threshold' },
  { min: 50, rate: 0.25, label: '25% floor', notes: 'Floor price shown on supplier cards' }
];

const PRODUCTS = [
  {
    id: 'gildan-adult-hooded-sweatshirt',
    label: 'Gildan Adult Hooded Sweatshirt',
    supplierProductId: '306598281',
    supplierProductCode: '',
    supplierUrl: 'https://www.thetshirtmill.com.au/blank_product/306598281/Adult-Hooded-Sweatshirt?c=3097422',
    manufacturer: 'GILDAN',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 52.95,
    floor: 39.71,
    notes: 'Lowest starting cost, classic pullover fit.',
    colours: [{ label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/gildan-adult-hoodie.png' }],
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'],
    guide: {
      source: 'supplier screenshot',
      verified: true,
      rows: {
        XS: ['', '', ''],
        S: ['51', '69', '85'],
        M: ['56', '71', '88'],
        L: ['61', '74', '90'],
        XL: ['66', '76', '93'],
        '2XL': ['71', '79', '95'],
        '3XL': ['76', '81', '98'],
        '4XL': ['81', '84', '100'],
        '5XL': ['86', '86', '103']
      }
    }
  },
  {
    id: 'ramo-adult-poly-cotton-fleece-sloppy-joe',
    label: 'RAMO Adult Poly Cotton Fleece Sloppy Joe',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 57.45,
    floor: 43.09,
    notes: 'Crewneck option for lighter purple deployment gear.',
    colours: [
      { label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/ramo-sloppy-joe.png' },
      { label: 'Lavender', supplierColourName: 'Lavender', filter: '27', image: '../assets/gear-products/lavender-sloppy-joe.png' }
    ],
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']
  },
  {
    id: 'unisex-adults-pull-over-hoodie',
    label: 'Unisex Adults Pull Over Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Purple,
    manufacturer: '',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 59.99,
    floor: 44.99,
    notes: 'Wide size range, good one-at-a-time test base.',
    colours: [{ label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/unisex-pullover.png' }],
    sizes: ['XS', 'S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '7XL']
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
    single: 62.35,
    floor: 46.76,
    notes: 'RAMO TP212H. Purple storefront option maps to supplier colour Grape; Lavender is also verified.',
    colours: [
      { label: 'Purple', supplierColourName: 'Grape', filter: '-7', image: '../assets/gear-products/ramo-kangaroo-pocket-grape-front.jpg' },
      { label: 'Lavender', supplierColourName: 'Lavender', filter: '27', image: '../assets/gear-products/ramo-kangaroo-pocket-lavender-front.jpg' }
    ],
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL'],
    guide: {
      source: 'supplier page 277286481 captured 2026-05-06',
      verified: true,
      rows: {
        S: ['59', '', ''],
        M: ['61', '', ''],
        L: ['63', '', ''],
        XL: ['65', '', ''],
        '2XL': ['67', '', ''],
        '3XL': ['69', '', ''],
        '4XL': ['71', '', ''],
        '5XL': ['73', '', ''],
        '6XL': ['75', '', ''],
        '7XL': ['77', '', '']
      }
    }
  },
  {
    id: 'ramo-mens-brushed-heavy-zip-fleece-hoodie',
    label: 'RAMO Mens Brushed Heavy Zip Fleece Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 65.00,
    floor: 48.75,
    notes: 'Zip option for people who hate pullovers.',
    colours: [{ label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/ramo-heavy-zip.png' }],
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']
  },
  {
    id: 'ramo-mens-zip-hoodie-with-pocket',
    label: 'RAMO Mens Zip Hoodie with Pocket',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 77.20,
    floor: 57.90,
    notes: 'Higher-cost zip hoodie, still purple-family.',
    colours: [
      { label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/ramo-zip-pocket.png' },
      { label: 'Lavender', supplierColourName: 'Lavender', filter: '27', image: '../assets/gear-products/lavender-zip-pocket.png' }
    ],
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL', '6XL', '7XL']
  },
  {
    id: 'ramo-mens-brushed-heavy-fleece-hoodie',
    label: 'RAMO Mens Brushed Heavy Fleece Hoodie',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Purple,
    manufacturer: 'RAMO',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 82.39,
    floor: 61.79,
    notes: 'Premium heavy fleece test option.',
    colours: [{ label: 'Purple', supplierColourName: 'Purple', filter: '-7', image: '../assets/gear-products/ramo-heavy-fleece.png' }],
    sizes: ['S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL']
  },
  {
    id: 'comfort-colors-color-blast-crewneck',
    label: 'Comfort Colors Color Blast Crewneck',
    supplierProductId: '',
    supplierProductCode: '',
    supplierUrl: SUPPLIER_COLLECTION_URLS.Lavender,
    manufacturer: 'COMFORT COLORS',
    category: 'Sweatshirts & Hoodies',
    process: 'DTF Printing',
    single: 100.71,
    floor: 75.53,
    notes: 'Expensive lavender crewneck, only if the market asks.',
    colours: [{ label: 'Lavender', supplierColourName: 'Lavender', filter: '27', image: '../assets/gear-products/comfort-colorblast.png' }],
    sizes: ['S', 'M', 'L', 'XL', '2XL']
  }
];

function doGet() {
  return jsonResponse({
    schema_version: SCHEMA_VERSION,
    sheets: SHEETS,
    headers: HEADERS,
    products: PRODUCTS,
    discount_tiers: DISCOUNT_TIERS
  });
}

function doPost(event) {
  try {
    const payload = JSON.parse((event.postData && event.postData.contents) || '{}');

    if (payload.action === 'setupSheets') {
      setupGearBackend();
      return jsonResponse({ ok: true, message: 'Sheets created and seeded.' });
    }

    if (payload.action === 'logDemoOrder') {
      const order = normaliseOrder_(payload.order || {});
      const orderId = logOrder_(order, '', '');
      return jsonResponse({ ok: true, order_id: orderId });
    }

    if (payload.action === 'quotePostage') {
      const order = normaliseOrder_(payload.order || {});
      return jsonResponse({ ok: true, fulfilment_method: order.fulfilment_method, postage: quotePostage_(order) });
    }

    if (payload.action === 'createCheckout') {
      const order = normaliseOrder_(payload.order || {});
      const session = createCheckoutSession_(order);
      const orderId = logOrder_(order, session.id, session.url);
      return jsonResponse({ ok: true, order_id: orderId, checkoutUrl: session.url });
    }

    return jsonResponse({ ok: false, error: 'Unknown action.' });
  } catch (error) {
    return jsonResponse({ ok: false, error: String(error && error.message ? error.message : error) });
  }
}

function setupGearBackend() {
  const spreadsheet = getSpreadsheet_();
  Object.keys(HEADERS).forEach((sheetName) => {
    const sheet = getOrCreateSheet_(spreadsheet, sheetName);
    ensureHeaders_(sheet, HEADERS[sheetName]);
  });

  replaceRows_(spreadsheet.getSheetByName(SHEETS.products), HEADERS.Products, productRows_());
  replaceRows_(spreadsheet.getSheetByName(SHEETS.colours), HEADERS.ProductColours, colourRows_());
  replaceRows_(spreadsheet.getSheetByName(SHEETS.sizes), HEADERS.ProductSizes, sizeRows_());
  replaceRows_(spreadsheet.getSheetByName(SHEETS.discounts), HEADERS.DiscountTiers, discountRows_());
}

function createCheckoutSession_(order) {
  const stripeKey = PropertiesService.getScriptProperties().getProperty('STRIPE_SECRET_KEY');
  const successUrl = PropertiesService.getScriptProperties().getProperty('STRIPE_SUCCESS_URL');
  const cancelUrl = PropertiesService.getScriptProperties().getProperty('STRIPE_CANCEL_URL');

  if (!stripeKey || !successUrl || !cancelUrl) {
    throw new Error('Missing STRIPE_SECRET_KEY, STRIPE_SUCCESS_URL, or STRIPE_CANCEL_URL.');
  }

  const itemUnitCents = dollarsToCents_(order.unit_customer_cost_aud + order.support_per_item_aud);
  const shippingCents = dollarsToCents_(order.shipping_estimate_aud);

  const params = {
    mode: 'payment',
    success_url: successUrl,
    cancel_url: cancelUrl,
    'line_items[0][quantity]': String(order.quantity),
    'line_items[0][price_data][currency]': CURRENCY,
    'line_items[0][price_data][product_data][name]': order.product_label,
    'line_items[0][price_data][product_data][description]': `${order.supplier_colour_label} (${order.supplier_colour_name}), ${order.size}, ${order.logo_style}`,
    'line_items[0][price_data][unit_amount]': String(itemUnitCents),
    'metadata[schema_version]': SCHEMA_VERSION,
    'metadata[order_mode]': order.order_mode,
    'metadata[website_product_id]': order.website_product_id,
    'metadata[supplier_product_code]': order.supplier_product_code,
    'metadata[supplier_colour_label]': order.supplier_colour_label,
    'metadata[supplier_colour_name]': order.supplier_colour_name,
    'metadata[supplier_collection_url]': order.supplier_collection_url,
    'metadata[size]': order.size,
    'metadata[quantity]': String(order.quantity),
    'metadata[support_per_item_aud]': String(order.support_per_item_aud),
    'metadata[fulfilment_method]': order.fulfilment_method,
    'metadata[shipping_estimate_aud]': String(order.shipping_estimate_aud),
    'metadata[branch_name]': order.branch_name,
    'metadata[volunteer_count]': String(order.volunteer_count)
  };

  if (shippingCents > 0) {
    params['line_items[1][quantity]'] = '1';
    params['line_items[1][price_data][currency]'] = CURRENCY;
    params['line_items[1][price_data][product_data][name]'] = 'Shipping estimate';
    params['line_items[1][price_data][unit_amount]'] = String(shippingCents);
  }

  if (order.buyer_email) {
    params.customer_email = order.buyer_email;
  }

  const response = UrlFetchApp.fetch(`${STRIPE_API_BASE}/checkout/sessions`, {
    method: 'post',
    headers: { Authorization: `Bearer ${stripeKey}` },
    payload: params,
    muteHttpExceptions: true
  });
  const body = JSON.parse(response.getContentText());

  if (response.getResponseCode() >= 300) {
    throw new Error(body.error && body.error.message ? body.error.message : 'Stripe checkout failed.');
  }

  return body;
}

function quotePostage_(order) {
  if (order.shipping_mode === 'pickup') {
    return {
      required: false,
      provider: order.shipping_provider,
      amount_aud: 0,
      note: 'Pickup selected. No postage quote required.'
    };
  }

  const apiKey = PropertiesService.getScriptProperties().getProperty('AUSPOST_PAC_API_KEY');
  if (!apiKey) {
    return {
      required: true,
      provider: order.shipping_provider,
      amount_aud: order.shipping_estimate_aud,
      status: 'missing_api_key',
      note: 'Set AUSPOST_PAC_API_KEY to automate postage from Dunwich 4183. Current value is the manual estimate.'
    };
  }

  if (!order.shipping_destination_postcode) {
    return {
      required: true,
      provider: order.shipping_provider,
      amount_aud: order.shipping_estimate_aud,
      status: 'missing_destination_postcode',
      note: 'Destination postcode is needed before calling Australia Post PAC API.'
    };
  }

  const params = {
    from_postcode: order.shipping_origin_postcode,
    to_postcode: order.shipping_destination_postcode,
    length: String(order.parcel_length_cm),
    width: String(order.parcel_width_cm),
    height: String(order.parcel_height_cm),
    weight: String(order.parcel_weight_kg)
  };
  const query = Object.keys(params)
    .map((key) => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
    .join('&');
  const url = `https://digitalapi.auspost.com.au/postage/parcel/domestic/service.json?${query}`;
  const response = UrlFetchApp.fetch(url, {
    method: 'get',
    headers: { 'AUTH-KEY': apiKey },
    muteHttpExceptions: true
  });
  const body = JSON.parse(response.getContentText());

  if (response.getResponseCode() >= 300) {
    return {
      required: true,
      provider: order.shipping_provider,
      amount_aud: order.shipping_estimate_aud,
      status: 'api_error',
      error: body.error && body.error.errorMessage ? body.error.errorMessage : response.getContentText(),
      note: 'Australia Post PAC API failed; fallback to manual quote.'
    };
  }

  return {
    required: true,
    provider: 'auspost_pac_api',
    status: 'quoted',
    origin_postcode: order.shipping_origin_postcode,
    destination_postcode: order.shipping_destination_postcode,
    parcel_weight_kg: order.parcel_weight_kg,
    parcel_length_cm: order.parcel_length_cm,
    parcel_width_cm: order.parcel_width_cm,
    parcel_height_cm: order.parcel_height_cm,
    raw: body
  };
}

function normaliseOrder_(raw) {
  const product = PRODUCTS.find((item) => item.id === raw.website_product_id);
  if (!product) throw new Error('Unknown website_product_id.');

  const colour = product.colours.find((item) => item.label === raw.supplier_colour_label);
  if (!colour) throw new Error('Unknown or unverified supplier colour for selected product.');

  if (product.sizes.indexOf(raw.size) === -1) {
    throw new Error('Size is not available for selected product.');
  }

  const quantity = Math.max(1, Number(raw.quantity || 1));
  const fulfilment = FULFILMENT_OPTIONS[raw.fulfilment_method] || FULFILMENT_OPTIONS.pickup_dunwich;
  const tier = discountTier_(quantity);
  const unitSupplierSingle = roundMoney_(product.single);
  const unitDiscount = roundMoney_(unitSupplierSingle * tier.rate);
  const unitCustomerCost = roundMoney_(unitSupplierSingle - unitDiscount);
  const itemCostSubtotal = roundMoney_(unitCustomerCost * quantity);
  const supportPerItem = roundMoney_(Math.max(0, Number(raw.support_per_item_aud || 0)));
  const supportTotal = roundMoney_(supportPerItem * quantity);
  const shippingEstimate = fulfilment.shippingMode === 'pickup' ? 0 : roundMoney_(Math.max(0, Number(raw.shipping_estimate_aud || 0)));
  const total = roundMoney_(itemCostSubtotal + supportTotal + shippingEstimate);
  const addonInterest = Array.isArray(raw.addon_interest) ? raw.addon_interest.map(String) : String(raw.addon_interest || '').split(',').map((item) => item.trim()).filter(Boolean);

  return {
    source: String(raw.source || 'p4a_xyz_deployment_gear_demo'),
    schema_version: SCHEMA_VERSION,
    order_mode: String(raw.order_mode || 'single'),
    website_product_id: product.id,
    product_label: product.label,
    supplier_name: 'Dunwich local shirt printer first; supplier catalogue reference',
    supplier_product_id: product.supplierProductId,
    supplier_product_code: product.supplierProductCode || '',
    supplier_product_url: product.supplierUrl,
    supplier_category: product.category,
    supplier_manufacturer: product.manufacturer,
    supplier_process: product.process,
    supplier_colour_label: colour.label,
    supplier_colour_name: colour.supplierColourName || colour.label,
    supplier_colour_filter: colour.filter,
    supplier_collection_url: SUPPLIER_COLLECTION_URLS[colour.label] || product.supplierUrl,
    supplier_image_path: colour.image,
    size: raw.size,
    quantity,
    quantity_discount_min: tier.min,
    quantity_discount_rate: tier.rate,
    quantity_discount_label: tier.label,
    unit_supplier_single_aud: unitSupplierSingle,
    unit_discount_aud: unitDiscount,
    unit_customer_cost_aud: unitCustomerCost,
    item_cost_subtotal_aud: itemCostSubtotal,
    support_per_item_aud: supportPerItem,
    support_total_aud: supportTotal,
    fulfilment_method: raw.fulfilment_method && FULFILMENT_OPTIONS[raw.fulfilment_method] ? raw.fulfilment_method : 'pickup_dunwich',
    fulfilment_label: fulfilment.label,
    fulfilment_origin_label: fulfilment.originLabel,
    shipping_estimate_aud: shippingEstimate,
    shipping_provider: fulfilment.provider,
    shipping_mode: fulfilment.shippingMode,
    shipping_origin_postcode: fulfilment.originPostcode,
    shipping_destination_postcode: String(raw.shipping_destination_postcode || ''),
    auspost_calculator_url: String(raw.auspost_calculator_url || AUSPOST_CALCULATOR_URL),
    auspost_api_status: fulfilment.shippingMode === 'postage' ? 'planned_pac_api' : 'not_required_for_selected_fulfilment',
    parcel_weight_kg: roundMoney_(Math.max(0.5, Number(raw.parcel_weight_kg || quantity * 0.75))),
    parcel_length_cm: Number(raw.parcel_length_cm || 35),
    parcel_width_cm: Number(raw.parcel_width_cm || 28),
    parcel_height_cm: Number(raw.parcel_height_cm || Math.min(45, Math.max(8, quantity * 6))),
    logo_style: String(raw.logo_style || 'P4A chest mark'),
    branch_name: String(raw.branch_name || ''),
    volunteer_count: Math.max(0, Number(raw.volunteer_count || 0)),
    addon_interest: addonInterest,
    bulk_notes: String(raw.bulk_notes || ''),
    buyer_name: String(raw.buyer_name || ''),
    buyer_email: String(raw.buyer_email || ''),
    order_total_aud: total,
    currency: 'AUD',
    fulfilment_status: String(raw.fulfilment_status || 'checkout_created'),
    fulfilment_note: String(raw.fulfilment_note || fulfilment.note)
  };
}

function logOrder_(order, stripeSessionId, checkoutUrl) {
  const spreadsheet = getSpreadsheet_();
  const now = new Date();
  const orderId = Utilities.getUuid();
  appendByHeader_(spreadsheet.getSheetByName(SHEETS.orders), HEADERS.Orders, {
    order_id: orderId,
    created_at: now,
    updated_at: now,
    status: stripeSessionId ? 'checkout_created' : 'demo_logged',
    source: order.source,
    schema_version: SCHEMA_VERSION,
    order_mode: order.order_mode,
    stripe_session_id: stripeSessionId,
    stripe_checkout_url: checkoutUrl,
    buyer_name: order.buyer_name,
    buyer_email: order.buyer_email,
    currency: order.currency,
    order_total_aud: order.order_total_aud,
    item_cost_subtotal_aud: order.item_cost_subtotal_aud,
    support_total_aud: order.support_total_aud,
    fulfilment_method: order.fulfilment_method,
    fulfilment_label: order.fulfilment_label,
    fulfilment_origin_label: order.fulfilment_origin_label,
    shipping_estimate_aud: order.shipping_estimate_aud,
    shipping_provider: order.shipping_provider,
    shipping_mode: order.shipping_mode,
    shipping_origin_postcode: order.shipping_origin_postcode,
    shipping_destination_postcode: order.shipping_destination_postcode,
    auspost_calculator_url: order.auspost_calculator_url,
    fulfilment_status: order.fulfilment_status,
    fulfilment_note: order.fulfilment_note,
    branch_name: order.branch_name,
    volunteer_count: order.volunteer_count,
    addon_interest: order.addon_interest.join(', '),
    bulk_notes: order.bulk_notes
  });

  appendByHeader_(spreadsheet.getSheetByName(SHEETS.items), HEADERS.OrderItems, Object.assign({ order_id: orderId, line_number: 1 }, order));
  appendByHeader_(spreadsheet.getSheetByName(SHEETS.shipping), HEADERS.ShippingEstimates, {
    order_id: orderId,
    created_at: now,
    provider: order.shipping_provider,
    shipping_mode: order.shipping_mode,
    fulfilment_method: order.fulfilment_method,
    fulfilment_label: order.fulfilment_label,
    origin_label: order.fulfilment_origin_label,
    origin_postcode: order.shipping_origin_postcode,
    destination_postcode: order.shipping_destination_postcode,
    calculator_url: order.auspost_calculator_url,
    auspost_api_status: order.auspost_api_status,
    entered_shipping_estimate_aud: order.shipping_estimate_aud,
    parcel_weight_kg: order.parcel_weight_kg,
    parcel_length_cm: order.parcel_length_cm,
    parcel_width_cm: order.parcel_width_cm,
    parcel_height_cm: order.parcel_height_cm,
    production_time_note: 'Local Dunwich printer first; add production time before quoting delivery.',
    notes: 'Use pickup by default. Postage automation should call Australia Post PAC API from 4183 once configured.'
  });
  appendByHeader_(spreadsheet.getSheetByName(SHEETS.events), HEADERS.Events, {
    created_at: now,
    event_type: stripeSessionId ? 'stripe_checkout_created' : 'demo_order_logged',
    order_id: orderId,
    stripe_session_id: stripeSessionId,
    message: checkoutUrl || 'Demo order logged without Stripe session.'
  });

  return orderId;
}

function getSpreadsheet_() {
  const sheetId = PropertiesService.getScriptProperties().getProperty('ORDER_SHEET_ID');
  if (!sheetId) throw new Error('Missing ORDER_SHEET_ID script property.');
  const spreadsheet = SpreadsheetApp.openById(sheetId);
  Object.keys(SHEETS).forEach((key) => getOrCreateSheet_(spreadsheet, SHEETS[key]));
  return spreadsheet;
}

function getOrCreateSheet_(spreadsheet, name) {
  return spreadsheet.getSheetByName(name) || spreadsheet.insertSheet(name);
}

function ensureHeaders_(sheet, headers) {
  const existing = sheet.getLastColumn() ? sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0] : [];
  if (existing.join('|') !== headers.join('|')) {
    sheet.clear();
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.setFrozenRows(1);
  }
}

function replaceRows_(sheet, headers, rows) {
  ensureHeaders_(sheet, headers);
  if (sheet.getLastRow() > 1) {
    sheet.getRange(2, 1, sheet.getLastRow() - 1, headers.length).clearContent();
  }
  if (rows.length) {
    sheet.getRange(2, 1, rows.length, headers.length).setValues(rows);
  }
}

function appendByHeader_(sheet, headers, row) {
  ensureHeaders_(sheet, headers);
  sheet.appendRow(headers.map((header) => {
    const value = row[header];
    if (value === undefined) return '';
    return Array.isArray(value) ? value.join(', ') : value;
  }));
}

function productRows_() {
  return PRODUCTS.map((item) => [
    item.id, item.label, 'The Tshirt Mill', item.supplierProductId, item.supplierProductCode || '', item.supplierUrl,
    item.category, item.manufacturer, item.process, item.single, item.floor, 50, true, item.notes
  ]);
}

function colourRows_() {
  return PRODUCTS.reduce((rows, item) => rows.concat(item.colours.map((colour) => [
    item.id, colour.label, colour.supplierColourName || colour.label,
    colour.filter, SUPPLIER_COLLECTION_URLS[colour.label] || item.supplierUrl,
    colour.image, true, 'Only verified colour/image variants are exposed in the storefront.'
  ])), []);
}

function sizeRows_() {
  return PRODUCTS.reduce((rows, item) => rows.concat(item.sizes.map((size) => {
    const guide = item.guide && item.guide.rows && item.guide.rows[size] ? item.guide.rows[size] : ['', '', ''];
    return [
      item.id, size, true, guide[0], guide[1], guide[2],
      item.guide ? item.guide.source : 'supplier card size list',
      item.guide ? item.guide.verified : false
    ];
  })), []);
}

function discountRows_() {
  return DISCOUNT_TIERS.map((tier) => [tier.min, tier.rate, tier.label, tier.notes]);
}

function discountTier_(quantity) {
  return DISCOUNT_TIERS.reduce((active, tier) => quantity >= tier.min ? tier : active, DISCOUNT_TIERS[0]);
}

function dollarsToCents_(value) {
  return Math.round(roundMoney_(value) * 100);
}

function roundMoney_(value) {
  return Number((Math.round((Number(value || 0) + Number.EPSILON) * 100) / 100).toFixed(2));
}

function jsonResponse(body) {
  return ContentService
    .createTextOutput(JSON.stringify(body))
    .setMimeType(ContentService.MimeType.JSON);
}
