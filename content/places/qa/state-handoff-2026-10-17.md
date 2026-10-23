# State and territory source adapter handoff — stopped 17 October 2026

## Resumed implementation, same day — supersedes the stop-only instructions below

The user explicitly resumed this work. Source integration is now saved in `state.json`: **442 places, 619 current representative records, 4,087 event-specific contestant rows, 11 layers and 344 sources**. The detailed [state integration coverage report](state-coverage-2026-10-17.md) records the changed sources, preserved editions, actual checks and remaining partial history. The original stop-state audit below remains as history; its data counts and missing WA/NSW Council/Karama/Ngadjuri/TAS geometry statements are superseded by that report.

`tools/acquire-state-places.py` remains offline by default. New source retrieval can be narrowly consolidated with repeated `--only <registered-id>` plus `--network --acquire-only`; this avoids replaying unrelated failures or rewriting canonical data during acquisition. The complete TAS projection is cached only when the retained ZIP and both compressed deliveries match the actual verification hashes. Its optional local dependencies are documented in the coverage report.

No new Twinkles, commits, pushes or publication were performed. Shared national page/browser/contract/discovery acceptance belongs to the parent build and is not established by the state-specific PASS.

The user requested a handoff and a stop because of approval fatigue. **Do not resume acquisition, implementation, or publication without new user direction.** This is a truthful partial implementation handoff, not acceptance evidence or a completed national state build. No new Twinkles were created.

## Saved inputs and adapter

- Canonical normalized input: `content/places/state.json` — schema version 1, scope `state`, checked `2026-10-17` (underlying facts retain their separate dates).
- Owned acquisition/offline normalization adapter: `tools/acquire-state-places.py`.
- Request URL/status/hash registry: `content/places/sources/state-requests.json`.
- Source rights/exclusion register: `content/places/sources/state-source-rights.json`.
- Retained research responses: `content/places/raw/state/`.
- Generated lower-house geography: `assets/maps/national/state-*-assembly-2025.geojson.gz`.
- Existing Victoria sources are reused at `assets/maps/vic-assembly.geojson`, `assets/maps/vic-council.geojson`, `content/electorates/vic.md`, `content/electorates/vic-election-results.json`, and `content/representatives/vic.json`. Their original 2 October 2026 review dates were retained.
- Independent Queensland supplement, owned by the federal helper: `content/places/state-qld-details.json`; reproducible with `tools/acquire-qld-state-details.py --build`.
- Independent NSW supplement, owned by the federal helper: `content/places/state-nsw-details.json`; its source and verification records use the `state-nsw-supp-` prefix.

An ordinary `python -B tools/acquire-state-places.py` run reads cached responses and rebuilds the entire canonical state file and derived state map deliveries. It also rewrites the request registry and rights register. **Do not run it merely to inspect one fact or claim it is a safe single-place update.** Its presently implemented supplement merge covers Queensland and NSW. `--network` performs registered public source requests; `--probe ID=URL` registers another source. No further network run is authorized by this handoff.

## Exact saved canonical counts

The inspected final `state.json` contains **441 places, 9 layers, and 288 source records**.

| Jurisdiction | Places | Current member records | Historical contestant rows |
| --- | ---: | ---: | ---: |
| Victoria | 96 | 127 | 1,197 |
| NSW | 94 | 93 | 603 |
| Queensland | 93 | 93 | 541 |
| South Australia | 48 | 68 | 0 |
| Western Australia | 60 | 0 | 544 |
| Tasmania | 20 | 50 | 164 — contains three erroneous group-header rows, see below |
| Northern Territory | 25 | 24 | 80 |
| ACT | 5 | 25 | 149 |

The 441 place identities comprise 415 lower-house electoral areas, eight Victorian Council regions, 15 Tasmanian Council divisions, and three whole-state Legislative Council contexts (NSW, SA, WA). Multi-member lower-house areas are not counted as individual members. Whole-state upper-house contexts have no invented regional map.

Current member sources are independent parliamentary rosters/profiles, not election-winner inference. The 127 Victorian member records preserve the pre-existing dated snapshot and its Brunswick vacancy. NSW current Assembly members and its 2023 plus six later by-election ballots come from the helper supplement; NSW Legislative Council members and its previous 2023 contestants remain missing. Queensland includes 93 independently verified current MPs, all 525 general-election contestants from 2024, seven Hinchinbrook 2025 contestants, and nine Stafford 2026 contestants. These historical events remain separate.

## Boundary coverage and edition limitations

Seven non-Victorian lower-house layers were acquired from the official Digital Atlas of Australia / Geoscape service:

`https://services-ap1.arcgis.com/ypkPEy1AmwPKGNNv/ArcGIS/rest/services/State_Electoral_Polygon/FeatureServer/19`

All source polygon rows reconcile to independent official `returnCountOnly` responses: NSW 242; Queensland 95; SA 247; WA 2,749; Tasmania 271; NT 38; ACT 5. WA required three pages. Empty additional pages were checked for every jurisdiction. Polygon fragments are grouped by persistent `se_pid`, retaining each original ring/coordinate and source polygon ID. The service's class domain was verified: 1 House of Assembly, 2 Legislative Assembly, 3 Legislative Council. Its May 2025 national source supplies lower-house geometry only for the seven newly acquired jurisdictions. It explicitly describes an aggregated geographic representation, not the legal boundary instrument.

**South Australia is not current-boundary complete.** The national May 2025 source includes historical Frome; the serving 2026 Parliament uses Ngadjuri. This accounts for the unmatched 47th lower-house member. Do not rename the old Frome polygon and call it the current district. A current official ECSA map response is already saved, but has not been normalized:

- `raw/state/state-sa-map-geometry.html` — 1,772,871 bytes, fetched from the map's own published `get_sa_council_region` public endpoint. Its response includes separate `2026` and historical `2022` sections.
- `raw/state/state-sa-map-page.html`, `state-sa-map-app.html`, `state-sa-map-district.html`, and `state-sa-map-model.html` document the official viewer and decoder.
- The correct future continuation is to preserve the current 2026 polygon data and its exact original encoding/rights, create a distinct current layer, reconcile its 47 district IDs/names, and keep historical representation/election geography distinct. Existing generated Frome routes will need explicit historical handling.

**Tasmanian Legislative Council map delivery is incomplete.** All 15 division records and all 15 current MLCs are present, but none of those 15 places currently has `layerId`, because the adapter requires the complete layer before connecting it. Official LIST ArcGIS EPSG:4326 responses succeeded for 13 divisions; Murchison (`LEG_CNL_ID` 100032) and McIntyre (100031) returned server error 500. Alternate native queries returned error JSON; do not treat their short HTTP-200 error bodies as geometry.

The complete official, licensed original 15-division ZIP was subsequently acquired and is retained at `raw/state/state-tas-lc-official-zip.html` (71,431,225 bytes; extension reflects generic probe storage, actual bytes are a ZIP). It contains `list_legislative_council_divs_statewide.shp/.shx/.dbf/.prj`, MapInfo and geodatabase files. Its projection is **GDA94 / MGA Zone 55 (EPSG:28355)**, not geographic degrees. Conversion and exact point/ring validation were **not implemented** before the stop. Do not pass the coordinates directly to the web map or approximate those two divisions. Prefer deriving one coherent layer from the full official ZIP with an appropriate reviewed CRS transformation, retaining all native bytes and recording the transformation.

LIST feature attributes confirm `2017 Redistribution`; the ArcGIS layer's narrative still incorrectly describes 2008. The current official metadata record confirms 2017, revision 20 March 2025. LIST CC BY 3.0 Australia terms and attribution documents were acquired as `state-tas-list-terms.html` and `state-tas-list-attribution.html` (actual bytes are PDFs). The catalogue's public download code, retained as `state-tas-list-download-code.html`, supplies the actual ZIP URL.

Queensland's represented 2017 boundaries must stay distinct from the new 2026 redistribution that first applies at the 2028 ordinary election; the supplement documents that distinction. Do not use the new boundaries for a pre-2028 by-election. Other redistribution/effective-date checks have not been fully reviewed jurisdiction by jurisdiction.

## People and contestant gaps / known corrections

- **TAS:** All 35 current House members and 15 MLCs are present with actual official individual profile links; public personal sites are retained where the profile links them. Singular `Green` and Casey Hiscutt's blank affiliation are handled; his party was not invented. The official 2025 first-preference workbook plus ballot-roster pages are retained. The adapter incorrectly includes the `Shooters, Fishers, Farmers TAS` group heading as a candidate in three worksheets. Remove those three rows and constrain the parser to actual ballot candidate names. The official total is **161**, not 164. It needs a full ballot/name/party/vote reconciliation. Upper-house previous periodic-election candidates and most division-specific past/next events are not normalized. The official LC calendar and history page are already retained: six-year cycles differ by division; do not apply the House election countdown to them. A rule supports May/year context without inventing an unannounced exact polling date.
- **SA:** 46 lower-house members plus all 22 current MLCs are normalized from the official current 56th-Parliament contact API configured in its public contact app. The 47th current HA member belongs to Ngadjuri and requires the current boundary/place adapter. Actual official `pmId` profile links are preserved. The API records more recent affiliation changes; do not substitute old election labels. The **2026 HA and LC results are downloaded but not normalized**: `state-sa-2026-ha-results.html` (157,058 bytes), `state-sa-2026-ha-change.html` (2,340,754), `state-sa-2026-lc-results.html` (1,586), `state-sa-2026-lc-change.html` (1,617,300), and `state-sa-results-dates.html` (917). These public production endpoints were discovered from `state-sa-results-code.html`, not guessed access credentials. Their exact URLs/hashes are in the registry. LC result-stage votes must not be mislabeled first preferences.
- **WA:** All 398 Assembly and 146 whole-state Council 2025 contestant names/ballot affiliations are normalized from the official WAEC public production API. The retained API and report can support further result transcription, but votes are not normalized. **No serving WA members are yet present.** Parliament list URLs returned 403. Do not use the elected-members result endpoint to infer current office. Publicly indexed parliamentary current-profile facts or an explicitly published current contact export can be legitimate sources; do not bypass a 403, CAPTCHA, paywall, or other access control. From 2025 the Council is one whole-state electorate electing 37 members; the former six regions must not be displayed as current.
- **NT:** All 80 previous 2024 contestants and their primary votes are normalized from the browser-accessible official NTEC source extraction. The current official member roster is dated **18 September 2026**, although its PDF filename says May. Actual individual profile URLs were resolved from the official current directory. **Karama is the sole unmatched current member** (24 of 25 normalized); its public source material is already retained. The current roster contains Ed Smelt and Yiwarr McGrath, so the new office is not inferred from 2024 results. Separate Nightcliff (7 March 2026) and Mulka (12 September 2026) by-election ballots/results are not normalized. They must remain separate from 2024. The NTEC official public event URLs were discovered but not downloaded after the stop.
- **ACT:** 25 current members independently sourced from the current parliamentary roster; all 149 previous 2024 contestants with party labels and first preferences are present. Leanne Castley's current Independent affiliation is distinct from her 2024 ballot party. The June 2026 Kurrajong countback replacing Shane Rattenbury with Rebecca Vassarotti has a separate historical event, but its consenting contestant roster/transfer results are still missing.
- **NSW:** 93 Assembly current profiles and 603 historical contestant rows (2023 general plus six by-elections) are merged. The whole-state Council context is present, but its current member/vacancy roster and previous 2023 contestants remain missing. The helper found 41 results in the current filtered parliamentary Council roster; do not silently fill a presumed 42nd member. The helper owns its detailed verification record.
- **VIC:** Original member/results/geometry snapshots remain dated 2 October 2026. Imported votes carry an explicit measure. No claim was made to refresh every Victorian current office or future candidate announcement. Existing 2026 candidate announcements remain in their original independent source/build; they are not copied into empty future-event nomination arrays.

## Clocks

Each normalized place has sourced ordinary-election context where applicable. The inherited national calendar was checked 2 October 2026 and its date has not been silently advanced. NSW supplement independently verifies **13 March 2027**, and Queensland independently sources the rule-derived ordinary **28 October 2028** date. TAS House timing remains null/unannounced; no invented exact countdown. The whole-state Council events distinguish NSW/SA half-chamber periodic elections from WA's whole chamber. Tasmanian Council events still need division-specific calendar/history ingestion. Past polling dates, countbacks and by-elections are separate events, and historical votes never establish current office or future nominations.

## Rights, QA, and stop state

Public accessibility does not establish a right to republish complete Parliament/electoral HTML, scripts, PDFs, browser extractions or contact datasets. Treat the full non-licensed research snapshots as **local-only**, as listed in `state-source-rights.json`; normalized factual names, roles, affiliations and results plus source links are the public output. No portraits were downloaded. The parent was warned that the existing upload helper otherwise includes all `content/`; its source exclusion handling must respect this register and any new raw files. Geoscape CC BY 4.0 and LIST CC BY 3.0 source-specific attribution/rights remain separate from the repository licence. Retain original licensed geometry bytes and hashes.

Executed: repeated offline parser/build runs; primary source acquisition with retained bytes, request URLs, hashes, statuses; jurisdiction polygon count reconciliation; exact canonical place/member/contestant count inspection; TAS 35+15 member reconciliation; identification of the three erroneous candidate group rows and the SA edition mismatch. The parent owns common renderer/navigation/browser QA. **This agent did not run final national validators, browser acceptance, full geometry coordinate-equality validation, full ballot reconciliation, or external-link verification.** These are not passing claims.

Acquisition initially failed sandbox DNS; a scoped reusable script permission was then used. An old Miniconda CA-store verification failure was corrected by using its maintained `certifi` CA bundle; TLS verification remained enabled. Public 403 responses were retained as failures and not bypassed. LIST 500 errors and error JSON remain explicit failures. Process enumeration through CIM was denied; a subsequent ordinary `Get-Process python` returned no active Python process. Known owned sessions were checked/closed: 52615 and 73187 returned completed exit 0; all other known session IDs were already closed. Deferred exec cell 59 no longer existed. **No owned acquisition process was observed active at handoff.** No new request was started during this local handoff.

Everything remains local, uncommitted, unpushed, and unpublished by this agent. Resume only from the saved current files after new user direction; preserve unrelated work and existing Twinkles.
