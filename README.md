# p4a-xyz-cinema

<!-- github-organisation:start -->

## Project links and history

- First substantive build: 1 May 2026.
- GitHub repository: [p4a-xyz-cinema](https://github.com/auraofintelligence/p4a-xyz-cinema).
- Public site: [visit the public site](https://p4a.xyz/).

## Related public projects

Each link below reflects an evidenced family, lineage or direct connection. This project has 8 relevant public connections.

### Direct and other supported connections

- [right-place-right-time](https://github.com/auraofintelligence/right-place-right-time) - [public page](https://auraofintelligence.github.io/right-place-right-time/) - explicit cross-reference.

### P4A and Purple builds

- [p4a-native-nations-cinema](https://github.com/auraofintelligence/p4a-native-nations-cinema) - [public page](https://auraofintelligence.github.io/p4a-native-nations-cinema/) - earlier build; p4a-native-nations-cinema is later, explicit cross-reference, ordered build lineage, shared named build family.
- [p4a-oceania-cinema](https://github.com/auraofintelligence/p4a-oceania-cinema) - [public page](https://auraofintelligence.github.io/p4a-oceania-cinema/) - earlier build; p4a-oceania-cinema is later, explicit cross-reference, ordered build lineage, shared named build family.
- [p4a-oceania-expansion-lab](https://github.com/auraofintelligence/p4a-oceania-expansion-lab) - [public page](https://auraofintelligence.github.io/p4a-oceania-expansion-lab/) - parallel build, parallel builds in an ordered lineage, shared named build family.
- [p4a_xyz](https://github.com/auraofintelligence/p4a_xyz) - [public page](https://auraofintelligence.github.io/p4a_xyz/) - later build; p4a_xyz is earlier, explicit cross-reference, ordered build lineage, shared named build family.
- [P4Australia](https://github.com/auraofintelligence/P4Australia) - [public page](https://auraofintelligence.github.io/P4Australia/) - later build; P4Australia is earlier, explicit cross-reference, ordered build lineage, shared named build family.
- [purple01](https://github.com/auraofintelligence/purple01) - [public page](https://auraofintelligence.github.io/purple01/) - later build; purple01 is earlier, ordered build lineage, shared named build family.
- [Purple02](https://github.com/auraofintelligence/Purple02) - [public page](https://auraofintelligence.github.io/Purple02/) - later build; Purple02 is earlier, explicit cross-reference, ordered build lineage, shared named build family.

<!-- github-organisation:end -->

> 🤝🔷 **A Luke × Claude build.** Created by Luke Nathan Hayes (`auraofintelligence`) and Claude — Fable 5, July 2026. Original cinematic build credit; the October 2026 Victoria workbench and maintenance were developed with Codex. This is the cinematic rebuild fork of [p4a_xyz](https://github.com/auraofintelligence/p4a_xyz); the original Codex-era repo stays untouched upstream.

Static multi-page prototype for the Purple Party for Australia.

P4A is currently a proposed movement and drafting project, not a registered political party. The site is a public workbench for civic imagination, local-first democratic repair, transparent systems, constitutional literacy, public ledgers, state and region portals, legal-memory tooling and future cyber-republic rehearsal.


## Victoria workbench — implemented October 2026

Start at the [Victoria portal](https://p4a.xyz/states/vic/), [electorate atlas](https://p4a.xyz/states/vic/map/) or [2026 election guide](https://p4a.xyz/states/vic/election/). The [homepage](https://p4a.xyz/) includes a Melbourne-calendar countdown to 28 November 2026 with election-day and post-election wording. [About](https://p4a.xyz/pages/about.html) separates working tools from proposals and gaps; the [site map](https://p4a.xyz/pages/site-map.html) lists the public rooms.

- Atlas: 88 Assembly districts, eight Council regions, 79 councils, eight unincorporated areas and 467 ward/electoral-structure records. Exact sourced geometry, search, map picking, public representative details and source-derived chamber seating work via `file://` and HTTP.
- Election directory: **482 records, checked 2 October 2026** — 407 Assembly and 75 Council across 14 affiliations. Announced/preselected status is not formal VEC nomination. Source conflicts and unknown coverage are retained; no incumbent recontest or Council ticket order is inferred.
- First Peoples: community reference links and separate public statutory RAP/RSA layers. These are not a national Country map; absence of a statutory polygon does not imply absence of Traditional Owners or rights.
- Evidence: dated current representation, 2022 election results, 2021 Census indicators and local-government population/roster sources. Council finance fields remain unavailable where source retrieval was blocked. Broader civic-ledger, contribution and constitutional rooms remain exploratory.

### Source files and local generation

`content/electorates/vic.md`, `content/councils/vic.json`, `content/first-peoples/vic.json`, `content/representatives/` and `content/elections/vic-2026.json` are the reviewed sources. The election JSON is also the source for atlas candidate cards. Check the data’s own date; clocks update automatically, political records do not.

```powershell
pwsh -NoProfile -File tools/build-state-sites.ps1 -StateSlug vic -SkipHistory
python tools/build-vic-election.py
python tools/build-vic-map.py
python tools/verify-vic-map.py
python tools/verify-vic-numbers.py
python tools/verify-vic-councils.py
python -m http.server 8766 --bind 127.0.0.1
```

Generators use checked local data, not network acquisition. Python and PowerShell 7 are used for generation; Node checks JavaScript. The website is static and needs no package install or backend. Full source boundary files and lossless delivery encodings are intentionally retained; initial map loads are substantial on slower connections. See `content/electorates/vic-implementation.md`, `tools/vic-qa/` and `tools/link-qa/` for implementation and dated QA evidence.

### Rights, limits and distinct siblings

The [source-use register](content/licences/vic-source-register.md) records third-party conditions. The existing [Strange But True Public Source Licence](LICENCE.md) remains unchanged and is **not an open-source licence**. Source-specific rights are not relicensed by this repository. A changed political-party/campaign, fundraising or commercial role requires review; non-commercial status alone does not settle electoral authorisation or finance obligations.

- [Native Nations of the World](https://auraofintelligence.github.io/p4a-native-nations-cinema/): global, nation-led Country, protocols, rights and self-description, with its own onboarding.
- [P4A Oceania](https://auraofintelligence.github.io/p4a-oceania-cinema/): regional places, relationships, political geography and shared currents.

Both are separate projects. The existing [Australian Treaty Atlas](pages/treaty-atlas.html) links to them without merging scopes. External web links open new tabs; internal navigation, downloads, mail and telephone links retain their intended behaviour.

## Two Ways To Localise It

There are now two intended reuse paths:

1. **Fork the repo** and customise the code, content and data files directly.
2. **Paste the agent prompt** in [LOCALISE_WITH_AN_AGENT.md](LOCALISE_WITH_AN_AGENT.md) into a capable coding agent and ask it to build a local self-similar version with your own variables.

The second path is for communities that want the pattern without needing to understand this codebase first.

## Current Site Shape

The homepage is a cinematic, chaptered doorway: Act I the spark (Twinkle), Act II the system, Act III the ground game (L1 outreach, field kit, gear), Act IV the origin, Act V the culture layer, then the open-scaffold invitation. The deeper work is split into clearer pages:

- Architecture: roots-up civic model and flexible scale layers
- Twinkle: public gripe series
- Rabbit Hole: deeper campaign map
- Gear: support bundles and deployment materials
- Music: culture layer
- States: Australian state and territory portals
- History: state history pages generated from markdown
- Constitution: draft constitution workbench
- Law: legal-memory and Legal RAG direction
- Ledger: public records and trust infrastructure

Current political and historical data should live in reviewed Markdown or JSON under `content/` so future agents can refresh it with permission.

## Refreshing Election Data

By-elections, seat splits, leadership and election dates are agent-refreshable. `content/refresh-watchlist.md` is the trigger map (signals, source-of-truth order, exact recipe); `content/refresh-log.md` records every check, including no-change runs; [REFRESH_WITH_AN_AGENT.md](REFRESH_WITH_AN_AGENT.md) is the paste-able prompt. A run where nothing changed reads two small files per state and writes one log line.

## Navigation System

Every page shares a compact header (six primary doors plus an Index button) and a full-screen searchable index of all public rooms. The whole navigation layer — index overlay, breadcrumbs and footer explore-columns — is generated from one data file: `assets/site-nav.js`. To surface a new page everywhere, add one entry to the `SECTIONS` list in that file. No other page needs touching.

Without JavaScript the static header links and the site-map page still cover the whole site.

`tools/apply-chrome.mjs` is the re-runnable migration script that stamps the shared header and script includes across all pages.

## Typography and Performance

The site self-hosts two variable fonts in `assets/fonts/` (Archivo for display and body, JetBrains Mono for labels and data) so it stays offline-first with no CDN calls. Legacy family names in older CSS rules are aliased to these files via `@font-face`.

## Open Civic Scaffold

The goal is not only for Australia to turn purple. The broader hope is that other communities, regions and countries can adapt the scaffold for their own lawful, local, democratic repair work as the age of super intelligence changes what government can be.

Local versions should not impersonate P4A or imply endorsement. They should use their own name, values, sources, people, laws, histories and public accountability.

## Colour Direction

The site uses royal purple as the dominant environment, with amethyst neon, plasma magenta, solarpunk green and signal gold for navigation through the rabbit hole.

## Preview

Open `index.html` in a browser, or refresh the existing in-app browser tab.

## Licence

See [LICENCE.md](LICENCE.md) for the P4A public licence covering public-interest reuse, attribution, creative works, and the current pre-party status of the movement.

---

Built on Minjerribah by Luke × Claude.


<!-- mutual-futures-connection -->
## Mutual Futures: connected workbench

[Mutual Futures](https://auraofintelligence.github.io/mutual-futures/) connects this project with Luke Nathan Hayes's proposed mutual business succession, Try Everything Once, Intermittent Retirement, personal intelligence, legal reflection, resilience, travel and wider civilisational horizon. The connection does not merge the projects or imply outside endorsement.

[Source repository](https://github.com/auraofintelligence/mutual-futures) · [Project connections and sources](https://auraofintelligence.github.io/mutual-futures/sources.html)


## Homepage issue ticker

`content/home-ticker.json` contains dated issue headlines, jurisdiction labels, primary sources and editorial limits. Run `python tools/build-home-ticker.py` after a reviewed refresh. The ticker pauses on hover and keyboard focus, offers pause/play and touch-friendly links, respects reduced motion, and excludes animation clones from keyboard navigation. Prior topics are archived under `content/archive/`. It is not an automated breaking-news feed.


## Sitemap election calendar and shared navigation

`content/elections/state-election-calendar.json` records source-checked general-election dates, time zones and statutory-date qualifications. `assets/state-election-calendar.js` carries the same snapshot for file and HTTP use: update both together after a commission announcement. Fixed dates count calendar days locally; Tasmania has no invented exact date. Passed dates move below upcoming dates pending review; they never silently roll forward four years. All shared footers use top-aligned natural-height link groups. Sitemap directory links use explicit `index.html` paths for local-file compatibility.

Connected projects are maintained in `content/connected-projects.json`; run `python tools/build-connected-projects.py` to refresh the seven reviewed cards and contextual links in existing pages. Other inherited cards remain in `pages/site-map.html`. The legacy `#official-links-out` anchor remains compatible and `#connected-projects` is an alias. The 2 October approved batch adds Australian Law: Luke’s Relevance, C-Hour introduction, Aura Direct Hardware and Mutual Futures.
