/*
 * P4A gear catalogue: the single data spine for the store.
 *
 * Rules this file enforces by shape, not by promises:
 * - Every price carries last_verified and status. Stale prices are shown as
 *   stale, never silently trusted. An unverified supplier says "unverified".
 * - pricing_mode is honest: 'fixed' only where we control the quote today,
 *   'range' for local-sourced items, 'quote' for anything that needs a real
 *   conversation before money moves.
 * - Local first. Affiliate links only where no local option exists, always
 *   labelled, and any affiliate income lands on the same public ledger as
 *   every other dollar. No links exist yet, and the empty list says so.
 */
window.P4A_CATALOGUE = {
  meta: {
    schema: 'p4a_gear_catalogue_v1',
    updated: '2026-07-15',
    pricing_note: 'Prices are evidence, not decoration: each carries the date it was last checked. Anything older than 90 days renders as stale.'
  },

  suppliers: [
    {
      id: 'dunwich-printer',
      name: 'Dunwich shirt printer, Minjerribah',
      role: 'Local print partner (first preference)',
      status: 'unverified',
      note: 'Not yet visited. No prices captured. Nothing sells through this lane until real quotes exist.'
    },
    {
      id: 'brisbane-supplier',
      name: 'Brisbane garment supplier (catalogue reference)',
      role: 'Overflow and reference pricing',
      status: 'stale',
      last_verified: '2026-07-07',
      note: 'Hoodie base prices captured July 2026 for the pilot. Treat as reference until re-quoted.'
    },
    {
      id: 'local-general',
      name: 'Your local hardware, op-shops and printers',
      role: 'Starter kit hardware, banners, cards',
      status: 'guidance',
      note: 'Kits are designed to be sourced in your own town first. The ranges below are honest estimates, not offers.'
    }
  ],

  wearables: [
    { id: 'gildan-adult-hooded-sweatshirt', label: 'Gildan Adult Hooded Sweatshirt', single: 52.95, floor: 39.71, last_verified: '2026-07-07', status: 'stale' },
    { id: 'ramo-sloppy-joe', label: 'RAMO Poly Cotton Fleece Sloppy Joe', single: 57.45, floor: 43.09, last_verified: '2026-07-07', status: 'stale' },
    { id: 'unisex-pullover', label: 'Unisex Adults Pull Over Hoodie', single: 59.99, floor: 44.99, last_verified: '2026-07-07', status: 'stale' },
    { id: 'ramo-kangaroo-pocket', label: 'RAMO Kangaroo Pocket Hoodie', single: 62.35, floor: 46.76, last_verified: '2026-07-07', status: 'stale' },
    { id: 'ramo-heavy-zip', label: 'RAMO Brushed Heavy Zip Fleece Hoodie', single: 65.00, floor: 48.75, last_verified: '2026-07-07', status: 'stale' },
    { id: 'ramo-zip-pocket', label: 'RAMO Zip Hoodie with Pocket', single: 77.20, floor: 57.90, last_verified: '2026-07-07', status: 'stale' },
    { id: 'ramo-heavy-fleece', label: 'RAMO Brushed Heavy Fleece Hoodie', single: 82.39, floor: 61.79, last_verified: '2026-07-07', status: 'stale' },
    { id: 'comfort-colorblast', label: 'Comfort Colors Color Blast Crewneck', single: 100.71, floor: 75.53, last_verified: '2026-07-07', status: 'stale' }
  ],

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
        { name: 'Password manager', source: 'free and open source options first', est: '$0' },
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
