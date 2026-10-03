# Victoria electorate atlas — implementation and maintenance

The atlas is `states/vic/map/index.html`. It is a separate representation view; the architecture page keeps its council-first framing. The atlas uses local Canvas rendering and a complete text directory of 96 state, 554 local-government/electoral-area and 16 statutory-recognition records. No package install, external map SDK, tiles, account or API key is required.

## Sources and generation

- Authored records: `content/electorates/vic.md`; state overview: `content/states/vic.md`.
- Full original WFS GeoJSON: `assets/maps/vic-assembly.geojson` and `vic-council.geojson`; CC BY 4.0 sources and SHA-256 hashes in `vic-provenance.json`.
- Rendered assets: `assets/vic-electorates.js`, `vic-electorate-map.js`, `vic-map-geometry.js`, `vic-map.css`.
- Template: `tools/templates/vic-map.html`; builder: `tools/build-vic-map.py`.
- The projection is equirectangular with standard parallel 37 degrees south and a local origin. It is affine in source longitude/latitude, so every straight source segment stays aligned. All 1,683,468 source vertices are retained. Canvas uses identical even-odd paths for drawing and picking. Label anchors are derived inside the largest polygon component; they do not alter boundaries.
- Original geometry remains 26,581,934 bytes (Assembly) and 13,487,487 bytes (Council). HTTP loads exact microdegree delta/varint gzip payloads of 2,360,526 and 1,149,454 bytes. File URLs load local classic-script base64 wrappers (3,753,611 and 1,914,186 bytes), avoiding file-fetch CORS restrictions without a server or browser security changes. `tools/encode-vic-geometry.py` generates both delivery forms. Every original coordinate, ring and property round-trips exactly; originals and hashes remain unchanged.

Run from the repository root:

```powershell
powershell -NoProfile -File tools/build-state-sites.ps1 -StateSlug vic -SkipHistory
python tools/build-vic-map.py
python tools/verify-vic-map.py
```

The generator also supports PowerShell 7.5: ISO dates are explicitly kept as strings. Both versions read UTF-8 source content. The scoped build preserves other states’ existing national cards and emits the current six-door navigation and Index script. The map builder reuses the reconciled Victoria header. No global chrome migration is needed.

## Refresh rules

Archive superseded state facts before editing. Keep retrieval date, event/election date, source observation period and boundary edition separate. The October 2026 changes are logged in `content/archive/2026-10-02-victoria-refresh.md`; the old May source is preserved verbatim alongside it. Victoria’s older history research date is retained; this was a political/electoral refresh, not a new history audit.

Member data was joined from the official Parliament CSV: 87 Assembly members, Brunswick vacant, 40 Council members. Stable IDs use official district/region codes. Do not turn party announcements into nominations. Historical VEC result links include Narracan’s 2023 supplementary election and subsequent district by-elections. Numerical sources are `vic-election-results.json` (96 complete VEC result snapshots, distinct primary/DOP/2CP/2PP tables) and `vic-census-2021.json` (616 values, seven fields across 88 districts, exact workbook source cells). `tools/vic_profile_facts.py` builds the same numerical HTML used in the interactive and no-JavaScript profiles. Keep 2021 observations separate from 2022 boundaries and 2026 representation. Narracan uses January 2023 and Mulgrave November 2023; subsequent by-elections remain separately dated. Indicative 2CP totals are not forced to equal rechecked formal totals.

## Verification

`tools/verify-vic-map.py` needs only Python and Node. It checks source hashes, coverage, joins, member counts, source/generated parity for every state, local links, navigation, ISO dates, no-JavaScript records and calendar/DST behavior.

Additional QA scripts are in `tools/vic-qa/`. `geography.py <output-directory>` needs Shapely and creates independent picking fixtures plus a report. It found valid geometry throughout, four additional multipart components in each layer, no interior rings in these source datasets, and zero symmetric difference between each Council region and its 11-district union. Synthetic hole/multipart tests cover the geometry helper.

`browser.py <output-directory>` uses the generated fixtures and an isolated headless Chromium/Edge debugging endpoint on port 9227, with this repository served locally at `http://127.0.0.1:8765/`. It checks 156 Assembly and 41 Council points, including approximately one-metre offsets beside shared edges, all electorate interiors, small components and outside-water points. Checks repeat after metropolitan/rural zoom and at mobile DPR 2. Real mouse hover, keyboard Enter selection and focus retention, touch selection and pinch zoom pass; mobile has no horizontal overflow. Browser and geographic report snapshots are included in this folder. Use text report mode for this task; no screenshots or source files are uploaded.

No deployment, commit or push is part of this implementation.


## Sorting, representation and navigation

Alphabetical, population, electorate area, median age, median weekly rent and median weekly household income support both directions. Missing values are last in either direction and numeric ties use electorate name. Each selected metric shows units and period. Region population/area are explicitly sums of 11 district observations; no medians are averaged. Area is not described as land-only, and district sums need not equal the statewide workbook area. Volunteering and rented-tenure percentages are withheld because denominator validation is incomplete. Budgets/debt are not apportioned to electorates.

`assets/vic-representation.js` derives chamber seats and totals from the same current-member records used by profiles. Assembly shows 88 seats (87 members and one vacancy); Council shows 40. Geographic colours identify Council-region groups. Party mode uses current sitting parties for Assembly; Council retains geographic fills and shows five individually labelled member badges per region. Independent and vacant styles are distinct. Physical seat positions now come from the official Assembly and Council seating sources, with hover/focus/tap detail, arrow-key navigation and written totals. The 45/21 full-house markers are explicitly distinguished from procedural voting thresholds. Party order implies no coalition.

Selected records have permanent query links; browser Back/Forward restores chamber and selection, including `file://`. The atlas footer opts into four compact groups through `data-footer-compact`; other pages retain their existing footer behavior.

## Performance and verification limits

Cold headless Edge at 10 Mbps / 80 ms simulated latency improved observed Assembly load from 24.38 s to 5.89 s after lossless delivery encoding. This is a local controlled comparison, not a production-network guarantee. Picking p95 was around 0.1 ms. Full-state zoom repaint in GPU-disabled headless mobile emulation remains roughly half a second; geometry is intentionally not simplified. Real device GPU performance and production cache/compression headers remain unmeasured.

`tools/verify-vic-numbers.py --sources <download-directory>` checks every source cell and all VEC snapshot checksums. Browser text reports cover direct-file/HTTP, desktop/mobile, all profiles, Back/Forward, no-JavaScript and geometry failures, all sort orders, missing/tied metrics, party legends and chamber totals. `verify-codec.js <repo>` deep-compares all 1,683,468 coordinates plus properties and rings. No dependencies were installed and nothing was published.

## Council data model and remaining national coverage

The Legislative Council layer remains the state upper house. Separate `lga` and `ward` layers now implement actual local government: 79 municipalities plus eight distinct unincorporated polygons, and 467 source electoral-area features (444 wards, 22 unsubdivided areas and one unspecified unincorporated area). These are not 87 councils or 467 conventional wards. Budgets, debt, rates and service-performance figures remain unavailable.

Use distinct identifiers and versioned records: `jurisdiction` (AU/VIC), `level` (federal/state/local), `body` (Assembly/Council/municipality), `officialCode`, `boundaryEdition`, and validity dates. Represent municipalities, wards and electorates as separate entities. Store representation as dated person-to-seat appointments, distinguishing elected councillors and administrators; affiliation is sourced or unknown, never inferred.

Store statistical observations by entity, metric ID, value, unit, denominator, reference period, geography version, source URL/cell, retrieval date and revision. Preserve annual source series and boundary changes. Council budget vs actual expenditure, operating result, borrowings, liabilities, rates, services and population require precise definitions and comparable periods; unknown values remain null, not zero. Census measures retain their own observation year.

Add independently validated many-to-many geometry intersections between municipal/ward, Assembly/Council and federal electorates. Separate geometric area overlap from population correspondence; do not allocate people or finance using an unlabelled area share. Document tiny slivers, coastline differences and boundary vintages rather than forcing a one-to-one council/electorate relationship.

Completed: council register, exact municipal/ward boundaries, current councillor and administrator profiles, dated population series and state-electorate spatial intersections. Pending: accessible/licensed comparable finance/service series, verified federal geometry/crosswalks and other states. First Peoples-led cultural sources and separately labelled public legal-recognition layers are the next priority; they are not claimed complete by this council checkpoint. Australia-wide completeness is not claimed.


### Council checkpoint — 2 October 2026

`content/councils/vic.json` is the reviewed council snapshot; `tools/vic_council_facts.py` generates static and interactive profiles. The same atlas route supports `?chamber=lga` and `?chamber=ward&council=vic-lga-…`. Ward geometry is lazy-loaded and filtered to the selected municipality; the full ward layer remains accessible. Browser Back/Forward and permanent links preserve scope and selection. Local layers disable party colouring because affiliations were not verified.

All 79 official VEC profiles were checked: 640 current councillors and seven explicit vacancies across 78 elected councils; Moira has no sitting councillors and its two administrators are sourced separately from its official panel page. Melbourne's Lord Mayor/Deputy Lord Mayor are distinguished from its nine other councillors. Ward roster totals reconcile with the source seat capacities, including those exceptions. Historical election/review links are source links, not newly transcribed vote tables.

ABS supplies 1,975 annual ERP observations (25 years × 79 councils), current density/area and 2024–25 growth components. Every stored ABS field matches the downloaded source, and population/change component totals reconcile. These use ABS LGA 2025 statistical geography, not each year's historical legal boundary. Merri-bek is explicitly crosswalked from Vicmap's retained ABS code 25250 to ABS LGA 2025 code 24700. The eight unincorporated polygons share ABS aggregate code 29399; no population is allocated between them. Financial nulls mean unavailable, not zero. The LGPRF request returned HTTP 403; no bypass was attempted.

Council geometry: 686,964 vertices; ward geometry: 1,103,279 vertices. Original WFS GeoJSON hashes and every coordinate/property/ring are retained. Lossless HTTP assets are 1,555,758 bytes (municipalities) and 2,562,129 bytes (wards), about 90% below original JSON; direct-file classic-script delivery uses the same exact binary. All four atlas layers together round-trip 3,473,711 vertices. Five municipal source polygons have self-intersection defects; the downloaded/displayed coordinates are unchanged. GEOS `make_valid` is used only in the analysis copy for label anchors and intersections, with each defect logged. All ward source geometries are valid.

There are 422 positive-area Assembly intersections across municipal/unincorporated polygons. Touch-only edges are excluded; positive-area slivers remain visible as qualified links. Council-region links follow the already-verified exact union of their 11 Assembly districts. These many-to-many links are not centroid assignments, population shares or allocations of finance.

QA text reports in `tools/vic-qa/` cover every local profile, ten council sort orders, explicit missing-last behavior, nine-ward Yarra drilldown, Moira administration, permanent links/Back, no overflow and no runtime exceptions under file and HTTP loading. Independent geometry fixtures include all interiors, approximately one-metre edge offsets, holes and small components. HTML source remains usable without the interactive map. Original state electorates, party schematics and numerical profiles remain intact.


## Source-use review

Read the [human-readable licence register](../licences/vic-source-register.md) or [JSON register](../licences/vic-source-register.json) before introducing new source assets or changing the project purpose. The present purpose is personal/public non-commercial civic research; political-party, commercial, fundraising and wider redistribution changes trigger a source-specific recheck. LGV conditional non-commercial terms are now verified; numerical finance coverage is still blocked by source access.


## Completed interaction and recognition follow-through — 2 October 2026

The All Victoria control clears search and ward scope, restores the fixed statewide extent, and preserves the selected record. Ward drill-down, individual ward and cross-layer links align the map and its controls after fonts/layout and the shared header settle. Layout observation uses animation frames rather than an arbitrary navigation delay. Reset during loading, repeat activation, deep links, reload, Back and keyboard Home are covered by `tools/vic-qa/map-navigation-report.json` under file/HTTP and desktop/mobile conditions.

Country & First Peoples starts with community-led Gambay, VACL and FVTOC sources, linked without copying or tracing. Separate RAP appointment and Recognition and Settlement Agreement controls display 12 and four public statutory records. Original EPSG:4326 service responses are retained; VIC2 binary delivery retains original IEEE754 coordinates exactly. All six layers contain 4,020,843 vertices and pass exact geometry/property/ring round trips for HTTP and file delivery. All 16 new geometries are valid. Independent interior and overlap fixtures total 35; the picker returns every matching record, and overlap choices/permalinks retain them. Empty statutory coverage is explicitly not a statement that Country or Traditional Owners are absent. No sensitive heritage-site layers were accessed. NNTT claims/determinations remain source links; cultural maps and native-title geometry are not claimed imported.

`content/representatives/vic-seating.json` records 88 Assembly and 40 Council physical positions and source hashes. Assembly positions derive from the 11 August 2026 official PDF: occupancy is separately dated 2 October, with the former Tim Read/Brunswick position vacant. Later Assembly seat moves cannot be inferred from that older plan. Council positions and names derive from the live official graphical plan retrieved 2 October. Furniture is an independent orientation drawing, not copied source artwork. Non-member furniture is not counted as a parliamentary vacancy. The procedural voting notes and 45/21 full-house markers remain separate from seat arrangement and party ordering.

`content/representatives/vic.json` contains 127 MPs, 640 councillors and two Moira administrators. `assets/vic-profile-details.js` supplies labelled native dialogs, source/contact links, stable person URLs and Area / Representatives / Elections tabs. MPs' professional contact values retain the CSV update date; councillor biographies/direct contacts are not fabricated. Election history links on councillor profiles are explicitly council-level sources, not verified personal histories. Nine result-link annotations were removed from display names while original source labels and stable IDs remain. Generated browser data shares repeated council histories, reducing its size from 1,605,261 to 489,966 bytes without losing records.

Automatic focus chooses Election from 90 days before to 14 days after the scheduled state election, based on Melbourne's date; users can explicitly select Election or Governance. This is a disclosed workbench preference, not an official campaign-period claim. Announced, formally nominated, elected and former statuses are defined separately. No 2026 candidate records have been verified in this snapshot; current members are not silently promoted to candidates. Later readers must check the linked VEC source rather than treating the 2 October snapshot as current.

The final asset version is shared across atlas scripts/styles to avoid mixing cached readers with the compact data format. Browser reports cover all 769 dialogs, 128 seat positions, all statutory profiles and fixtures, source-layer toggles/empty state, map-preserving UI history, seasonal modes and no document overflow, on file/HTTP at desktop/mobile widths. Visual checks cover non-overlapping seat buttons, close/Back focus, direct person URLs and modal overflow. Tested gold text/active-tab contrast is at least 11.17:1. Screenshots were inspected locally and are not delivered or committed as report artifacts.

### Current complete-page performance

assembly: 13.71 seconds, 6,313,845 transferred bytes, picker p95 0.10 ms; firstpeoples: 15.41 seconds, 10,145,441 transferred bytes, picker p95 0.30 ms. These are cold-cache local HTTP observations at simulated 10 Mbps / 80 ms latency, mobile 390×844 DPR2, isolated headless Edge with hardware acceleration disabled. They include the larger full HTML directory and representative data, so they are not directly comparable to the earlier state-only 5.89-second checkpoint. Production compression/cache headers, real-device GPU behavior and typical mobile networks remain unmeasured. Exact geometry is intentionally retained; the full-state rendering cost remains a limitation.

### Re-running focused browser QA

Use an isolated headless Chromium/Edge debugging endpoint on port 9227 and serve the repository at `http://127.0.0.1:8766/`. Then run `python tools/vic-qa/map-navigation.py`, `python tools/vic-qa/expanded-browser.py` and `python tools/vic-qa/visual-performance.py` one at a time. These tests share the isolated browser, set viewport/network conditions, and reset that test tab's navigation history. They must not target a personal browser session. First Peoples fixture generation additionally requires Shapely; no package was installed for this work. Existing numerical and source integrity verifiers remain applicable. The licence register, not the project licence alone, governs source-specific maintenance decisions.


## Dedicated election guide — 2 October 2026

The election doorway is `states/vic/election/index.html`. Its source is `content/elections/vic-2026.json`; run `python tools/build-vic-election.py`, then `python tools/build-vic-map.py` after candidate updates. The latter derives atlas candidate payloads from the same source. `tools/build-state-sites.ps1 -StateSlug vic -SkipHistory` preserves the prominent Victoria navigation link. Source research and historical/manual-review claims are separate JSON records; candidate status is not inferred from office-holding. The 482-record snapshot supersedes earlier empty-candidate notes, not the dated historical evidence.
