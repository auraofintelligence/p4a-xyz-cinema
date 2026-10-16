# Election Refresh Log

Append-only. One line per jurisdiction per run: date, state, outcome, sources checked.
A "no change" line means the sources were checked and the site data still matches.

## 2026-07-14

- qld: CHANGED — Stafford by-election (held 2026-05-16) applied: Luke Richmond (Labor) retained the seat, 51.3–48.7 2PP, ~4% swing against Labor. ALP 35→36, Vacant row removed, statuses and notes updated across all layers. Sources: antonygreen.com.au/stafford-by-election-results/, results.elections.qld.gov.au/Stafford2026.
- nsw, vic, wa, sa, tas, act, nt: not checked this run (Stafford-only update).

## 2026-10-02

- vic: CHANGED — Premier Ben Carroll (sworn 28 July); Assembly 87 members plus Brunswick vacancy; Council composition refreshed from official member CSV and September chamber lists. Updated election calendar and Melbourne calendar-day handling. Added official unsimplified geometry (88 districts, eight regions), dated electorate profiles and historical-result links. Superseded May state JSON and June 2025 Council observation retained in [dated archive](archive/2026-10-02-victoria-refresh.md). Sources and exact periods recorded there. Other jurisdictions not researched in this run.

- vic numerical completion: added 96 dated VEC result records (including Mulgrave 18 November 2023, Narracan supplementary and subsequent by-elections), 440 exact Census workbook observations across 88 districts, and constituent-district Census tables for eight regions. Primary, preference-distribution, indicative 2CP and 2PP tables stay distinct. Verified the 11 August 2026 removal of Council group voting tickets; no stale one-box instructions were found in the existing Victoria material. Added current VEC instructions. No voting-centre layer is published.


### Local-file, sorting and representation follow-up

Fixed direct `file://` loading through lossless classic-script geometry payloads; no browser bypass or local server is required. Grouped the map footer into four compact link groups. Added verified alphabetical/population/area/age/rent/household-income sorting, withholding volunteering/rented-tenure percentages pending denominator verification. Seven verified fields provide 616 dated district values. Region medians are not inferred.

Added geographic/current-party colour explanations, truthful five-member Council-region compositions and keyboard-accessible current Assembly/Council seat schematics. Majority markers (45/88 and 21/40) are separate from actual voting procedure; current parties are not predictions or assumed alliances. Local-government councils remain a distinct planned next layer, documented in `content/electorates/vic-implementation.md`; no council statistics are fabricated.


### Actual local-government atlas checkpoint

Added a separate local layer for 79 municipalities and eight unincorporated areas, plus 467 source ward/electoral-area features. Profiles include verified current rosters/vacancies, Moira administration, source election-history links and 1,975 annual ABS population observations (2001–2025). Statistical geography and legal boundaries remain explicitly distinct. Added many-to-many state-electorate intersections, including disclosed source slivers/topology defects. Original geometry is preserved exactly and both added layers support direct-file loading. Finance/service figures remain unavailable after the official LGPRF download returned HTTP 403 and other reuse terms remain unchecked. No navigation redesign, commit, push or publication is included.


### 2026-10-02 — Victoria interaction, representation and source-use completion

- Fixed ward navigation alignment and All Victoria reset; desktop/mobile file/HTTP, repeat/loading/reset/deep-link/history/keyboard checks pass.
- Added separately labelled RAP/RSA statutory layers with community-led cultural source links; 16 exact geometries, 35 independent interior/overlap fixtures, complete multiple-match selection and empty-layer explanations. Native-title geometry remains source-link-only.
- Replaced party-grid chambers with official-source physical member positions (Assembly 11 August plan / current occupancy separately dated; Council graphical source retrieved 2 October). Preserved current totals, vacancy and procedural distinctions.
- Added 769 deeper public representative/administrator profiles, area/representation/election sections, explicit seasonal preferences and disclosed unverified candidate coverage; improved gold heading/link contrast.
- Verified all six map deliveries: 4,020,843 unchanged vertices, properties and rings. Numerical regression: 616 exact Census cells and 96 VEC source snapshots remain valid. Added source hashes and QA reports under `tools/vic-qa/`.
- Added human/agent-readable source-use register for the stated personal/public non-commercial purpose, including political-party/commercial/fundraising/redistribution review triggers. Verified VEC main-site CC BY terms and LGV conditional non-commercial terms; LGPRF HTTP 403 remains an access limitation. `LICENCE.md` is unchanged.
- No commit, push, deployment, external message or screenshot upload was performed. Existing May archives and older history research dates remain intact; this was not a fresh history audit.


## 2026-10-02 — Victoria election doorway and sourced candidate directory

Added `states/vic/election/index.html`, generated from `content/elections/vic-2026.json` and `tools/templates/vic-election.html` by `tools/build-vic-election.py`. Public newcomer paths connect place, candidates, standing, councils, First Peoples and Parliament. Prominent links added to the Victoria landing, atlas, shared navigation and site index; the state generator preserves the doorway.

Reconciled four research handoff parts to **482 distinct records: 407 Assembly, 75 Council, 14 affiliations**. 481 announced and one explicitly preselected; zero formal VEC nominations asserted. All records join an existing electorate. Source-domain, party, chamber, status and text filters have shareable URLs; all records remain readable without JavaScript. Atlas election panels use the same canonical candidate source. Candidate sources/raw handoff, coverage gaps and separate historical/manual-review events are preserved in `content/elections/`.

Current primary directory plus agreeing profile resolves AJP Chloe Nicolosi to Bundoora and Rachel Unicomb to Broadmeadows; conflicting pod assignments remain visible, not duplicated. Socialist Alliance affiliation is distinct from a registered ballot label; no Council ticket order or incumbent recontest is inferred. Matthew De Angelis is Sydenham. Missing coverage is not absence/withdrawal. Earlier empty-candidate checkpoint is superseded by this dated source pass.

The guide separates the passed **1 June** new-party application deadline from 4–9 November candidate nominations, with appointment, deposit, group, voting and practical source links. Later affiliation/registration and potential electoral authorisation/finance duties are distinguished. Project licence unchanged; non-commercial purpose alone does not determine electoral duties. No applications, private nominator details or money collected.

QA: file/HTTP at 1440px and 390px, all filter values, deep-link restoration, no-JS 482-card coverage, all 96 atlas candidate joins, local links, visible focus, gold headings/links, compact footer, syntax, diff checks and reproducible scoped generators. Reports in `tools/vic-qa/election-*.json`. Managed browser-extension import errors are recorded separately from zero page runtime errors. Local QA screenshots were inspected only, not published. No commit, push or deployment.


## 2026-10-02 — Distinct sibling links and external-link behaviour

Added Native Nations and clarified the existing Oceania link in shared navigation/site map. Added two distinct outbound cards to the existing Treaty Atlas and its Markdown source; no duplicate hub or new national Indigenous map. Both exact public destinations returned HTTP 200. Native Nations remains a global nation-led workbench with its own onboarding; Oceania remains regional places, relationships, political geography and shared currents. No sibling repository was edited.

`assets/external-links.js` is the shared policy loaded by `script.js` and `assets/site-nav.js`. It covers initial anchors, inserted profiles, changed hrefs and synchronous click/auxclick. External HTTP(S) links use `_blank` plus `noopener noreferrer`; same-site/relative navigation and mailto/tel/download semantics remain intact. GitHub Pages sibling repositories count as external even on the same origin. Static Victoria generators use `tools/web_link_policy.py`; foundation external-card rendering retains both rel tokens. Source/template updates survive regeneration.

QA: eight sibling-navigation runs and twenty page/protocol/viewport link audits (file/HTTP, 1440/390), thirteen hosted/file classification cases, actual sibling new-tab openings, dynamic profile links, special-link preservation, no overflow, syntax and stable map/election rebuilds. Evidence: `tools/link-qa/`. Canonical Victoria candidate data and unrelated existing work preserved; only authorised link behaviour changed. Local-only, no commit/push/deployment.


## 2026-10-02 — Candidate information first

Reordered the atlas election tab: selected area, concise election date, candidate names/parties/status/actions, then current-member context and collapsed coverage/nomination notes. Removed the visible empty status schema. Candidate names and Details open a compact native dialog; source dates and provenance are expandable, and candidate person links restore from the URL. No unavailable profile/date fields are displayed. Essential unregistered-affiliation and source-discrepancy indicators remain available.

The election directory now leads with filters and name-first cards. Coverage notes are collapsed; only populated status options are generated. Profile/source/electorate actions align across cards. Gold headings, mobile spacing and existing external-link behaviour are retained. All 482 source records and their dates/statuses are unchanged.

QA: Kew’s five named candidates, a multi-candidate Council region, a synthetic empty-coverage fixture, keyboard dialog/disclosure activation, close-focus return, candidate permalink restoration, directory filters, external links and no overflow on file/HTTP at 1440px and 390px. Reproducible build and syntax checks pass. Report: `tools/vic-qa/candidate-order-report.json`. Local screenshots inspected only. No publication.


## 2026-10-02 — Homepage Victoria card and interactive issue ticker

Added a Melbourne-calendar election countdown with non-negative election-day/post-election states and direct guide/map links. Replaced the generic ticker with source-linked issues covering Victoria, AI, data centres, superannuation, tobacco, fuel, alcohol, food, housing and insurance. Official PM&C/Industry/ATO/VEC sources checked; no tax amounts, new allegations or enacted-law claims invented. Federal topics are labelled separately from the Victorian election. ATO direct web rendering was unavailable for some pages; official indexed guidance supported the limited category-level wording. Sources: `content/home-ticker.json`; prior generic topics: `content/archive/home-ticker-before-2026-10-02.json`. Hover/focus pause, phone pause/play, reduced motion and clone keyboard exclusion added. Documentation/About/sitemap refreshed for publication.

## 3 October 2026 publication recovery

- Completed all seven approved Connected projects cards and contextual links; retained the legacy sitemap anchor and Native Nations/Oceania connections. The rejected stale link batch was not added.
- Added the reviewed project generator and shared HTML finalization so source rebuilds retain the publication footer styles and external-link policy.
- Verified 99 pages, 4,836 local links and 24 file/HTTP desktop/mobile browser cases, plus Victoria geometry, Census/election arithmetic, council integrity and reproducible 482-candidate generation. See `tools/publication-qa/recovery-report.json`. These are local validation results; deployment must be verified separately.


## 3 October 2026 — Restore original ticker topics

The prior release incorrectly replaced the original ticker when additions were requested. Restored all 23 original topic labels verbatim and in their original order, followed by all 11 added political topics (34 items total). The old strip repeated its 23 labels twice solely for animation and contained no links or factual assertions; the restored labels now link to existing P4A topic pages. No original factual correction was needed. All 11 additional topic slots remain, with one-to-three-word political topic labels. Explanations are kept in source notes and linked destinations. The mismatched Payday Super item is corrected to the super-for-housing debate; the fuel link now opens ACCC market context. The alcohol topic links to the existing Beer tax issue page; other addition destinations remain unchanged. Bragg’s official 22 September speech explicitly describes ideas rather than settled Coalition policy, so no enacted access or settled party commitment is claimed.

`content/home-ticker.json` is the complete source. `tools/build-home-ticker.py` now checks the original archived inventory before generation to prevent replacement or deletion. Hover/focus pause, pause/play, reduced-motion support and usable links remain; animation duration scales with track width to keep the longer inventory readable. Only the ticker and its maintenance evidence changed.


## 3 October 2026 — Broader political ticker topics

Preserved all 23 original labels verbatim and in order. Renamed the AI jobs addition to the user’s “Job apocalypse” and linked the workforce-transition room, as a debate label rather than an established forecast. Appended Copyright, Data sovereignty, Child safety, Mental health, Gas prices, Corporate tax, Multinational tax avoidance and Resource profits. Consolidated Grocery prices, Housing affordability, Insurance premiums and Alcohol taxes under the preserved Food, Housing, Insurance and Beer tax topics; their previous records remain in the ticker source’s consolidation notes. Final inventory: 23 originals plus 15 distinct additions, 38 labels.

Official copyright/AI, eSafety, ACCC, Treasury and OECD sources inform the new destinations and notes. The gas/resources/data-centre connection is an editorial question about public benefit, control and costs. No blanket zero-tax claim or universal overseas-price comparison is made: royalties, company income tax and PRRT are distinguished; market, period, contract basis and costs matter to gas-price comparisons. No unrelated page sections were edited.

Resource profits opens the existing Public Assets room for public-return and extraction-rights discussion. Source notes distinguish resource ownership and extraction licences from surface Crown-land tenure, and do not claim a universal public opinion.

## 16 October 2026: Redland local journey pattern and refresh trail

- redland/qld local build: added a dated reusable agent pattern at `docs/agents/local-place-pattern.md`, place build-history at `content/history/redland.md` and event-driven local refresh triggers in the watchlist. The route extends the existing States -> Queensland -> councils -> Redland journey. Canonical local sources are `content/councils/redland.json` and `content/local/redland-connections.json`; generated pages remain a static reviewed snapshot. New local maps use actual attributed raster source maps, with source-specific terms and boundary dates retained.
- This entry records implementation guidance, not a fresh verification of all Queensland state facts, a declared mayoral vacancy, an announced by-election, a personal nomination or a completed clinical/AI system. Research observations keep their own dates; the build date does not redate them. Record source checks and completed-build validation separately after those checks occur. No commit, push or publication is authorised by this entry.
- Added the requested countdown pattern to guidance: shared hub/candidate timing from `content/local/redland-election.json`; 25 March 2028 is ECQ-rule-derived and subject to regulation (ECQ election events checked 16 October 2026). AEST calendar-day arrival is distinct from poll opening. Early-voting opening/closing dates and locations need a separate official notice, with unavailable dates kept null; the conditional by-election also keeps a null date and no timer pending official announcement. Documentation records the source check supplied by the build research, not an independent recheck by the documentation step.

## 17 October 2026: sourced national raster for the council entry journey

- Added the exact Wikimedia Commons PNG rendering of PoliticsMaps' 9 March 2024 Australian states map at `assets/maps/australian-states-wikipedia.png`, with CC0 attribution, original source/API/download URLs, source and retrieval dates, dimensions and hashes in `assets/maps/australian-states-wikipedia.json`. Original file page and API metadata checked 17 October 2026; PNG signature and hash checked and the image visually inspected. This is a general orientation map, not an electoral boundary dataset. Other 16 October source checks retain their own dates. Final site build validation is not claimed by this asset check.

## 17 October 2026: Redland local first-pass validation

- Completed the local-only eight-page journey and marked entry links. Official council map acquired through the public browser after direct-download errors; exact attribution and historical enrolment caveats retained. No election, early-voting window or candidacy inferred.
- Scoped checks passed: 844 local references, 43 connected records, 24 local Twinkles, 18 dated indicators and ten map records; JavaScript syntax; AEST clock before/on/after target; synthetic early-voting window before/during/after; private form's no-script protection; exact repeat-generation identity across 15 outputs.
- Browser checked: States -> Queensland -> councils -> Redland, search/related link/no-results/reset, malformed fragment resilience, private synthetic-note download and a 390px overview inspection. Source checks remain 16 October except individually dated 17 October asset acquisitions. Individual candidate dossiers and local vote collection remain unpopulated first-pass scope. Preview runs on loopback port 8768. No publication or push.

## 17 October 2026: replace the council doorway with the requested interactive map

- Added one reusable Canvas map directly on the Queensland portal and council directory. Source: current Queensland Government administrative boundary layer, ECQ spatial guidance, snapshot checked/retrieved 17 October; catalogue updated 15 October. Raw geometry and full source-specific rights retained. All 77 councils and separate Weipa Town area are searchable/selectable.
- Implemented drag, wheel/button/keyboard zoom, pinch handling, exact polygon selection and the Redlands opening route; other local portals remain explicitly unbuilt. Kept state political research dates unchanged.
- Fixed navigation and map-control wrapping at tablet and phone widths. Source/picking review, nine independent point fixtures, native browser drag/zoom/selection/search/reset, and 680px/390px overlap/overflow checks passed. The DPR2 fixture is synthetic, not physical touch-device evidence. No commit, push or publication.

## 17 October 2026: geographic raster alignment correction

- Replaced the misleading solid-water administrative display with the official QldMap Topo PNG below transparent council boundaries. The actual physical coast and island geography comes from the map service. Both base and boundaries use EPSG:3857, with the returned raster extent rather than guessed image placement. No SVG or synthetic geography.
- Retained unchanged PNG, export JSON and exact extent, source terms, publisher copyright year and 17 October retrieval metadata. Added online zoom-specific PNG detail using the same official service plus the retained local geographic fallback. Rechecked map selection and tablet/phone fixtures after reprojection; raw and delivered geometry identity and geographic-image hash checks added. No political dates changed; local-only build continues.

## 17 October 2026: quiet map styles, Redland divisions and local Twinkle pattern

- Scope: local Queensland -> Redland -> ten division journey. Default official QldBase_Pastel PNG reduces road contrast; optional Detailed roads uses QldMap Topo. Faint roads remain in the default. Soft transparent administrative colours are navigational, with no political meaning. Retain official raster geography, actual returned extents, source terms, copyright years and separate retrieval dates.
- Reused one generic widget/renderer and the same map/search/select/inspect/open interaction through the new ten division overviews. Redland's overview keeps one interactive map; historical map images remain in Sources & data. Current official councillor links are used, and missing division statistics remain unavailable rather than inferred from council-wide ABS figures.
- Current official division layer checked/retrieved 17 October 2026. The raw 2024 source has ten polygons, ten closed rings, 7,858 coordinate pairs and SHA-256 bc2cc7ef4994b49c93f1ddafd462352538e4db63e3f7c6f1be00b06e5a24b8bf. Provenance: content/councils/redland-divisions-sources.json; 2019 determination and 2024 spatial edition remain distinct. No SVG or geometry simplification.
- Local Twinkles now follow the existing content/rooms/twinkle.html#format: one gripe, one breath, a spoken seed, with serious context underneath and the canonical quiet-care guidance and rules. Expansion guidance appended to docs/agents/local-place-pattern.md; earlier history retained.
- Documentation records implementation and supplied source checks, not an additional QA pass. The main build verification records actual checks separately. Recheck when ECQ boundaries take effect, councillor records change, division-compatible statistics appear, map terms/extent/hash change, or Twinkle format is revised. Australia/Brisbane; no unrelated political research redated, no publication or push.

## 17 October 2026: page review register, sitemap, README and shared navigation

Recorded all 19 new local page routes and six rule versions with their actual update dates/review triggers, keeping source periods separate. Linked the register from Sources & dates, sitemap, README and shared Index/footer routes. Corrected the division directory's start stamp. Replaced the sitemap file tree with readable purpose groups/search and full 177-page coverage; consolidated both legacy sitemap builders under the durable human-sitemap generator. Canonical/public parity, repeatability, scoped links and existing Victoria checks pass. Browser search/Index/register and synthetic phone/tablet overlap/overflow checks pass; evidence is under qa/redland-20261017. Refreshed source-upload preparation only; no publication.

## 17 October 2026: licence-preserving crawler discovery

Added origin-root robots.txt, sitemap.xml and voluntary llms.txt from the recent Aura Genesis pattern, with 177 public routes and 24 evidence-backed implementation dates. Search discovery and the GPTBot training opt-out are separate; original and third-party rights remain unchanged. Durable generation, exact actual-route coverage, named search exclusions, licence Windows/Git byte variants, altered-licence rejection and local HTTP responses were checked. CI and the upload allowlist include the new files; README and agent rules link maintenance notes and review triggers. Evidence: qa/redland-20261017/discovery-results.json. No commit, push, deployment or search-console submission.

## 17 October 2026: reviewed song links and publication authorisation

Linked named Redlands song references directly to the user's individual lyric/context pages in i-C-infinity-music-universe. All eleven destinations returned HTTP 200 with lyrics; the canonical link register records the check. Meanings remain in place. Shared civic rules version 2.1 require reviewed per-song destinations rather than only a general music door. GitHub publication was authorised; preserve newer remote Aura/Twinkle work alongside the prepared local journey and record the published revision through Git history and Pages deployment status.
