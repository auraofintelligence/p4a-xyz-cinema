# P4A Gear Supplier Source Pages

This is the capture table for matching the P4A storefront, Google Sheet tabs and The T-Shirt Mill options. A row is live-ready only when the supplier product URL, product ID/code, colour names, colour images, sizes, pricing and shipping/discount notes have been checked.

Storefront catalogue filters:

- Purple: `https://www.thetshirtmill.com.au/create?c=3097422&color=37,-7`
- Lavender: `https://www.thetshirtmill.com.au/create?c=3097422&color=27,-7`

Fulfilment defaults:

- Local printer first: Dunwich, North Stradbroke Island / Minjerribah.
- Pickup option: no postage added, customer or branch collects locally.
- Postage option: quote from postcode `4183` using Australia Post PAC API when configured, with the public calculator as fallback.
- Branch kit option: capture organiser intent before forcing a normal retail checkout.

| Store product ID | Store label | Supplier URL | Supplier product ID | Supplier code | Store colours | Exact supplier colour names | Image status | Size guide status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `gildan-adult-hooded-sweatshirt` | Gildan Adult Hooded Sweatshirt | `https://www.thetshirtmill.com.au/blank_product/306598281/Adult-Hooded-Sweatshirt?c=3097422` | `306598281` |  | Purple | Purple | Local screenshot image captured | Width, length and sleeve captured from supplier screenshot | Needs direct supplier page recheck before live checkout. |
| `ramo-mens-kangaroo-pocket-hoodie` | RAMO Mens Kangaroo Pocket Hoodie | `https://www.thetshirtmill.com.au/blank_product/277286481/Mens-Kangaroo-Pocket-Hoodies?c=3097422` | `277286481` | `TP212H` | Purple, Lavender | Grape, Lavender | Exact supplier front images cached locally | Half Chest row captured from supplier page | Storefront Purple maps to supplier colour Grape. |
| `ramo-adult-poly-cotton-fleece-sloppy-joe` | RAMO Adult Poly Cotton Fleece Sloppy Joe | needs exact blank product page |  |  | Purple, Lavender | needs supplier names | Local screenshot images captured | Size list only | Capture exact page before live checkout. |
| `unisex-adults-pull-over-hoodie` | Unisex Adults Pull Over Hoodie | needs exact blank product page |  |  | Purple | needs supplier name | Local screenshot image captured | Size list only | Capture exact page before live checkout. |
| `ramo-mens-brushed-heavy-zip-fleece-hoodie` | RAMO Mens Brushed Heavy Zip Fleece Hoodie | needs exact blank product page |  |  | Purple | needs supplier name | Local screenshot image captured | Size list only | Capture exact page before live checkout. |
| `ramo-mens-zip-hoodie-with-pocket` | RAMO Mens Zip Hoodie with Pocket | needs exact blank product page |  |  | Purple, Lavender | needs supplier names | Local screenshot images captured | Size list only | Capture exact page before live checkout. |
| `ramo-mens-brushed-heavy-fleece-hoodie` | RAMO Mens Brushed Heavy Fleece Hoodie | needs exact blank product page |  |  | Purple | needs supplier name | Local screenshot image captured | Size list only | Capture exact page before live checkout. |
| `comfort-colors-color-blast-crewneck` | Comfort Colors Color Blast Crewneck | needs exact blank product page |  |  | Lavender | needs supplier name | Local screenshot image captured | Size list only | Capture exact page before live checkout. |

Required capture fields for new rows:

- `supplier_product_id`: numeric ID from the blank product URL.
- `supplier_product_code`: supplier code from the page metadata, such as `TP212H`.
- `store_colour_label`: customer-facing colour group, such as Purple or Lavender.
- `supplier_colour_name`: exact supplier colour option, such as Grape.
- `supplier_colour_filter`: URL/filter value where visible.
- `supplier_image_path`: local cached image path used by the storefront and Apps Script.
- `sizes`: exact available sizes for that colour/product combination.
- `size_guide`: measurement rows and source date where available.
- `single_unit_cost_aud` and `floor_unit_cost_aud`: DTF single price and 50+ floor shown by the supplier.
