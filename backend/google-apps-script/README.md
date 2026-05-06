# P4A Gear Checkout Backend

Low-cost backend for the purple hoodie shopfront.

The design is intentionally boring:

1. GitHub Pages owns the storefront and builds one strict order payload.
2. Google Apps Script validates the payload against the same product catalogue.
3. Apps Script creates a Stripe Checkout Session.
4. Apps Script writes filterable rows into Google Sheets.
5. Luke places the supplier print order after payment clears.

Supplier role: printer/shipper only. The customer chooses the support/profit amount per item.

## Script properties

Set these in Apps Script project settings:

```text
STRIPE_SECRET_KEY=sk_test_or_live_key
STRIPE_SUCCESS_URL=https://auraofintelligence.github.io/p4a_xyz/pages/deployment-gear.html?gear=success
STRIPE_CANCEL_URL=https://auraofintelligence.github.io/p4a_xyz/pages/deployment-gear.html?gear=cancelled
ORDER_SHEET_ID=the_google_sheet_id
AUSPOST_PAC_API_KEY=optional_postage_assessment_calculation_key
```

Use Stripe test mode first.

## Setup

1. Create a Google Sheet.
2. Create an Apps Script project attached to it, or a standalone project.
3. Paste `gear-checkout.gs`.
4. Set the script properties above.
5. Run `setupGearBackend()` once from the Apps Script editor.
6. Deploy as a web app when ready.

You can also POST this action after deployment:

```json
{
  "action": "setupSheets"
}
```

## Sheet tabs

The script creates these filterable tabs:

- `Orders`: one row per customer order and Stripe checkout session.
- `OrderItems`: one row per product line, mapped to The Tshirt Mill and the website store.
- `Products`: website product ID, supplier name, supplier product ID/code, product URL, single price, 50+ floor price.
- `ProductColours`: only verified colour/image combinations exposed in the shopfront, including the plain storefront label and exact supplier colour name.
- `ProductSizes`: available sizes plus captured size-guide measurements where known.
- `DiscountTiers`: 1, 5, 10, 20, 30 and 50 item thresholds.
- `ShippingEstimates`: pickup/postage mode, Dunwich origin, postcode, AusPost calculator URL, API status, entered estimate and parcel fields.
- `Events`: simple audit trail.

## Fulfilment lanes

The pilot defaults to `pickup_dunwich`: local pickup from Dunwich, North Stradbroke Island / Minjerribah, with no postage added.

For postage, use `ship_from_dunwich`. The script keeps the Australia Post calculator as a manual fallback and includes a `quotePostage` action for future automated PAC quoting once `AUSPOST_PAC_API_KEY` is set.

For serious organiser orders, use `branch_bundle` with `local_handoff`. That captures branch/group name, volunteer count, add-on interest and bulk notes so Angel or Luke can quote a proper campaign kit.

## Order payload

The frontend sends `schema_version = p4a_gear_order_v1` and fields such as:

```json
{
  "action": "createCheckout",
  "schema_version": "p4a_gear_order_v1",
  "order": {
    "website_product_id": "gildan-adult-hooded-sweatshirt",
    "order_mode": "single",
    "supplier_colour_label": "Purple",
    "supplier_colour_name": "Purple",
    "size": "M",
    "quantity": 1,
    "fulfilment_method": "pickup_dunwich",
    "unit_customer_cost_aud": 52.95,
    "support_per_item_aud": 20,
    "shipping_estimate_aud": 0,
    "order_total_aud": 72.95
  }
}
```

Apps Script recalculates cost, discounts and totals from its own catalogue before it trusts the order.

## Product source table

Use `product-source-pages.md` as the capture list for supplier pages. The storefront should only expose a colour/product pair after its page URL, supplier product ID/code, image and size data are captured there and mirrored in `gear-checkout.gs`.
