# P4A civic workbench

This is the `p4a-xyz-cinema` source for [p4a.xyz](https://p4a.xyz): connected places, everyday questions, evidence, public decisions and possibilities for meaningful change.

## Find your way


The national expansion resumed on 17 October 2026. [Find a council, state electorate or federal area](pages/places.html) across all eight jurisdictions. The [23 October publication review](docs/releases/2026-10-23-national-expansion-publication.md) and [resumed implementation report](docs/releases/2026-10-17-national-expansion-resumed.md) record coverage, evidence and remaining source/journey gaps. These new place routes preserve the deeper Victoria and Redlands workbenches; no new Twinkles were authored for the expansion.

Start with the [human-readable site map](pages/site-map.html). It groups the whole site by what you want to do, rather than by filenames.

| I want to… | Start here |
| --- | --- |
| Find my place | [Councils and electorates](pages/places.html) → choose a jurisdiction and institution |
| Explore the full local example | [Redlands](states/qld/councils/redland/index.html) → [choose a division](states/qld/councils/redland/divisions/index.html) |
| Follow a connection | [Connected systems and public evidence](states/qld/councils/redland/explore/index.html) |
| Explore wider systems | [Connected possibilities](states/qld/councils/redland/possibilities/index.html) |
| Examine people and decisions | [Public records and elections](states/qld/councils/redland/candidates/index.html) |
| Contribute or see what changed | [Take part](states/qld/councils/redland/action/index.html) · [Outcomes](states/qld/councils/redland/outcomes/index.html) |
| Inspect Victoria's existing electorate work | [Victorian state electorate atlas](states/vic/map/index.html) |
| Review page dates and sources | [Page and rule update register](docs/releases/2026-10-17-page-and-rule-register.md) · [Sources and dates](states/qld/councils/redland/sources/index.html#review-register) |
| Build another place with an agent | [Read the agent entry rules](AGENTS.md), then the separate council, state or federal guide |
| Update one election, member, countdown or linked page | [Fractal election and navigation updates](docs/agents/fractal-election-updates.md), including individual by-elections, previous contestants, profiles and sitemap maintenance |
| Prepare a GitHub upload | [Upload instructions](docs/github-upload.md) |

**Local preview:** run `node scripts/serve.mjs` in this folder, then open [the local site map](http://127.0.0.1:8768/pages/site-map.html). The [public site map](https://p4a.xyz/pages/site-map.html) shows the deployed version; GitHub's commit history and Pages run record its publication status.

**Latest implementation updates:** 17 October 2026, Australia/Brisbane. Nineteen new Redlands/council pages and the rules have explicit review records. Source facts retain their own observation, boundary-edition and check dates; rebuilding a page does not make its data newer.

## Search discovery and rights

Added 17 October 2026, following the recent Aura Genesis repository pattern: [robots.txt](robots.txt) points search crawlers to the [XML sitemap](sitemap.xml), and [llms.txt](llms.txt) provides a voluntary guide for assistants. These discovery files preserve the [Strange But True Public Source Licence](LICENCE.md) and third-party rights; they grant no additional reuse or AI-training permission. The crawl policy welcomes search discovery and separately signals a GPTBot training opt-out. These are cooperative signals, not enforcement or a promise of indexing.

Run `python tools/build-human-site-map.py` after adding or retiring public pages; it rebuilds the human directory, page inventory and discovery files together. Run `python tools/verify-discovery.py` to check coverage, supported update dates, crawler rules and the unchanged licence. See the [discovery and rights maintenance notes](docs/discovery-and-rights.md) for the examples and review triggers.

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

## Redland local journey - first pass, 16-17 October 2026

Agent replication now starts at [AGENTS.md](AGENTS.md), with separate [council](docs/agents/council-journey-rules.md), [state electorate](docs/agents/state-electorate-journey-rules.md) and [federal electorate](docs/agents/federal-electorate-journey-rules.md) guides. They share the [civic place contract](docs/agents/local-place-pattern.md), [acceptance gates](docs/agents/council-build-acceptance.md) and a completion report. Check [existing coverage](docs/agents/existing-place-coverage.md) and the [Victoria–Redlands lessons](docs/agents/victoria-redlands-lessons.md) before extending a place. Victoria already has its state atlas/data foundation; that is distinct from a full per-electorate civic deep dive. Federal Bowman material remains contextual coverage.

Run `python tools/verify-place-contracts.py` to check all reviewed manifests named `*-pattern-contract.json` under `content/`. New places register their own properly adapted contract. The included GitHub Actions workflow repeats structural/source-integrity checks after upload; browser, editorial and original-source reviews still have explicit acceptance requirements. [GitHub preparation](docs/github-upload.md) explains the clean public-source bundle and upload status.

The 17 October correction puts the same draggable, zoomable, searchable atlas on the Queensland portal, council directory and Redlands division journey. Actual Queensland Government boundary geometry overlays the official QldBase Pastel PNG in shared EPSG:3857 coordinates. Soft colours distinguish areas; gold marks selection. Faint grey roads stay in the quiet default, with detailed topographic roads optional. Marine areas remain transparent, so the actual coast and islands stay visible. All 77 councils plus Weipa Town Authority are selectable; Redlands opens one interactive map of its ten divisions, each leading to a sourced local overview. Historical maps remain on Sources & dates. No SVG map is used. Tablet navigation wraps without overlapping text. Attribution, unchanged geometry, original PNGs, returned extents and refresh notes are retained in `content/councils/qld-map-sources.json`, `qld-basemap-sources.json` and `redland-divisions-sources.json`.

The existing States map uses an attributed Wikimedia PNG with accessible state-label links. Follow Queensland -> councils -> Redland City -> a division. The 19-page local example includes 18 dated indicators, 19 connected records, wider systems, public-record pathways, participation, outcomes and the cost/free-contribution/change trinity. The 24 invented local Twinkle seeds were removed on 1 November 2026; national Twinkles are unchanged. Personal Genesis reflection is optional within candidates. No individual is announced as a candidate.

Run `node scripts/serve.mjs` in this checkout, then open [the local States entry](http://127.0.0.1:8768/pages/states.html) or [the local Redlands overview](http://127.0.0.1:8768/states/qld/councils/redland/index.html). The server binds only to this computer. This build has not been published.

`content/councils/redland.json`, `content/local/redland-connections.json` and `content/local/redland-election.json` hold reviewed source records. Run `python tools/build-redland.py`, `python tools/verify-redland.py` and `node tools/check-redland-clock.mjs` after scoped changes. The local generator also restores its marked entry links after another state/room generator has run; it preserves surrounding content. Research dates do not advance when pages regenerate.

The live clock targets the rule-derived scheduled local election day, 25 March 2028, subject to the official timetable and any regulation. Early voting and a possible mayoral by-election have independent null dates until official notices establish them. The UI supports a sourced early-voting window without inventing one now. See [the repeatable agent pattern](docs/agents/local-place-pattern.md), [dated change history](content/history/redland.md) and each map's source-specific rights. Historical numbers printed on a boundary map are not current enrolment.

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
- Rabbit-hole policies: all 49 Twinkle solutions and seven key civic systems.
- Civic pathway: the preserved journey through origins, culture, organising and civic design.
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

Every page shares a compact header (six primary doors plus an Index button) and a full-screen searchable index of public rooms. `assets/site-nav.js` supplies the shared index, breadcrumbs and footer links. New pages also need their real parent/directory links, canonical generator changes and discovery updates; follow [the sitemap and link procedure](docs/agents/fractal-election-updates.md#7-maintain-sitemap-navigation-and-links). Keep large place directories within their appropriate council/electorate entry points.

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


## October 2026 Twinkles and public rooms

The workbench now has 49 Twinkles. `content/public-topic-inventory.json` maps Luke's 24-topic expansion to its actual Twinkle and deeper room, alongside the previously approved AI copyright, broader mental health and Sensorium work; `followupTopics` records the separate super-investment transparency addition. The original 22 Twinkles and their media remain; new topics extend the sequence. Migration equations, International wars and Security fallacies are distinct rooms. Marriage and divorce is one doorway into Global Group Marriages and U.N. of Love. Tobacco tax and Prohibited plants are separate.

Reviewed page HTML is authoritative in `content/rooms/`. Publish it with `python tools/build-policy-rooms.py`; optional stem arguments limit the run. These sources preserve each existing room's artwork, media and chrome. When refreshing connected projects, run `python tools/build-connected-projects.py` first, then publish rooms: that generator updates the canonical room source where present. Do not rerun the one-time `upgrade-sensorium.py`, `expand-policy-rooms.py`, `polish-twinkle-batch.py`, `expand-public-topics.py` or `finish-topic-order.py` migrations for routine updates.

`content/twinkle-topic-icons.json` records the topic icon mapping. Feather 4.29.2 icons are locally served under `assets/topic-icons/`, with the upstream MIT licence. Games uses a five-ring CSS cue. Icon and number share one row, and every card retains its text and keyboard link. New adult mental-health research and prohibited-plant topics sit together away from child/youth entries; the first 23 original ticker labels retain their order.

Validation: `python tools/publication-qa/policy-qa.py` uses the repository's isolated CDP browser on port 9227 for desktop/mobile renders, local links, anchors and external-link targets. `python tools/publication-qa/topic-integrity.py` checks the topic inventory, sequence, icons, ticker and preserved media. Reports and selected screenshots live under `tools/publication-qa/`. This is local generation and QA, not a deployment.

The 3 October author's reviewed 47 headlines and gripes are recorded in `content/twinkle-reviewed-copy.json`, including the final donations, pay-gap and plant wording. All 49 Twinkle HTML sources now live in `content/rooms/`. `tools/apply-reviewed-twinkle-copy.py` is a completed one-time migration, not a routine generator. Earlier long-form seeds and hero descriptions are preserved verbatim in `content/twinkle-earlier-seeds.json`; `tools/twinkle_seed_context.py` publishes them as expandable context in their existing follow-through rooms. The policy and foundation publishers integrate this context. Run the context publisher explicitly after another generator that rewrites those rooms. `python tools/publication-qa/reviewed-copy-qa.py` verifies the exact approved copy, preserved original material and unchanged ticker against the pre-copy commit.

## Homepage issue ticker

`content/home-ticker.json` contains dated issue headlines, jurisdiction labels, primary sources and editorial limits. Run `python tools/build-home-ticker.py` after a reviewed refresh. The ticker pauses on hover and keyboard focus, offers pause/play and touch-friendly links, respects reduced motion, and excludes animation clones from keyboard navigation. Prior topics are archived under `content/archive/`. It is not an automated breaking-news feed.


## Sitemap election calendar and shared navigation

`content/elections/state-election-calendar.json` records source-checked general-election dates, time zones and statutory-date qualifications. `assets/state-election-calendar.js` carries the same snapshot for file and HTTP use: update both together after a commission announcement. Fixed dates count calendar days locally; Tasmania has no invented exact date. Passed dates move below upcoming dates pending review; they never silently roll forward four years. All shared footers use top-aligned natural-height link groups. Sitemap directory links use explicit `index.html` paths for local-file compatibility.

Connected projects are maintained in `content/connected-projects.json`; run `python tools/build-connected-projects.py` to refresh the seven reviewed cards and contextual links in existing pages. Other inherited cards remain in `pages/site-map.html`. The legacy `#official-links-out` anchor remains compatible and `#connected-projects` is an alias. The 2 October approved batch adds Australian Law: Luke’s Relevance, C-Hour introduction, Aura Direct Hardware and Mutual Futures.

Twinkle 48, Political lies, adds the approved “Lying, but authorised.” seed without changing the earlier 47 entries. It opens the Truth Engine and remains distinct from Twinkle 17 on donations. The inventory maps this shared destination; `add-political-lies-twinkle.py` is a completed one-time migration.

Twinkle 49, AI p(doom), opens `pages/ai-pdoom.html`: four outcome questions with dated primary sources and links to the existing GAJRA Earth Claude build. `tools/add-ai-pdoom-twinkle.py` is a completed one-time migration; publish subsequent edits with `build-policy-rooms.py`. Earlier 48 approved entries and historical planning audits remain intact.

Editorial preference: do not use "bloody" or "bloody hell" as colloquialisms in new copy; use "bloomin’" where requested. Preserve unrelated source quotations and previously approved seeds unless an edit is specifically authorised.

Public prose uses ordinary ASCII hyphens (-), never en or em dashes, including HTML entities. Prefer natural sentence punctuation. Preserve URLs, code operators, source quotations and historical archives. Run `python tools/publication-qa/punctuation-qa.py` after generators.

The complete policy directory and every-page site inventory are generated from `content/twinkle-policy-drafts.json` by `tools/build-rabbit-hole-policies.py`. `tools/build-p4a-connections.py` also refreshes that directory; it preserves the earlier civic journey at `pages/civic-pathway.html`. Bare policy-room routes display their connected proposals; a `?twinkle=slug` route focuses one proposal.
