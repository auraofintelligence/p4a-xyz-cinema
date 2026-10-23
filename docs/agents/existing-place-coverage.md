# Existing civic place coverage

Repository audit: 17 October 2026, Australia/Brisbane. This inventories the local `p4a-xyz-cinema` checkout. It does not claim to audit other repositories or the deployed website, or to recheck every political fact against live sources.

## National place routes implemented locally

The same-day national expansion adds `pages/places.html`, eight jurisdiction place gateways, separate council/state/federal directories and dedicated place pages. Its canonical inputs are `content/places/councils.json`, `state.json` and `federal.json`; exact route and layer coverage is in the generated `route-registry.json`. The [canonical agent file](../../content/places/AGENTS.md) documents the implemented generator and scoped update commands. Current verification and outstanding individual-source coverage are recorded under `content/places/qa/`; a structural pass is not a claim of complete per-place source or browser review.

The [resumed local report](../releases/2026-10-17-national-expansion-resumed.md) records the 2,080 place routes, 33 directories, actual scoped evidence and remaining deeper-journey gaps. The earlier stopped handoff is historical. This local implementation has no national commit, push or deployment.

The following sections preserve the pre-expansion audit and explain the deeper features that must survive. Their statements about then-unbuilt atlases are historical baseline findings, superseded for national map/page coverage by the registry above. New local Twinkles remain for grassroots authorship.

## Councils

Redland City is the fuller public journey: one interactive division map, ten division overview pages, local Twinkle seeds, connected systems, public-record routes, participation, outcomes and the three accounts. The Queensland atlas selects all 77 councils plus the separately labelled Weipa Town Authority; those other councils do not yet have equivalent local journeys.

Victoria already has an additional council atlas within `states/vic/map/index.html`: 79 municipalities, eight unincorporated areas and 467 ward/electoral-structure records. This is substantial existing map and data work. Do not label those as 79 completed Redlands-style local issues and systems journeys.

## State electorates

**Victoria is implemented as an electorate atlas and data foundation.** The user's latest work did not yet extend into an equivalent deep issues and systems journey for each electorate.

| Existing component | Evidence in this checkout | Scope |
| --- | --- | --- |
| Interactive state electorate atlas | `states/vic/map/index.html`; `assets/vic-electorate-map.js` | Searchable, selectable Canvas map with Assembly and Legislative Council layers, sortable metrics and profiles |
| Assembly records | `content/electorates/vic.md`; `assets/vic-electorates.js` | 88 districts |
| Legislative Council records | Same source and atlas | Eight multi-member upper-house regions; these are state electorates, not local councils |
| Source geometry | `assets/maps/vic-assembly.geojson`, `vic-council.geojson`; `vic-provenance.json` | Official source shapes, retained hashes and lossless delivery |
| Election result snapshots | `content/electorates/vic-election-results.json` | 96 result records, each with its own event period and original VEC source |
| Census snapshot | `content/electorates/vic-census-2021.json` | Seven measures across 88 districts: 616 values with workbook cells; 2021 observations on the stated 2022 boundary basis |
| Representation and election material | `content/representatives/vic.json`, `content/elections/vic-2026.json` | Public member/profile material and separately identified candidate announcements and election stages |
| Implementation notes | `content/electorates/vic-implementation.md` | Existing generator, projection, compression, source and QA contracts |

The electorate source carries a **2 October 2026** check date. The audit date above must not replace it. Related candidate, election and member records have their own dates. Representation counts and roles describe those dated snapshots.

All eight state/territory portals exist, but a portal, chamber summary or election countdown does not establish complete electorate-by-electorate coverage. No comparable complete state electorate atlas was found for the other jurisdictions in this checkout. Queensland's Oodgeroo, Capalaba, Redlands and Springwood maps currently provide boundary context within the Redlands journey; they are not independent electorate journeys.

## Federal electorates

**No dedicated federal electorate atlas or complete federal electorate journey was found in this checkout.**

Bowman has an attributed AEC map retained as `assets/maps/redlands/bowman-2018.pdf` and `.png`, with edition and source notes in `content/councils/redland.json`. It is used for Redlands boundary comparison and public-record routes. This is useful research material; it is not an interactive federal division atlas, a reviewed electorate-specific issues journey or a full current candidate/voting-history database.

National policy rooms, Commonwealth discussion and external parliamentary links remain separate from electorate coverage. House divisions and Senate state/territory representation require separate source and representation models when built.

## How to continue

Read the appropriate council, state or federal guide. Reuse the implemented map and source pipeline, then record the missing human journey, data and evidence in a place-specific report. Preserve existing features while adding depth. The comparisons and transfer priorities are in `victoria-redlands-lessons.md`.

Update this inventory when a reviewed place is actually implemented. Record atlas coverage, full journey coverage and partial contextual references separately; do not count buttons, data rows or a historical map as completed journeys.
