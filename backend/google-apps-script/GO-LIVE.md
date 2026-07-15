# Taking the gear store live

The storefront is wired and tested. This is the part only you can do, because it
involves accounts and keys. Claude must never handle either: keys go straight
from Stripe into Apps Script, and never into this repo.

Work through it in order. Nothing here costs money up front.

## What it costs

| Piece | Cost |
| --- | --- |
| GitHub Pages (storefront) | free |
| Google Apps Script (the small backend) | free |
| Google Sheets (order log) | free |
| Stripe account | free, no monthly fee |
| Stripe per sale | ~1.75% + 30c on Australian cards |
| Stock | none. You print per order, after you have been paid. |

The only money that moves before a sale is zero. That is the whole point of this
shape: a customer pays, the money lands, then you order the print.

## 1. Stripe account (you, not Claude)

1. Create a Stripe account at stripe.com. An individual/sole trader account is
   fine; you do not need a company.
2. Add the bank account the money should land in.
3. Stay in **test mode** for now. The toggle is in the dashboard.
4. Copy your **test** secret key (starts with `sk_test_`).

Never paste a key into this repo, a chat window, or any file under `assets/`.
It belongs in exactly one place: step 3 below.

## 2. Google Sheet + Apps Script

1. Create a new Google Sheet. Call it something like `P4A Gear Orders`.
2. From the Sheet: **Extensions > Apps Script**.
3. Delete the placeholder code. Paste the whole of `gear-checkout.gs`.
4. Copy the Sheet ID out of its URL: the long string between `/d/` and `/edit`.

## 3. Script properties (where the key lives)

In the Apps Script editor: **Project Settings > Script properties > Add**.

```text
STRIPE_SECRET_KEY   = sk_test_...   (your test key for now)
STRIPE_SUCCESS_URL  = https://p4a.xyz/pages/test-store1.html?gear=success
STRIPE_CANCEL_URL   = https://p4a.xyz/pages/test-store1.html?gear=cancelled
ORDER_SHEET_ID      = the sheet id from step 2
```

Script properties are server-side. The public never sees them, which is why the
key is safe here and nowhere else.

## 4. Build the sheet tabs

In the Apps Script editor, select `setupGearBackend` from the function dropdown
and press **Run**. Approve the permissions prompt the first time.

Your Sheet should now have tabs: Orders, OrderItems, Products, ProductColours,
ProductSizes, DiscountTiers, ShippingEstimates, Events.

## 5. Deploy the web app

1. **Deploy > New deployment > Web app**.
2. Execute as: **Me**.
3. Who has access: **Anyone**. (This must be "Anyone", not "Anyone with Google
   account", or customers cannot check out.)
4. Deploy, then copy the **web app URL**. It looks like
   `https://script.google.com/macros/s/AKfy..../exec`.

## 6. Connect the storefront

Open `assets/store-config.js` and paste the URL:

```js
checkoutEndpoint: 'https://script.google.com/macros/s/AKfy..../exec',
```

Commit and push. That is the switch. Empty string = demo mode, URL = live.

## 7. Test with a fake card

Load the store, fill in name and email, hit **Pay securely by card**. Use
Stripe's test card:

```text
Card    4242 4242 4242 4242
Expiry  any future date
CVC     any 3 digits
```

Then check:

- You land back on the store with the green "Payment received" banner.
- A row appeared in the `Orders` tab of your Sheet.
- The payment shows in the Stripe dashboard (test mode).

If the button does nothing and the status line shows an error, see
Troubleshooting below.

## 8. Go live for real

1. In Stripe, complete account activation (identity + bank details).
2. Switch the dashboard out of test mode and copy the **live** secret key
   (`sk_live_...`).
3. Update `STRIPE_SECRET_KEY` in Apps Script properties.
4. **Re-deploy the web app.** Editing code or properties does not update the
   live deployment until you deploy again. This is the single most common way
   to end up wondering why nothing changed.
5. Do one real purchase on your own card, for a few dollars, and refund it. It
   is worth the 30c to know the money actually lands.

## Troubleshooting

**Button does nothing / "Failed to fetch"**
The web app is not deployed as "Anyone", or the URL is wrong. Re-check step 5.

**"Unknown website_product_id"**
The storefront offers a product the backend catalogue does not have. The two
catalogues (`script.js` `gearProducts` and `gear-checkout.gs` `PRODUCTS`) must
agree on IDs. This error is the backend refusing to trust the browser, which is
working as designed.

**Changed something and nothing happened**
Re-deploy the web app (step 5). Apps Script serves the last deployment, not
your latest save.

**Price looks wrong**
The backend recalculates every price from its own catalogue and ignores what the
browser claims. If they disagree, the backend wins, and it is right to.

## Why it is built this way

The browser is never trusted. It builds an order and asks; Apps Script prices it
again from its own catalogue, creates the Stripe session, and logs the row. A
customer who edits the page can change what they *ask* for, but not what they
*pay*.

You own the storefront and the customer relationship. You rent only the payment
rail and the printing, and only per sale. Nothing is owed if nothing sells.
