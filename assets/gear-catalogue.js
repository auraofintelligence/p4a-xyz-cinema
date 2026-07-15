/*
 * P4A gear catalogue: the single data spine for the store.
 *
 * Pricing honesty rules, enforced by shape rather than by promises:
 *
 * - A price without a captured date is not a price. It is a rumour. Items with
 *   mode 'reference' carry provenance text instead of a fake date and are
 *   never presented as buyable.
 * - mode 'quote_needed' means exactly that: no number, no guess. Most of the
 *   spectrum sits here until a real supplier quotes it. That is the honest
 *   state of a store that has not opened yet.
 * - mode 'verified' requires last_verified (ISO date) and a supplier id. The
 *   renderer ages it automatically; over 90 days it flags itself stale.
 *
 * Adding a supplier or a price? Follow SUPPLIER-INTAKE.md. The process is the
 * product: anyone should be able to add a supplier without asking Luke.
 */
window.P4A_CATALOGUE = {
  meta: {
    schema: 'p4a_gear_catalogue_v2',
    updated: '2026-07-15',
    pricing_note: 'Every price carries its provenance or it carries nothing. Nothing here is buyable until a supplier is verified and a quote is dated.'
  },

  suppliers: [
    {
      id: 'dunwich-printer',
      name: 'Dunwich shirt printer, Minjerribah',
      role: 'Local print partner, first preference',
      status: 'visited',
      last_verified: '2026-05-11',
      note: 'Visited 11 May 2026. Quotes were discussed but never written into this catalogue, so there are still no numbers here. Intake step 2: get it in writing, with the date.'
    },
    {
      id: 'brisbane-supplier',
      name: 'Brisbane garment supplier',
      role: 'Reference pricing and overflow only',
      status: 'stale',
      last_verified: '2026-05-01',
      precision: 'approximate',
      note: 'Hoodie base prices captured early May 2026; the exact day was never recorded, so the date is deliberately set to the earliest plausible one and ages fastest. Reference only until re-quoted.'
    },
    {
      id: 'local-general',
      name: 'Your local hardware, op-shops, printers and signwriters',
      role: 'Starter kit hardware and signage',
      status: 'guidance',
      note: 'Kits are designed to be sourced in your own town first. Ranges are honest estimates, not offers.'
    }
  ],

  /*
   * Who we ask, in order. This ladder is the difference between a party store
   * and a Vistaprint account. Rank 5 exists so the rule can be broken honestly
   * and visibly, not quietly.
   */
  sourcing_ladder: [
    { rank: 1, name: 'Local to the table', detail: 'The printer, signwriter or maker in the town where the table stands. Money that stays local is the whole argument.' },
    { rank: 2, name: 'Indigenous-owned businesses', detail: 'Ask, invite, and let them onboard themselves on their own terms. We list nobody without consent and speak for nobody. Supply Nation is a real directory to search; Country and community come before our print run.' },
    { rank: 3, name: 'Community enterprise, co-ops, social enterprise', detail: 'Businesses that already answer to a community rather than a shareholder. Ask what their surplus does.' },
    { rank: 4, name: 'Independent makers running their own shop', detail: 'Sovereign in the plain sense: they own their gear, set their prices and answer the phone themselves.' },
    { rank: 5, name: 'Generic print mills', detail: 'The Vistaprint tier. Cheap, fast, soulless, and the last resort. If we ever use one, the page says so out loud and says why nothing above it could do the job.' }
  ],

  /*
   * Candidates, not a catalogue.
   *
   * The test for every line: would you wear or carry it if the politics were
   * stripped off? If it only works because of the logo, it is landfill with a
   * cause printed on it. That rule deleted the lanyards, the tea towel, the
   * ceramic mug, the button badges, the car magnet and the branded notebook.
   *
   * This list is a starting guess and is explicitly allowed to be wrong. What
   * gets quoted is what people ask for: see `requests` below.
   */
  merch: [
    {
      category: 'Worn',
      note: 'Good blanks, heavy cotton, boxy fits. The kind of thing that survives the movement it advertises.',
      items: [
        { id: 'purple-tee', label: 'Heavyweight boxy tee', decoration: 'screen print', pricing: { mode: 'quote_needed' } },
        { id: 'purple-crewneck', label: 'Crewneck sweater', decoration: 'screen print', pricing: { mode: 'quote_needed' } },
        { id: 'purple-cap', label: 'Embroidered cap', decoration: 'embroidery', pricing: { mode: 'quote_needed' } },
        { id: 'purple-beanie', label: 'Beanie', decoration: 'embroidery', pricing: { mode: 'quote_needed' } },
        { id: 'purple-socks', label: 'Socks', decoration: 'knitted', pricing: { mode: 'quote_needed' } }
      ]
    },
    {
      category: 'Hoodies, the pilot lane',
      note: 'The only lines with any numbers, and the numbers are old. Blanks quoted early May 2026 by a Brisbane supplier; the local Dunwich printer gets first refusal once a written quote exists.',
      items: [
        { id: 'gildan-adult-hooded-sweatshirt', label: 'Gildan Adult Hooded Sweatshirt', decoration: 'screen print', pricing: { mode: 'reference', single: 52.95, floor: 39.71, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'ramo-sloppy-joe', label: 'RAMO Poly Cotton Fleece Sloppy Joe', decoration: 'screen print', pricing: { mode: 'reference', single: 57.45, floor: 43.09, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'unisex-pullover', label: 'Unisex Adults Pull Over Hoodie', decoration: 'screen print', pricing: { mode: 'reference', single: 59.99, floor: 44.99, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'ramo-kangaroo-pocket', label: 'RAMO Kangaroo Pocket Hoodie', decoration: 'screen print', pricing: { mode: 'reference', single: 62.35, floor: 46.76, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'ramo-heavy-zip', label: 'RAMO Brushed Heavy Zip Fleece Hoodie', decoration: 'screen print', pricing: { mode: 'reference', single: 65.00, floor: 48.75, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'ramo-zip-pocket', label: 'RAMO Zip Hoodie with Pocket', decoration: 'screen print', pricing: { mode: 'reference', single: 77.20, floor: 57.90, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'ramo-heavy-fleece', label: 'RAMO Brushed Heavy Fleece Hoodie', decoration: 'screen print', pricing: { mode: 'reference', single: 82.39, floor: 61.79, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } },
        { id: 'comfort-colorblast', label: 'Comfort Colors Color Blast Crewneck', decoration: 'screen print', pricing: { mode: 'reference', single: 100.71, floor: 75.53, last_verified: '2026-05-01', precision: 'approximate', supplier: 'brisbane-supplier' } }
      ]
    },
    {
      category: 'Carried',
      note: 'Small, cheap, actually used. The sticker outlives the campaign.',
      items: [
        { id: 'sticker-pack', label: 'Sticker pack', decoration: 'digital print', pricing: { mode: 'quote_needed' } },
        { id: 'enamel-pin', label: 'Enamel pin', decoration: 'enamel', pricing: { mode: 'quote_needed' } },
        { id: 'patch', label: 'Iron-on patch', decoration: 'embroidery', pricing: { mode: 'quote_needed' } },
        { id: 'tote-bag', label: 'Canvas tote', decoration: 'screen print', pricing: { mode: 'quote_needed' } },
        { id: 'reusable-cup', label: 'Reusable cup', decoration: 'wrap print', pricing: { mode: 'quote_needed' } },
        { id: 'stubby-holder', label: 'Stubby holder', decoration: 'wrap print', pricing: { mode: 'quote_needed' } }
      ]
    }
  ],

  /*
   * Demand, not guesses. A request here is what puts an item into the quote
   * queue. Empty because nobody has been asked yet, and an empty list is a
   * truer thing to publish than a catalogue nobody wanted.
   *
   * Field gear (corflutes, banners, QR cards, hi-vis) is not merch and lives in
   * the kits below, where it belongs.
   */
  requests: [],

  kits: [
    {
      id: 'table-kit',
      name: 'One Table Kit',
      tagline: 'A real table in a real town. Rung one of the ladder.',
      pricing_mode: 'range',
      est_range: '$400 to $700 sourced locally',
      items: [
        { name: 'Folding table', source: 'local hardware or op-shop', est: '$60 to $120' },
        { name: 'Shade gazebo or umbrella', source: 'local hardware', est: '$100 to $180' },
        { name: 'P4A banner', source: 'local print shop', est: '$80 to $150' },
        { name: 'QR trail cards x250', source: 'local printer', est: '$30 to $60' },
        { name: 'Name badges x6', source: 'local printer or office supply', est: 'about $20' },
        { name: 'Sticker sheets x100', source: 'local printer', est: '$40 to $80' },
        { name: 'Clipboard, sign-up sheets, pens', source: 'office supply', est: 'about $15' },
        { name: 'Local issue cards', source: 'print at home, templates in the repo', est: 'about $10' },
        { name: 'Water, sunscreen, basic first aid', source: 'chemist and supermarket', est: 'about $40' }
      ]
    },
    {
      id: 'digital-kit',
      name: 'Digital Crew Kit',
      tagline: 'No cameras: three phones at a table already beat a media kit. This funds what a crew cannot pull from a pocket.',
      pricing_mode: 'range',
      est_range: '$50 to $200 per month, running cost not hardware',
      items: [
        { name: 'AI assistant seats for the crew', source: 'direct from providers, free tiers first', est: '$0 to $100 per month per seat' },
        { name: 'Domain name', source: 'any registrar', est: 'about $20 per year' },
        { name: 'Site hosting', source: 'GitHub Pages, same as this site', est: '$0' },
        { name: 'Online marketing / boosted posts', source: 'set a cap, publish the spend on the ledger', est: 'whatever the books can carry' },
        { name: 'Email and forms', source: 'free tiers first', est: '$0 to $20 per month' },
        { name: 'Twinkle seeds, templates, site pattern', source: 'free, this repo', est: '$0' }
      ]
    },
    {
      id: 'kiosk-kit',
      name: 'Disaster Kiosk Noticeboard',
      tagline: 'A public screen that keeps working when the towers do not. The NODE pillar, made of parts you can buy in town.',
      pricing_mode: 'range',
      est_range: '$500 to $1,200 depending on housing and power',
      items: [
        { name: 'Refurbished mini PC or Raspberry Pi', source: 'refurb dealers or local electronics', est: '$150 to $300' },
        { name: 'Screen (touch if the budget allows)', source: 'refurb or local electronics', est: '$150 to $400' },
        { name: 'Weatherproof housing', source: 'local fabricator or hardware', est: '$100 to $300' },
        { name: 'Battery / UPS so outages do not kill it', source: 'local electronics', est: '$100 to $250' },
        { name: 'Solar top-up (optional)', source: 'local solar supplier', est: 'quote' },
        { name: 'Offline-first noticeboard software', source: 'free, Straddie noticeboard pattern in the repo', est: '$0' }
      ]
    },
    {
      id: 'data-stack-kit',
      name: 'Self-Sovereign Data Stack',
      tagline: 'Your crew\'s records on your own shelf, not rented from a hyperscaler. The sovereignty stack with a power cord.',
      pricing_mode: 'range',
      est_range: '$600 to $1,000 one-off',
      items: [
        { name: 'Small home server (refurb NUC or Pi 5 kit)', source: 'refurb dealers or local electronics', est: '$150 to $400' },
        { name: 'Two storage drives (working copy plus backup)', source: 'local electronics', est: '$200 to $300' },
        { name: 'Hardware security keys x2', source: 'online, no local option usually exists', est: 'about $150' },
        { name: 'Battery / UPS', source: 'local electronics', est: 'about $100' },
        { name: 'Password manager, local-first: KeePassXC file, or Vaultwarden on the server above', source: 'free and open source. A cloud vault inside a sovereignty kit is a contradiction. There is no vendor to email if you lose it, so the backup drive above IS the recovery plan', est: '$0' },
        { name: 'Local-first profile and ledger patterns', source: 'free, private civic profile builder in the repo', est: '$0' }
      ]
    },
    {
      id: 'branch-kit',
      name: 'Branch in a Box',
      tagline: 'Table kit plus crew kit plus the volunteer layer.',
      pricing_mode: 'quote',
      est_range: 'Quoted per region once a local printer is confirmed',
      items: [
        { name: 'Everything in the One Table Kit', source: 'as above', est: 'range above' },
        { name: 'Digital Crew Kit running costs, first six months', source: 'as above', est: 'range above' },
        { name: 'Volunteer shirts x6', source: 'local print partner', est: 'quote' },
        { name: 'A-frame footpath sign', source: 'local signage shop', est: '$120 to $200' },
        { name: 'Cash tin and QR payment stand', source: 'office supply', est: 'about $50' },
        { name: 'Printed admin pack: consent notes, correction log, handover sheet', source: 'free, templates in the repo', est: 'printing only' }
      ]
    }
  ],

  /*
   * Supplier intake: the duplicable process. Stages are deliberately gated so a
   * supplier cannot appear in the store before it has been checked. The full
   * detail lives in SUPPLIER-INTAKE.md; this is the machine-readable spine.
   */
  intake: [
    { step: 1, name: 'Find, local first', detail: 'Search your own town before anywhere else: printers, signwriters, embroiderers. Log who exists, even the ones you do not use.' },
    { step: 2, name: 'Request a real quote', detail: 'Use the quote template. Ask for price at 1, 10, 25, 50 and 100, lead time, minimum order, decoration method and setup fees.' },
    { step: 3, name: 'Screen the ethics', detail: 'Who makes the blank, and where? Any labour or environmental claims we would have to repeat? If we cannot check a claim, we do not print it on the page.' },
    { step: 4, name: 'Sample before selling', detail: 'Order one. Photograph it. If the purple is wrong or the print cracks, that is cheaper to learn now than after fifty volunteers wear it.' },
    { step: 5, name: 'Record with a date', detail: 'Add the supplier and every price to gear-catalogue.js with last_verified set to the day you were quoted. No date, no listing.' },
    { step: 6, name: 'Publish and re-quote', detail: 'The store shows the price with its date. After 90 days it flags itself stale automatically. Re-quote or let it expire; never quietly leave an old number up.' }
  ],

  affiliates: {
    policy: [
      'Local suppliers first, every time. An affiliate link is a fallback, not a business model.',
      'Every affiliate link is labelled as one, next to the link, not in fine print.',
      'Affiliate income lands on the same public ledger as every other dollar.',
      'No affiliate deal that requires hiding the local option.'
    ],
    links: []
  }
};
