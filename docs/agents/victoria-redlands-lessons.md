# Victoria and Redlands: lessons to carry in both directions

Code and content audit: 17 October 2026, Australia/Brisbane. This compares the existing local files; it does not recheck political facts, candidate announcements or source websites. Each dataset retains its own research date. The transfer work below is a prioritised backlog, not a claim that those features have already been added.

Read this with [local-place-pattern.md](local-place-pattern.md) and the council, state and federal replication guides. Preserve the existing Victoria atlas while extending the common journey. A uniform human experience does not require replacing every working renderer in one operation.

## What already exists in Victoria

Victoria is an implemented atlas, not merely a collection of state-level buttons. Its current local delivery, `assets/vic-electorates.js`, contains:

| Record group | Snapshot coverage | Important qualification |
| --- | --- | --- |
| Legislative Assembly | 88 districts | Current membership is a separate dated snapshot; a vacancy is an explicit state. |
| Legislative Council | 8 regions | These are parliamentary upper-house regions, not municipal councils. Each connects to 11 Assembly districts. |
| Local areas | 87 records | 79 municipalities plus 8 unincorporated areas; the latter must not become fictional councils. The snapshot distinguishes elected council and administration. |
| Local electoral areas | 467 records | 444 `WARD`, 22 `UNSUBDIVIDED`, 1 `unspecified` source classifications. Do not describe all 467 as wards or invent a ward for an unsubdivided municipality. |
| First Peoples statutory records | 16 records | 12 RAP and 4 RSA records. These legal datasets do not define all Country, cultural authority or consent. |

These counts describe the checked files, not an instruction to freeze Australia-wide counts. An official arrangement or dataset change needs a reviewed update.

`states/vic/map/index.html` includes 96 static electorate records and 554 static local-area/electoral-area records. The interactive view enhances that material. `assets/vic-profile-details.js` separates Area, Representatives, and Elections & candidates, with permanent links and keyboard-operable tabs. The people snapshot contains 769 people records and 482 candidate records; those counts are coverage of a dated collection, not a complete or current ballot declaration.

## What Victoria teaches the national pattern

### 1. Let people compare places through sourced measures

`assets/vic-electorate-map.js` already sorts the place directory by name and applicable measures. District measures include population, published area, median age, weekly rent and household income. Local-area sorting uses ERP population, growth, density and area. Unsupported measures are disabled for the selected layer; missing values sort last in both directions.

Every sort displays a period and unit. Region population and area are described as sums of district values; medians and rates are not averaged. Published electorate area is not relabelled verified land area. This is a stronger comparison pattern than a directory with names alone.

Transfer the behaviour, with a small useful set of genuinely comparable local indicators. A Redland division without a verified statistical correspondence gets “not available”, not its council's population divided by ten.

### 2. Carry evidence down to the cell or result table

`content/electorates/vic-census-2021.json` records seven fields for 88 districts with the source workbook, field sheet/column and individual cell references. Its 2021 observation year and 2022 boundary edition are separate. `content/electorates/vic-election-results.json` retains dated result records, source hashes, totals, and typed tables for the 88 districts and 8 regions.

Use this level of traceability for new council statistics where the source permits it. A visible value should lead to its exact source period, geography and denominator. A workbook cell needs its sheet name as well as the cell address. Historical election tables remain distinct from current office-holding, announcements and nominations.

### 3. Deliver large exact geometry efficiently

`assets/maps/vic-delivery.json`, `assets/vic-geometry-codec.js` and the existing encoder preserve exact coordinates while reducing transport size. Integer microdegree encoding is accepted only when the original numbers round-trip exactly. Other data uses original float64 values. Neither method permits rounding, simplification or dropping rings.

The Assembly source is 26,581,934 bytes; its retained gzip delivery is 2,360,526 bytes. The manifest records source and encoded hashes, vertex counts and delivery sizes. HTTP loading tries compressed data, handles an already-decompressed response, and falls back to original GeoJSON. A separate script delivery supports the existing file-preview path.

Queensland's current complete coordinate bundle is about 12.8 MB. A future performance improvement can reuse or generalise this lossless approach after measurement. Keep original source bytes, rights and hashes; prove every decoded geometry equals the original. Compression is a delivery change, not permission to alter boundaries. Do not load every Australian council's full geometry at first arrival.

### 4. Separate the person from the role, election and history

`assets/vic-profile-details.js` distinguishes current MPs, councillors, administrators and candidates. Candidate records distinguish announced, preselected and nominated status. The interface carries checked dates, source discrepancies, coverage limits and a warning that current office-holding does not establish candidacy.

Council-level history links are explicitly not asserted to be a person's electoral history. Missing personal biography or affiliation remains unverified. Carry those distinctions into Redlands profiles and every subsequent council. A public profile link is not evidence of a motive, vote or nomination.

### 5. Keep relationships navigable and shareable

Victoria connects an Assembly district to its Council region, a region to its districts, and a municipality to its electoral areas. URL state preserves the chosen layer, area, person and detail section. The directory searches names, relevant parent names, members and parties. Browser Back and a shared link can restore the relevant view.

Repeat this semantic relationship model in the national pattern. Use the actual institution labels: “Legislative Council region”, “local council” and “federal division” are different objects. A council/ward link is a parent relationship; a council/state/federal intersection is an overlap requiring its own evidence.

## What Redlands contributes back to Victoria

The Redlands build makes an ordinary concern the start of a civic journey: place or division → a recognisable question → evidence and perspectives → connected systems → who can act → what changed. Its additions should complement Victoria's richer comparison and representation work.

| Redlands addition | Existing implementation/reference | Transfer lesson for Victoria |
| --- | --- | --- |
| Same map, search, select, inspect and open pattern | `tools/qld_council_widget.py`, `assets/qld-council-map.js`, Redland division routes | Preserve the atlas selection interaction; connect selected municipalities and electoral areas to built local journeys without implying that every area is already complete. |
| Exact geographic context with quiet default roads | `content/councils/qld-basemap-sources.json`, retained raster and transparent boundaries | Use an appropriately licensed Victoria-covering geographic source and its real extent/projection. Queensland's base is not a national base. Marine administrative extent must never masquerade as land. |
| Small human Twinkle before its explanatory room | `content/local/redland-connections.json`, `qa/redland-20261017/twinkle-rule-review.md` | Use one gripe and one spoken breath. Put evidence, policy detail, dependencies and broader systems underneath. Do not shrink a policy essay and call it a Twinkle. |
| Local examples connected to macro proposals | Redland Explore and Possibilities pages | Connect a person's chosen concern to legal RAG, digital twins, civic AI, care, learning and existing project sources when relevance is evidenced. Related does not mean delivered or solved. |
| Braided economy trinity | Redland Action and Outcomes pages | Keep what it cost, what was given freely and what changed visible together. One verified voluntary hour counts once; do not invent a dollar conversion or replace paid responsibilities with assumed volunteers. |
| Human-controlled participation and private drafts | `assets/local-council.js`, static form guard and local exports | Carry the person's chosen purpose and evidence trail; explain export and publication separately. A static page must not imply a live civic database or record issuance. |
| Explicit conditional election branch | `content/local/redland-election.json` | Keep possible vacancies/by-elections, announced events and ordinary cycles separate. Early voting has its own verified dates and event identity. Never copy Queensland's laws or timetable to Victoria. |
| Meanings and agent continuity | local pattern guide and connected meaning record | Carry Joyful Responsible Abundance and the lyric meanings through choices and consequences. No forced philosophical preamble, invented endorsement or inferred personal candidacy. |

Redlands does not yet provide Victoria-equivalent historical result tables, comparable division statistics, or a complete individual voting-record and reason collection. Victoria does not yet demonstrate the complete Redlands local Twinkle-to-system-to-outcome journey for every municipality. Neither side should be advertised as satisfying every later national contract merely because some layers already work.

## Prioritised transfer backlog and acceptance

These are scoped next changes. Do not mass-generate 500 council portals or rewrite the two engines to satisfy this report.

| Priority and change | First files to inspect or change | Acceptance before calling it complete |
| --- | --- | --- |
| P0: preserve the existing atlas and source parity | `tools/verify-vic-map.py`, `content/states/vic.md`, `assets/state-data.js` | All authored state records match generated records; historical dates stay unchanged; all affected local asset links resolve. No full-state regeneration solely to fix a punctuation or path mismatch. |
| P0: make old implementation status explicit | existing atlas routes and the national place registry/validation report | A report distinguishes implemented legacy features, audited requirements, known gaps and unbuilt local journeys. Do not turn “not yet registered in a new manifest” into “no atlas exists”. |
| P1: connect a single Victoria municipality to a local journey | `assets/vic-electorate-map.js`, `assets/vic-profile-details.js`, reviewed local-place records | Map and search select the same actual area; its Open link enters a reviewed journey; breadcrumbs, place identity and chosen question survive; unrelated councils retain honest unbuilt status. |
| P1: add applicable measure sorting to the new council directory | `tools/qld_council_widget.py`, `assets/qld-council-map.js`, reviewed fact records | Measures show period/unit/geography; no invented division values; missing stays unavailable and sorts last; name/search/selection remain usable on a phone and tablet. |
| P1: transfer the representative/candidate evidence model | Victoria people/profile records and Redland candidates source/generator | Current role, election, candidate status and history are separate; sources and checked dates appear; missing vote reasons stay unknown; stated reason and analytical inference have different labels. |
| P1: add public issues and outcome connections to one Victoria example | existing Victoria profile links plus reviewed local Twinkle, system and outcome records | A small set of locally evidenced questions opens a real explanatory path, shows jurisdictional responsibility and the trinity, and links back to the selected place. Existing tools continue to produce drafts rather than fictional submissions. |
| P2: reduce Queensland geometry delivery without loss | current widget delivery and Victoria codec/manifest/encoder | Coordinate-by-coordinate equality, properties/IDs and ring count match; hashes and sizes recorded; search, holes, mainland/island picking, offline fallback and failed-network behaviour checked. |
| P2: establish statistical and electoral histories for one new place | local fact/election records and Victoria source models | Periods, official event IDs, boundary basis, result stage and table type are explicit. Redistribution breaks comparability where appropriate. No result is repurposed as a measure of council-wide public opinion. |
| P2: quieter geographic background in Victoria, if needed | `assets/vic-electorate-map.js`, appropriate new source register | Source terms and geographic coverage permit use; actual image extent/CRS is retained; island/coastline alignment and selected overlays checked; roads remain optional or visually subordinate. No SVG approximation. |

## Maintenance lesson from this preparation

On 17 October, the Victoria parity check detected two punctuation differences between authored state JSON and its browser delivery. Restoring the two exact authored strings repaired parity without changing political facts. The next check exposed an early-voting script copied into the sitemap at the wrong relative depth. The canonical room and rendered page both require the correct published-path reference.

Carry this into every place: canonical content and generated output are a pair; a passing data test does not prove navigation works. Validate actual output paths, preserve source dates during builds, and run the existing jurisdiction's checks alongside the common contract. A new framework must inherit working features and their regression checks, not silently discard them.

## Minimum evidence for a transfer report

Record the inspected source files, data observation/review dates, the exact route tested, missing coverage, and the verification actually run. This document is a code/content audit, not a fresh browser or source-verification pass. A future agent must not relabel its comparisons as current election facts or claim this backlog has been implemented. Publication and expansion remain subject to the operator's current authorised scope.
