# p4a-xyz-cinema

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
