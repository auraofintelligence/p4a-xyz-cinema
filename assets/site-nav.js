(() => {
  if (window.P4A_LINKS || document.querySelector('script[data-p4a-link-policy]')) return;
  const policy = document.createElement('script');
  policy.src = new URL('external-links.js', document.currentScript.src).href;
  policy.dataset.p4aLinkPolicy = '';
  document.head.append(policy);
})();

/*
 * P4A site chrome.
 * One data file describes every public room. The header, full-screen index,
 * breadcrumbs and footer explore-columns are all generated from it, so new
 * pages only need an entry here to appear everywhere.
 * Progressive enhancement: without JS the static header links and the
 * site-map page still cover the whole site.
 */
(() => {
  document.documentElement.classList.add('js');

  /* Resolve the site root from the styles.css link, so this works from
     index.html, pages/ and states/xx/room/ alike. */
  const styleLink = document.querySelector('link[rel="stylesheet"][href*="styles.css"]');
  const P = styleLink ? styleLink.getAttribute('href').split('styles.css')[0] : './';

  const STATES = [
    { slug: 'qld', name: 'Queensland' },
    { slug: 'nsw', name: 'New South Wales' },
    { slug: 'vic', name: 'Victoria' },
    { slug: 'wa', name: 'Western Australia' },
    { slug: 'sa', name: 'South Australia' },
    { slug: 'tas', name: 'Tasmania' },
    { slug: 'act', name: 'ACT' },
    { slug: 'nt', name: 'Northern Territory' }
  ];

  const SECTIONS = [
    {
      id: 'start',
      num: '01',
      label: 'Start here',
      blurb: 'The front door, the origin story and the maps that keep your bearings.',
      links: [
        { href: 'index.html', title: 'Home', note: 'The doorway to the whole workbench.' },
        { href: 'pages/joke.html', title: 'Started as a friendly bet', note: 'The origin note, before the machinery gets formal.' },
        { href: 'pages/rabbit-hole.html', title: 'Rabbit-hole policies', note: 'All 49 policy solutions, key civic systems and connected source projects.' },
        { href: 'pages/markdown-with-ai.html', title: 'Markdown with AI', note: 'Plain-English guide to .md files as civic memory.' },
        { href: 'pages/maps.html', title: 'Geographic maps', note: 'Victoria electorates, councils, public recognition and state geography.' },
        { href: 'pages/site-map.html', title: 'Site map tree', note: 'Every public room, one clickable tree.' }
      ]
    },
/* key-policy-navigation:start */
{"id": "key-policies", "num": "Key", "label": "Key policy ideas", "blurb": "The core proposals connecting the Twinkle solutions.", "links": [{"href": "pages/rabbit-hole.html#key-c-hour", "title": "C-Hour", "note": "Recognise a verified voluntary hour of care, teaching or community work alongside ordinary money and paid work. C-Hours would have no fixed dollar equivalent and would not replace wages."}, {"href": "pages/rabbit-hole.html#key-worker-mutuals", "title": "Worker mutuals", "note": "Help workers gain a shared stake in productive businesses through willing succession, patient finance, mentoring and learning as they go. Mutual Futures connects ownership with livelihoods, care and time."}, {"href": "pages/web3-sensorium.html", "title": "Web3 Sensorium", "note": "Build the missing middle between a household laptop and a corporate data centre: community-scale computing, sovereign data and useful models of places, services and possible futures."}, {"href": "pages/aura-genesis.html", "title": "Aura Genesis", "note": "Explore consent-led AI reflection, digital memoirs and personal intelligence, with separate paths into civic trust, care research and creative worldbuilding."}, {"href": "pages/truth-engine.html", "title": "Truth Engine", "note": "Make public claims traceable: show sources, uncertainty, contested interpretations and visible corrections. Connect honest politics to public evidence and accountability."}, {"href": "pages/legal-rag.html", "title": "Legal RAG", "note": "Use retrieval-augmented generation: find the relevant legal sources, explain their wording and follow the citations back. Connect Luke’s Relevance and the Legal Engine to contracts, disputes and reform design."}, {"href": "pages/cyber-republic.html", "title": "Cyber-Republic Simulator", "note": "Let people explore proposed constitutional and democratic changes before choosing them. Compare rules, powers and consequences through a public rehearsal that people can inspect and improve."}]},
/* key-policy-navigation:end */
    {
      id: 'spark',
      num: '02',
      label: 'The spark',
      blurb: 'Twinkle: an open short-clip format for the obvious gripes. 49 Twinkles, anyone can film. The way in, not the whole system.',
      links: [
        { href: 'pages/twinkle.html', title: 'Twinkle series', note: 'The format, all the seeds and the credibility ledger.' },
        { href: 'pages/twinkle-tolls.html', title: 'Twinkle 01: Tolls', note: 'Commuter pain, into Public Assets.' },
        { href: 'pages/twinkle-food.html', title: 'Twinkle 02: Food', note: 'Grocery shock, into Food Security.' },
        { href: 'pages/twinkle-insurance.html', title: 'Twinkle 03: Insurance', note: 'Premium pressure, into Risk and Mutual Care.' },
        { href: 'pages/twinkle-workforce.html', title: 'Twinkle 04: Workforce', note: 'AI job shock, into Workforce Transition.' },
        { href: 'pages/twinkle-housing.html', title: 'Twinkle 05: Housing', note: 'Renter maths, into Housing Simulations.' },
        { href: 'pages/twinkle-power.html', title: 'Twinkle 06: Power bills', note: 'Rebate-cliff shock, into Public Assets.' },
        { href: 'pages/twinkle-health.html', title: 'Twinkle 07: Health', note: 'Gap-fee pain, into the Aura Clinical Path.' },
        { href: 'pages/twinkle-family-violence.html', title: 'Twinkle 08: Family violence', note: 'A quiet one. Aimed at the system, into safe housing on demand.' },
        { href: 'pages/twinkle-childcare.html', title: 'Twinkle 09: Childcare', note: 'Fees that eat a pay packet, into care funded as infrastructure.' },
        { href: 'pages/twinkle-beer-tax.html', title: 'Twinkle 10: Beer tax', note: 'The pub test in a pub, into the Civic Ledger.' },
        { href: 'pages/twinkle-datacentres.html', title: 'Twinkle 11: Data centres', note: 'The local infrastructure bargain, into the Web3 Sensorium.' },
        { href: 'pages/twinkle-breaches.html', title: 'Twinkle 12: Data breaches', note: 'Breach fatigue, into the Sovereignty Stack.' },
        { href: 'pages/twinkle-resources.html', title: 'Twinkle 13: Resources', note: 'Dig it up, ship it out, buy the feed. Into Public Assets and the Civic Ledger.' },
        { href: 'pages/twinkle-triple-zero.html', title: 'Twinkle 14: Triple Zero', note: 'Four bars of 5G, zero for Triple Zero, into the Sovereignty Stack.' },
        { href: 'pages/twinkle-aukus.html', title: 'Twinkle 15: AUKUS / defence spending', note: 'AUKUS commitments, opportunity costs and the public receipt.' },
        { href: 'pages/twinkle-revolving-door.html', title: 'Twinkle 16: Lobbying and conflicts', note: 'Lobbying, conflicts of interest and post-public-office employment.' },
        { href: 'pages/twinkle-donations.html', title: 'Twinkle 17: Donations', note: 'Who paid for that ad, into real-time disclosure.' },
        { href: 'pages/twinkle-olympics.html', title: 'Twinkle 18: Olympics', note: 'Venue whiplash, into the Civic Surges legacy: stewards, healing, referendum.' },
        { href: 'pages/twinkle-treaty.html', title: 'Twinkle 19: First Nations treaties', note: 'First Nations treaties, agreement-making and the Treaty Atlas.' },
        { href: 'pages/twinkle-uap.html', title: 'Twinkle 20: UAP disclosure', note: 'UAP observations, disclosure and source records in the Truth Engine.' },
        { href: 'pages/twinkle-deep-time.html', title: 'Twinkle 21: Climate change', note: 'Climate change, long planning horizons and public risk models.' },
        { href: 'pages/twinkle-ptsd.html', title: 'Twinkle 22: PTSD', note: 'PTSD, especially veterans and first responders: claims, care and repeated histories.' },
        { href: 'pages/twinkle-ai-copyright.html', title: 'Twinkle 23: AI copyright', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-child-safety.html', title: 'Twinkle 24: Child safety', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-online-safety.html', title: "Twinkle 25: Online safety", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-gender-pay-gap.html', title: "Twinkle 26: Gender pay gap", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-closing-the-gap.html', title: "Twinkle 27: Closing the Gap", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-youth-crime.html', title: "Twinkle 28: Youth crime", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-family-choices.html', title: "Twinkle 29: Wanted families", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-marriage-divorce.html', title: "Twinkle 30: Marriage & divorce", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-super-housing.html', title: 'Twinkle 31: Super for housing', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-wealth-inequality.html', title: "Twinkle 32: Wealth inequality", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-multinational-tax.html', title: 'Twinkle 33: Multinational tax', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-ndis-scams.html', title: "Twinkle 34: NDIS scams", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-ai-scams.html', title: "Twinkle 35: AI scams", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-aged-care-scams.html', title: "Twinkle 36: Aged-care scams", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-gambling-harm.html', title: "Twinkle 37: Gambling harm", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-fuel.html', title: 'Twinkle 38: Fuel tax', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-tobacco.html', title: 'Twinkle 39: Tobacco tax', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-migration-equations.html', title: "Twinkle 40: Migration equations", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-international-wars.html', title: "Twinkle 41: International wars", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-security-fallacies.html', title: "Twinkle 42: Security fallacies", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-ancient-aliens.html', title: 'Twinkle 43: Ancient aliens', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-mental-health.html', title: 'Twinkle 44: Mental health', note: 'Evidence, options and a deeper policy room.' },
        { href: 'pages/twinkle-psychedelic-mental-health.html', title: "Twinkle 45: Psychedelic care", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-restricted-plants.html', title: "Twinkle 46: Prohibited plants", note: 'A public question with policy follow-through.' },
        { href: 'pages/twinkle-super-investments.html', title: 'Twinkle 47: Super investments', note: 'My super. What is it buying?' },
        { href: 'pages/twinkle-political-lies.html', title: 'Twinkle 48: Political lies', note: "Political lies. But the ad's authorised." },
        { href: 'pages/twinkle-ai-pdoom.html', title: 'Twinkle 49: AI p(doom)', note: "AI extinction odds. Any odds on a fair go?" }
      ]
    },
    {
      id: 'system',
      num: '03',
      label: 'The system',
      blurb: 'The serious rooms underneath: architecture, policy foundations, law, ledgers and rehearsal.',
      links: [
        { href: 'pages/price-tax.html', title: 'Price and tax', note: 'Beer tax, resource rent and the public return.' },
        { href: 'pages/civic-pathway.html', title: 'Civic pathway', note: 'Origins, culture, organising and the broader civic journey.' },
        { href: 'pages/architecture.html', title: 'Civic architecture', note: 'Roots-up model: homes, neighbours, councils, states.' },
        { href: 'pages/constitution.html', title: 'Party constitution', note: 'The internal rulebook workbench.' },
        { href: 'pages/legal-rag.html', title: 'Law engine / Legal RAG', note: 'Legal memory, citations, limits, human review.' },
        { href: 'pages/about.html', title: 'About the workbench', note: 'What is implemented, source limits, project status and distinct sibling sites.' },
        { href: 'pages/treaty-atlas.html', title: 'Treaty atlas', note: 'Inherited agreements mapped: who they touch, who they serve, what to renew.' },
        { href: 'pages/civic-ledger.html', title: 'Civic ledger', note: 'Public records, contribution trails, repair memory.' },
        { href: 'pages/truth-engine.html', title: 'Truth engine', note: 'Claim labels, correction paths, public audit trails.' },
        { href: 'pages/sovereignty-stack.html', title: 'Sovereignty stack', note: 'Consent, identity, privacy and self-governance layers.' },
        { href: 'pages/fair-go.html', title: 'The fair go evolves', note: 'A familiar Australian value moved into modern systems.' },
        { href: 'pages/purple-synthesis.html', title: 'Purple synthesis', note: 'Market efficiency plus community reciprocity.' },
        { href: 'pages/braided-economy.html', title: 'Braided economy', note: 'Money, care, contribution, transparent support.' },
        { href: 'pages/housing-simulations.html', title: 'Housing simulations', note: 'Housing as a right: models, C-Hours, ending homelessness.' },
        { href: 'pages/public-assets.html', title: 'Public assets', note: 'Tolls, leases, ownership and long public memory.' },
        { href: 'pages/food-security.html', title: 'Food security', note: 'Waste, local production, logistics, resilience.' },
        { href: 'pages/community-insurance.html', title: 'Risk and mutual care', note: 'AI legal and contract support, then mutual protection.' },
        { href: 'pages/workforce-transition.html', title: 'Workforce transition', note: 'Worker mutuals, C-Hours, patient capital and AI learning.' },
        { href: 'pages/civic-surges.html', title: 'Civic surges', note: 'Volunteer energy and practical mobilisation.' },
        { href: 'pages/web3-sensorium.html', title: 'Web3 sensorium', note: 'Open data, digital twins, human-reviewed simulation.' },
        { href: 'pages/cyber-republic.html', title: 'Referendum rehearsal', note: 'A national simulator fed by local proof.' },
        { href: 'pages/family-violence.html', title: 'Violence against women', note: 'Safety, housing, prevention and recovery.' },
        { href: 'pages/ai-copyright.html', title: 'AI copyright', note: 'Public choices and participation.' },
        { href: 'pages/child-safety.html', title: 'Child safety', note: 'Public choices and participation.' },
        { href: 'pages/online-safety.html', title: "Online safety", note: 'Evidence, choices and participation.' },
        { href: 'pages/gender-pay-gap.html', title: "Gender pay gap", note: 'Evidence, choices and participation.' },
        { href: 'pages/closing-the-gap.html', title: "Closing the Gap", note: 'Evidence, choices and participation.' },
        { href: 'pages/youth-crime.html', title: "Youth crime", note: 'Evidence, choices and participation.' },
        { href: 'pages/family-choices.html', title: "Wanted families", note: 'Evidence, choices and participation.' },
        { href: 'pages/marriage-divorce.html', title: "Marriage & divorce", note: 'Evidence, choices and participation.' },
        { href: 'pages/super-housing.html', title: 'Super for housing', note: 'Public choices and participation.' },
        { href: 'pages/wealth-inequality.html', title: "Wealth inequality", note: 'Evidence, choices and participation.' },
        { href: 'pages/multinational-tax.html', title: 'Multinational tax', note: 'Public choices and participation.' },
        { href: 'pages/ndis-scams.html', title: "NDIS scams", note: 'Evidence, choices and participation.' },
        { href: 'pages/ai-scams.html', title: "AI scams", note: 'Evidence, choices and participation.' },
        { href: 'pages/aged-care-scams.html', title: "Aged-care scams", note: 'Evidence, choices and participation.' },
        { href: 'pages/gambling-harm.html', title: "Gambling harm", note: 'Evidence, choices and participation.' },
        { href: 'pages/fuel.html', title: 'Fuel tax', note: 'Public choices and participation.' },
        { href: 'pages/tobacco.html', title: 'Tobacco tax', note: 'Public choices and participation.' },
        { href: 'pages/migration-equations.html', title: "Migration equations", note: 'Evidence, choices and participation.' },
        { href: 'pages/international-wars.html', title: "International wars", note: 'Evidence, choices and participation.' },
        { href: 'pages/security-fallacies.html', title: "Security fallacies", note: 'Evidence, choices and participation.' },
        { href: 'pages/ancient-aliens.html', title: 'Ancient aliens', note: 'Public choices and participation.' },
        { href: 'pages/mental-health.html', title: 'Mental health', note: 'Public choices and participation.' },
        { href: 'pages/psychedelic-mental-health.html', title: "Psychedelic care", note: 'Evidence, choices and participation.' },
        { href: 'pages/restricted-plants.html', title: "Prohibited plants", note: 'Evidence, choices and participation.' },
        { href: 'pages/super-investments.html', title: 'Super investments', note: 'Holdings, fees, screens and member control.' },
        { href: 'pages/ai-pdoom.html', title: 'AI futures', note: 'Doom, protopia, a fair go and joyful responsible abundance.' }
      ]
    },
    {
      id: 'ground',
      num: '04',
      label: 'The ground game',
      blurb: 'Where it becomes real: local builders, the L1 outreach kit and visible support.',
      links: [
        { href: 'pages/starter-field-kit.html', title: 'Starter field kit', note: 'Market table, signs, QR trails, organiser basics.' },
        { href: 'pages/civic-twin-builders.html', title: 'Civic twin builders', note: 'L0 profiles, L1 meshes, L2 civic fronts.' },
        { href: 'pages/p4a-builder.html', title: 'P4A local builder', note: 'Build a self-similar local version of this site.' },
        { href: 'pages/private-civic-profile-builder.html', title: 'Private civic profile', note: 'The L0 starting point. Private by default.' },
        { href: 'pages/noticeboard-contract-builder.html', title: 'Noticeboard contracts', note: 'Public notices and local agreements as Markdown.' },
        { href: 'pages/c-hour-receipt-builder.html', title: 'C-Hour receipts', note: 'Contribution-hour receipts for the braided economy.' },
        { href: 'pages/minjerribah.html', title: 'Minjerribah', note: 'Island-scale thinking. The live L1 test ground.' },
        { href: 'pages/deployment-gear.html', title: 'Deployment gear', note: 'Support bundles, hoodies and culture objects.' },
        { href: 'pages/gear-store.html', title: 'Gear store (design test)', note: 'Not a shop. A rapid-iteration sketch: the ladder, kits, dated prices, open books.' },
        { href: 'pages/colour-panel.html', title: 'Colour panel', note: 'First principles: the exact purples, plus dyes, paints and threads. Images over words.' },
        { href: 'pages/test-store1.html', title: 'Gear test store (design test)', note: 'Checkout sketch. Takes no money; no keys connected.' }
      ]
    },
    {
      id: 'culture',
      num: '05',
      label: 'Culture',
      blurb: 'Songs, myth and the creative worlds that keep the rest human.',
      links: [
        { href: 'pages/musicverse.html', title: 'Musicverse', note: 'i C. infinity, P4A songs and culture hooks.' },
        { href: 'pages/aura-politics.html', title: 'Aura politics', note: 'AI, care, public trust and civic architecture.' },
        { href: 'pages/aura-genesis.html', title: 'Aura genesis', note: 'Myth, reflection and system imagination.' },
        { href: 'pages/aura-clinical-path.html', title: 'Aura clinical path', note: 'Health, dementia and assistive-tech caution.' },
        { href: 'pages/alien-necklace-film.html', title: 'Alien necklace film', note: 'Fiction threshold and creative world-building.' }
      ]
    },
    {
      id: 'states',
      num: '06',
      label: 'States and territories',
      blurb: 'Eight portals with election clocks, chamber maps, histories and constitution rooms.',
      links: [
        { href: 'states/vic/election/index.html', title: 'Victoria election 2026', note: 'Dates, participation routes and sourced candidate announcements.' },
        { href: 'states/vic/map/index.html?chamber=firstpeoples&recognition=rap,rsa', title: 'Victoria First Peoples recognition', note: 'Community sources, RAP and settlement recognition; not a complete map of Country.' },
        { href: 'states/vic/map/index.html', title: 'Victoria electorate atlas', note: 'Official district and region boundaries, current members and civic tools.' },
        { href: 'pages/states.html', title: 'National state map', note: 'All eight portals from one map.' },
        { href: 'pages/state-history.html', title: 'State histories', note: 'Jurisdiction histories generated from Markdown.' }
      ],
      states: true
    }
  ];

  const EXTERNAL = [
    { href: 'https://github.com/auraofintelligence/p4a-xyz-cinema', title: 'Fork on GitHub' },
    { href: 'https://github.com/auraofintelligence/p4a-xyz-cinema/blob/main/LOCALISE_WITH_AN_AGENT.md', title: 'Localise with an agent' },
    { href: 'https://auraofintelligence.github.io/strange-but-true/', title: 'Strange But True - live L1 example' },
    { href: 'https://auraofintelligence.github.io/p4a-native-nations-cinema/', title: 'Native Nations - global, nation-led Country, rights and self-description' },
    { href: 'https://auraofintelligence.github.io/p4a-oceania-cinema/', title: 'P4A Oceania - regional places, relationships and shared currents' },
    { href: 'https://auraofintelligence.github.io/strange-but-true-cosmic-nexus/', title: 'Cosmic Nexus - myth, UAP and travel atlas' },
    { href: 'https://auraofintelligence.github.io/strange-but-true-travel-oracle/', title: 'Travel Oracle - self-sovereign travel-life navigation' }
  ];

  /* Normalise: strip /index.html and .html so clean URLs match too. */
  const norm = (href) => new URL(href, location.href).pathname.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
  const here = norm(location.href);
  const isCurrent = (href) => norm(P + href) === here;

  /* ---------- Full-screen index ---------- */
  const sectionMarkup = (section) => {
    const links = section.links.map((link) => `
      <li data-index-item>
        <a href="${P}${link.href}"${isCurrent(link.href) ? ' aria-current="page"' : ''}>
          <strong>${link.title}</strong>
          <em>${link.note}</em>
        </a>
      </li>`).join('');
    const states = section.states ? `
      <ul class="index-states" aria-label="State and territory portals">
        ${STATES.map((s) => `<li data-index-item><a href="${P}states/${s.slug}/index.html"${isCurrent('states/' + s.slug + '/index.html') ? ' aria-current="page"' : ''}><strong>${s.slug.toUpperCase()}</strong><em>${s.name}</em></a></li>`).join('')}
      </ul>` : '';
    return `
    <section class="index-section" data-index-section>
      <header><span>${section.num}</span><h2>${section.label}</h2><p>${section.blurb}</p></header>
      <ul class="index-links">${links}</ul>
      ${states}
    </section>`;
  };

  const overlay = document.createElement('div');
  overlay.className = 'site-index';
  overlay.id = 'site-index';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', 'Site index');
  overlay.hidden = true;
  overlay.innerHTML = `
    <div class="index-shell">
      <div class="index-top">
        <p class="index-kicker">P4A / every public room</p>
        <label class="index-search">
          <span class="sr-only">Filter the index</span>
          <input type="search" placeholder="Type to filter the rooms…" data-index-search autocomplete="off">
        </label>
        <button class="index-close" type="button" data-menu-close aria-label="Close index">Close</button>
      </div>
      <p class="index-count" data-index-count aria-live="polite"></p>
      <div class="index-grid">${SECTIONS.map(sectionMarkup).join('')}</div>
      <footer class="index-foot">
        ${EXTERNAL.map((l) => `<a href="${l.href}" target="_blank" rel="noopener noreferrer">${l.title}</a>`).join('')}
      </footer>
    </div>`;
  document.body.appendChild(overlay);

  const toggles = Array.from(document.querySelectorAll('[data-menu-toggle]'));
  const closeBtn = overlay.querySelector('[data-menu-close]');
  const searchInput = overlay.querySelector('[data-index-search]');
  const countLabel = overlay.querySelector('[data-index-count]');
  const items = Array.from(overlay.querySelectorAll('[data-index-item]'));
  const sections = Array.from(overlay.querySelectorAll('[data-index-section]'));
  let lastFocus = null;

  const setCount = (visible) => {
    countLabel.textContent = visible === items.length
      ? `${items.length} rooms in the index`
      : `${visible} of ${items.length} rooms match`;
  };
  setCount(items.length);

  const filterIndex = () => {
    const q = (searchInput.value || '').trim().toLowerCase();
    let visible = 0;
    items.forEach((item) => {
      const match = !q || item.textContent.toLowerCase().includes(q);
      item.hidden = !match;
      if (match) visible += 1;
    });
    sections.forEach((section) => {
      const any = Array.from(section.querySelectorAll('[data-index-item]')).some((i) => !i.hidden);
      section.classList.toggle('is-empty', !any);
    });
    setCount(visible);
  };
  searchInput.addEventListener('input', filterIndex);

  const setExpanded = (value) => toggles.forEach((t) => t.setAttribute('aria-expanded', String(value)));
  const openIndex = () => {
    lastFocus = document.activeElement;
    overlay.hidden = false;
    document.body.classList.add('index-open');
    setExpanded(true);
    requestAnimationFrame(() => {
      overlay.classList.add('is-open');
      searchInput.focus({ preventScroll: true });
    });
  };
  const closeIndex = () => {
    overlay.classList.remove('is-open');
    document.body.classList.remove('index-open');
    setExpanded(false);
    const done = () => { overlay.hidden = true; };
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    reduced ? done() : setTimeout(done, 320);
    if (lastFocus?.focus) lastFocus.focus({ preventScroll: true });
  };

  toggles.forEach((t) => t.addEventListener('click', () => (overlay.hidden ? openIndex() : closeIndex())));
  closeBtn.addEventListener('click', closeIndex);
  overlay.addEventListener('click', (event) => {
    if (event.target === overlay) closeIndex();
  });
  document.addEventListener('keydown', (event) => {
    if (overlay.hidden) return;
    if (event.key === 'Escape') { closeIndex(); return; }
    if (event.key !== 'Tab') return;
    const focusables = Array.from(overlay.querySelectorAll('a, button, input')).filter((el) => !el.hidden && el.offsetParent !== null);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });

  /* ---------- Header state + scroll progress ---------- */
  const header = document.querySelector('.site-header');
  const progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  progress.innerHTML = '<i></i>';
  document.body.appendChild(progress);
  const progressBar = progress.firstElementChild;

  let ticking = false;
  const syncScroll = () => {
    ticking = false;
    const top = window.scrollY;
    header?.classList.toggle('is-condensed', top > 24);
    const depth = document.documentElement.scrollHeight - window.innerHeight;
    progressBar.style.transform = `scaleX(${depth > 0 ? Math.min(1, top / depth) : 0})`;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) { ticking = true; requestAnimationFrame(syncScroll); }
  }, { passive: true });
  syncScroll();

  /* ---------- Breadcrumb (topic pages only; state pages keep their layer strip) ---------- */
  const findPage = () => {
    for (const section of SECTIONS) {
      for (const link of section.links) {
        if (isCurrent(link.href)) return { section, link };
      }
    }
    return null;
  };
  const isHome = norm(P + 'index.html') === here;
  const onStatePage = document.body.dataset.statePage || here.includes('/states/');
  const found = findPage();
  if (!isHome && !onStatePage && header) {
    const crumb = document.createElement('nav');
    crumb.className = 'crumb-strip';
    crumb.setAttribute('aria-label', 'You are here');
    const sectionLabel = found ? found.section.label : 'Rooms';
    const pageLabel = found ? found.link.title : (document.querySelector('h1')?.textContent || document.title);
    crumb.innerHTML = `
      <a href="${P}index.html">Home</a>
      <span aria-hidden="true">/</span>
      <button type="button" data-crumb-index>${sectionLabel}</button>
      <span aria-hidden="true">/</span>
      <strong aria-current="page">${pageLabel}</strong>`;
    header.insertAdjacentElement('afterend', crumb);
    crumb.querySelector('[data-crumb-index]').addEventListener('click', openIndex);
  }

  /* ---------- Footer explore columns ---------- */
  document.querySelectorAll('footer.site-footer').forEach((footer) => {
    if (footer.hasAttribute('data-footer-compact')) {
      const existing=footer.querySelector(':scope > .footer-index');
      if(existing){existing.dataset.footerColumns=String(existing.children.length);return;}
      const nav=footer.querySelector(':scope > nav');if(!nav)return;
      const links=[...nav.querySelectorAll('a')];const split=Math.ceil(links.length/2);
      const headings=footer.classList.contains('ve-footer')?['Victoria','Sources and site']:['Project','Reference'];
      nav.replaceChildren();nav.className='footer-index';nav.dataset.footerColumns='2';
      for(let i=0;i<2;i++){const group=document.createElement('section'),heading=document.createElement('strong'),list=document.createElement('ul');heading.textContent=headings[i];for(const link of links.slice(i*split,(i+1)*split)){const li=document.createElement('li');li.append(link);list.append(li);}group.append(heading,list);nav.append(group);}return;
    }
    const explore = document.createElement('nav');
    explore.className = 'footer-index';
    explore.setAttribute('aria-label', 'Explore the workbench');
    explore.innerHTML = SECTIONS.map((section) => `
      <div>
        <strong>${section.label}</strong>
        <ul>${section.links.slice(0, 6).map((link) => `<li><a href="${P}${link.href}">${link.title}</a></li>`).join('')}
        ${section.states ? `<li class="footer-state-row">${STATES.map((s) => `<a href="${P}states/${s.slug}/index.html">${s.slug.toUpperCase()}</a>`).join('')}</li>` : ''}</ul>
      </div>`).join('');
    footer.insertAdjacentElement('afterbegin', explore);
  });

  /* ---------- Mark current page in the static header nav ---------- */
  document.querySelectorAll('.site-nav a').forEach((link) => {
    if (norm(link.getAttribute('href')) === here) link.setAttribute('aria-current', 'page');
  });
})();
