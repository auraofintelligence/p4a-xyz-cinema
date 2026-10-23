# National place data: scoped maintenance

Version 1.5, 18 October 2026, Australia/Brisbane. Inherit [root instructions](../../AGENTS.md) and the [fractal election update guide](../../docs/agents/fractal-election-updates.md). This file supplies the implemented national adapter; it does not replace the level-specific civic rules or certify complete source coverage.

Repeat the same process for one event, ward, council, electorate or jurisdiction: identify stable records, verify the official change, edit canonical data, rebuild actual dependants, check, record. Create no new Twinkles. Preserve unrelated work and source dates.

## Canonical inputs and identities

- `councils.json`: real councils, local electoral areas and explicitly exceptional/unincorporated contexts.
- `state.json`: actual state/territory chambers and electoral areas.
- `federal.json`: serving House divisions, separate future boundary editions and Senate state/territory areas.
- `sources/` and `raw/`: dated source manifests and retained original source material. Respect their licences. Use legally accessible public sources; do not bypass access restrictions or collect private contact details.

`raw/` is a local-only research cache: it is ignored by Git and excluded from public-source packages by `source-retention.json`. Do not publish full source pages/PDFs or directory contacts merely because they were publicly readable. Required attributed map assets live separately under `assets/maps/`; public source manifests retain original URLs, dates and hashes. Missing local-only originals in a public checkout do not establish a fresh source verification.

Each place keeps a stable `id`, `jurisdiction`, `kind`, source IDs, `representatives` and event-specific `elections`. Genuine wards have `parentId`. The primary `layerId`/`featureId` joins the source layer; `mapRefs` preserves additional boundary editions. Never merge people or successor areas by name alone.

Current officeholders come from dated official rosters. An old election winner is not evidence of current office. Retain exact public profile URLs; use `profileType` containing `roster` when a link is an institutional roster rather than an individual profile. Historic contestants remain attached to their event, then-affiliation and vote measure. Append a by-election as a distinct event; preserve the previous general election.

Events retain `date`, `dateBasis`, `timezone`, `status`, official URLs and candidates. Unknown/estimated dates do not receive exact clocks. A published postal deadline uses `milestoneLabel: "postal voting closes"` and the sourced offset-bearing `dateTime`; polling day and postal closing time are different milestones. Passing a date never elects somebody automatically.

## Build only the affected unit and its dependants

From the repository root:

```text
python -B tools/build-national-places.py --place <actual-stable-id>
python -B tools/verify-national-places.py --source-hashes
node tools/check-civic-clocks.mjs
node tools/check-civic-geometry.mjs
node tools/check-civic-delivery.mjs
```

The build updates the target, its genuine parent/children and same-layer pages whose search/directories embed the changed record. It also rebuilds shared directory and route/geometry indexes. `--jurisdiction <slug> --scope councils|state|federal` selects a broader unit. Omit filters for the full build. Inspect all changed files; shared outputs are genuine dependants. The original Victoria atlas and Redlands journey have their own canonical sources and validators, documented in the parent guide.

Generated outputs include `route-registry.json`, `geometry-delivery.json`, `states/<jurisdiction>/places/`, council/electorate/federal detail pages, `pages/places.html` and `assets/qld-place-routes.js`. Edit their generator or canonical input, then rebuild. Do not hand-edit generated copies. Route families are described in the generated registry.

## Boundary change branch

Follow the parent guide's full redistribution procedure. Preserve raw geometry, rights, hashes, every coordinate/ring/part, source CRS, source pagination and serving/historical editions. Record proposal/final/effective/first-election stages separately. Never replace the currently serving map solely because a newer download exists.

Register new edition layers and source IDs; update actual feature joins, `mapRefs`, aliases, predecessor/successor relationships and new place routes with evidence. Retain old inbound routes and election histories. Check raster registration, lossless delivery, map/search/Open, island and hole picking, direct links and responsive layout. A roster-only update should leave geometry byte-for-byte unchanged.

## Navigation, evidence and handover

For added/renamed routes, update the appropriate `assets/site-nav.js` directory entries inside States and territories and the page/rule review register. Preserve the five primary Index themes in 01–05 order: Start here, The spark, The system, The ground game, States and territories, with their always-visible shortcut buttons. Start here opens by default with the nine chosen ideas: Genesis, Truth Engine, Musicverse, C-Hour/Braided Economy, Worker mutuals, Web3 Sensorium, Sovereignty Stack, Purple Synthesis and Cyber-Republic, followed by the seven bearings links including the civic pathway. Keep that human and conceptual front door and its plain purpose notes. Give each shared Index destination one category home. Do not duplicate Start ideas across categories or recreate a separate Key policy ideas category. The user chose deletion of Culture, including its shortcut/footer category, on 18 October; keep no placeholder or multicultural-coverage claim. Five specialist pages remain on their existing Genesis clinical/political/fiction paths, with no relocation, new topic or Musicverse content change. The readable sitemap uses Origins, music and imagination while retaining its group id/routes/membership. Legal RAG stays in System; preserve distinct query-specific destinations such as the Victoria First Peoples lens. It is a deliberate editorial choice informed by the original homepage/pathway, not a literal restoration of a sparse historical Start list. Council, electorate and Redlands links lead into deeper state/map journeys; they must not become new leading Index categories. `tools/build-redland.py` no longer prepends a local-navigation group. Place generators should leave shared navigation bytes unchanged unless a shared edit is explicitly intended. `tools/build-rabbit-hole-policies.py` removes its legacy Key navigation marker without reinserting a category; its KEY data still generates policy cards and homepage links. Run `python tools/build-human-site-map.py` followed by `python tools/verify-discovery.py`; this maintains human navigation, route inventory, XML sitemap and assistant directory together. Preserve known implementation dates and source dates separately.

The States section's footer is labelled Australia and has exactly one portal for each of the eight states/territories. Use its explicit `footerLinks = STATES.map(...)` list, not the first six States Index entries. Do not add repeated state chips or Minjerribah, Olympics or specialist Victoria links to that footer column. Keep the full States Index and its existing specialist links unchanged; this is a balanced Australia footer, not Queensland priority or a new topic-page project.

Other theme lists may start collapsed in the responsive grid. Search opens matching groups and clearing it restores the earlier expanded state, including the default-open Start group. Reopening the Index returns to Start here at the top, including after a States jump. Check the nine ideas and theme shortcuts, native summary keyboard focus, matching/no-results/clear behavior and narrow layout in an actual browser; a structural PASS cannot certify these interactions. Keep the existing style tokens. Record fresh results only after the affected review finishes. Prior five-fixture deduplication acceptance is retained under `qa/pre-culture-removal-2026-10-18/`; earlier Start and navigation reviews retain their own archives. They do not certify the later five-theme change. Do not equate one destination home with one total search result: distinct pages may legitimately mention the same idea. Review the current five themes, 132 unique destinations, removed category/shortcut/footer entry, unchanged nine Start ideas and retained deeper paths against the actual new evidence.

Record actual affected browser checks in `content/places/qa/browser-review.json`, with tested HTML paths, retained fixtures and their exact hashes. After default national structural validation and that review pass, `python -B tools/build-national-contracts.py` binds full canonical records and real evidence hashes. Run `python tools/verify-place-contracts.py`. Both reject changed data, pages, delivery or evidence. CI uses `python tools/verify-national-places.py --no-write` to repeat structural checks without replacing the saved reviewed report. Preserve the scoped `.gitattributes` byte rules on public evidence; raw originals and geometry are never line-normalized. Never copy a previous PASS into a new review or describe structural contracts as complete per-place source/browser certification.

Append the scoped event/source/route/check/coverage/publication handover to the shared refresh log and relevant history. A failed source request is an unresolved gap. Report local, committed, pushed and deployed state accurately; this guide authorises no automatic publication or monitoring.


## Match the existing style before extending it

Use the repository's documented self-hosted Archivo and JetBrains font tokens, purple panel treatment, width and radius tokens. Directory/person card headings must use the compact existing state-card scale, not the global cinematic H2 scale. Keep normal word wrapping in names. Do not introduce a separate visual system for national pages.

The 17 October typography correction followed a user screenshot showing oversized uppercase state names broken across lines. The earlier smoke review missed this visible failure. Inspect the actual card grid after fonts finish loading, not just its H1 or page-overflow measure. Use `content/places/qa/typography-fixture.html` at desktop, tablet and narrow widths, then save a real screenshot showing the cards. Original reference: `.state-portal-card h3` and the design rules in `LOCALISE_WITH_AN_AGENT.md`. A narrow page can pass an overflow check while still having unreadable headings.
