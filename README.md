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

> 🤝🔷 **A Luke × Claude build.** Created by Luke Nathan Hayes (`auraofintelligence`) and Claude — Fable 5, July 2026. Not a Codex build. This is the cinematic rebuild fork of [p4a_xyz](https://github.com/auraofintelligence/p4a_xyz); the original Codex-era repo stays untouched upstream.

Static multi-page prototype for the Purple Party for Australia.

P4A is currently a proposed movement and drafting project, not a registered political party. The site is a public workbench for civic imagination, local-first democratic repair, transparent systems, constitutional literacy, public ledgers, state and region portals, legal-memory tooling and future cyber-republic rehearsal.

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

Current political and historical data should live in markdown under `content/` so future agents can refresh it with permission.

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
