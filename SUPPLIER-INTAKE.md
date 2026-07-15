# Adding a merch supplier

The process is the product. Anyone should be able to add a supplier to the P4A
store without asking Luke, and anyone should be able to check the work
afterwards. This file is how.

The rule underneath all six steps: **a price without a captured date is not a
price, it is a rumour.** The store would rather show "no quote yet" forever than
show a number it cannot stand behind.

## Step 1: Find, local first

Search your own town before you search the internet: printers, signwriters,
embroiderers, promo suppliers, op-shops.

Log everyone you find in the notes, including the ones you decide against, and
why. The next crew in the next town should inherit your search, not repeat it.

Only look further afield when nothing local can do the job. Local first is not
sentiment; it is the whole point of a party that says the money should stay
where the table stands.

## Step 2: Request a real quote

Send this. Adapt the tone, keep the fields.

```text
Subject: Quote request: purple [item], community group

G'day,

I'm with a community/political project on [place]. Looking for a quote on:

- Item: [e.g. purple pullover hoodie, unisex]
- Colour: purple (I'll need to see your available purples)
- Decoration: [screen print / embroidery] , [1 or 2] positions
- Artwork: vector supplied

Could you please quote:
  - Unit price at 1, 10, 25, 50 and 100
  - Any setup or screen fees, one-off or per order
  - Minimum order quantity
  - Lead time from artwork approval
  - What the blank is and where it's made, if you know

We publish our costs openly, so I'll be listing the price and the date you
quoted it. Happy to send the artwork whenever suits.

Thanks,
[name]
```

That last paragraph is not a throwaway. Telling a supplier up front that their
price will be public, with a date on it, filters out anyone who wants to quote
you one thing and charge another.

## Step 3: Screen the ethics

Two questions, both answerable:

1. **Who makes the blank, and where?** You will not always get an answer. Record
   the answer you got, including "they didn't know", which is itself data.
2. **What claims would we be repeating?** If a supplier says "ethically made"
   and cannot show you what that means, we do not print the claim on our page.
   The Truth Engine rule applies to suppliers exactly as it applies to Twinkles:
   if we cannot check it, we do not say it.

A supplier who fails the screen can still be used, as long as the page says
plainly what we know and do not know. What is not allowed is laundering an
unchecked claim into P4A's voice.

## Step 4: Sample before selling

Order one. Pay for it yourself. Then:

- Photograph it in daylight, and put the photo in `assets/gear-products/`.
- Check the purple against the brand. "Purple" covers a lot of sins.
- Wash it. Twice. Does the print crack?

This step costs about $60 and saves you from fifty volunteers in a shirt that
went grey after one wash. It is cheaper to learn now.

If the sample is bad, log it in the supplier notes and move on. A negative
result is a result, and it belongs in the record.

## Step 5: Record it, with a date

Open `assets/gear-catalogue.js`.

Add the supplier:

```js
{
  id: 'kebab-case-id',
  name: 'Supplier name and town',
  role: 'What they do for us',
  status: 'verified',
  last_verified: '2026-08-03',   // the day they quoted you. Not today. Not the commit date.
  note: 'Lead time, minimums, anything the next person needs.'
}
```

Add each item's price:

```js
{
  id: 'purple-tee',
  label: 'Purple tee',
  decoration: 'screen print',
  pricing: {
    mode: 'verified',
    single: 34.00,
    floor: 24.50,               // best price at the top quantity break
    last_verified: '2026-08-03',
    supplier: 'kebab-case-id'
  }
}
```

`last_verified` is the date on the quote. Not the day you typed it up, not the
day you committed the file. If you do not have the date, you do not have a
price: use `mode: 'quote_needed'` and leave the numbers out.

The pricing modes, in full:

| Mode | Meaning | Shows a number? |
| --- | --- | --- |
| `verified` | Real quote, real date, named supplier | Yes, with its date |
| `stale` | Was verified, now over 90 days old | Yes, flagged stale |
| `reference` | Old figure, provenance unclear, planning only | Yes, greyed, marked not buyable |
| `quote_needed` | No quote captured | No |

## Step 6: Publish, then re-quote

Commit and push. The store renders the price with its date, and ages it for you:
after 90 days it flags itself stale without anyone remembering to.

That automation is the point. The failure mode for every honest store is not
lying, it is forgetting: a number sits there for two years quietly becoming
false. So the page does the remembering.

When it flags stale, do one of two things:

- Re-quote (back to step 2), or
- Set `mode: 'reference'` so it stops pretending to be buyable.

Never just change the date to make the badge go green. That is the one
unforgivable move in this whole file, and it is exactly the move the rest of
the site exists to argue against.

## Backend catalogue

The checkout backend keeps its own copy of the catalogue in
`backend/google-apps-script/gear-checkout.gs` (`PRODUCTS`), and it re-prices
every order from that copy rather than trusting the browser.

That means a product must exist in **both** files to be sellable. If they
disagree, checkout fails with "Unknown website_product_id", which is the backend
correctly refusing to trust the front end. Update both, and re-deploy the web
app (see `backend/google-apps-script/GO-LIVE.md`).

## Why this is so fussy

Because the store is rung zero of a ladder that ends at a public ledger and a
real party. If we cannot keep an honest price list for eight hoodies, nobody
should believe us about donation disclosure or resource royalties.

The store is the first thing the movement audits. It should be the easiest thing
to audit.
