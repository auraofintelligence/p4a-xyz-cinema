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

## 17 October 2026 — Scoped election maintenance guide

Documentation update only, requested for future individual by-elections at council/ward, state/territory and federal levels. Added `docs/agents/fractal-election-updates.md` version 1.0 and linked it from `AGENTS.md`, `README.md`, `REFRESH_WITH_AN_AGENT.md` and the watchlist. The guide covers current elected members/public profiles, previous contestants by event, shared countdowns, actual replacement processes, source dates, dependency-scoped generation, sitemap/navigation/links, checks and handover. Reconciled legacy state-only/manual-mirroring/automatic-commit instructions and recorded the rule in the review register. No political facts rechecked, election dates advanced, Twinkles authored or public HTML routes changed. This entry records local documentation work; it is not an election-source review or publication claim.

Validation: watchlist JSON and seven registered rule paths parse/resolve; 53 local documentation links resolve; the readable rule register was regenerated from its canonical record. Existing discovery checks pass for 177 public routes and 24 supported last-modified dates, preserving the licence and crawler policy. Independent review checked actual adapter commands, shared-output scope and the paired human/discovery grouping procedure. Whitespace checks pass. No commit, push or deployment.

## 17 October 2026: national expansion stopped for handoff

At the user's request, stopped national acquisition/implementation because repeated Allow prompts made the session burdensome. Saved `docs/agents/national-expansion-handoff-2026-10-17.md` and separate council, state, federal/ward handoffs under `content/places/qa/`. The owned preview server was stopped; all three source agents reported no remaining owned download sessions. This is a handoff, not a completion or fresh source-review claim.

The last generated national build has1,782place pages and33directories; discovery passed for1,992public routes. Canonical source additions and shared code have changed since that build, so generated pages and final national validation/contracts remain outstanding. The last full national validation failed and is stale. The handoff records current data counts, incomplete member/ballot coverage, cached but unmerged ward/current-boundary sources, the unfinished Tasmania council parser, three erroneous Tasmania candidate-header rows, actual browser/unit checks and remaining evidence work.

Raw source pages/PDFs are local-only under `content/places/raw/`, ignored by Git and excluded from public-source packaging; normalized public facts and licensed attributed maps remain distinct. A council-script TLS fallback was removed; two affected Queensland downloads were not used for canonical facts and failed subsequent normal certificate re-verification. Preserve that audit and access restrictions. No new Twinkles, commit, push or deployment. Reading the handoff does not authorise resuming acquisition; await a resume instruction and address permission workflow first.


## 17 October 2026: national work explicitly resumed and locally reviewed

The user resumed the saved handoff after changing authorization settings. Public sources were read through supported ordinary browser/HTTP paths; no certificate warning, authentication barrier, CAPTCHA or source restriction was bypassed. The earlier stopped snapshot and failed-access audit remain historical. No new Twinkles, staging, commit, push or deployment.

The synchronized local build now has **2,080 dedicated place pages and 33 directories**, with **49 delivered map layers**. Its 5,247 representative context records and 18,314 historical contestant context records are not unique people. TAS council rosters/87 contests, WA parent/106 exactly joined ward rosters, QLD 77 independent mayors/343 parent ballot contests and repaired child links, SA leaders/222 parent ballot contests, and NT 80 historical contexts/all 336 parent nominees were integrated. State additions include independent WA/NSW Council/NT rosters, SA2026 current districts and ballots, complete TAS Council geometry and division cycles, and NT/ACT intervening results. Current office, historical nominees, vote measures, exact postal deadlines and serving/historical/future boundary editions stay distinct.

The actual full national data/rendered-record/geometry/link validation passed; a repeat full build changed zero files. Browser evidence records 21 representative shared-renderer fixture outcomes, including 390/680 CSS-pixel frames, original Queensland/Redlands Open routes, Tasmania island selection, historical Frome/current Ngadjuri/future O'Donoghue, Back, keyboard, search, shared Index and retained raster fallback. These are not 2,113 browser reviews or physical touch tests or disabled-JavaScript browser sessions. Static text navigation is checked separately. Source records and deeper civic journeys remain incomplete; see the explicit report gaps.

The original page/rule dates were preserved and a separate national implementation register added. Discovery passed for 2,290 actual public routes with 2,137 evidenced lastmod dates and unchanged licence/crawler rights. Raw original research pages/PDFs/contact directories moved or remain under ignored `content/places/raw/`, including federal originals now in `raw/federal/`. Exact licensed geometry remains public; the optional 179 MB TAS expanded duplicate is excluded while its 61.2 MB gzip preserves all points. Scoped Git attributes preserve reviewed hashes across Windows/Linux; CI checks avoid replacing saved acceptance reports. Source-specific rights and live source gaps remain explicit.

See [the resumed report](../docs/releases/2026-10-17-national-expansion-resumed.md), [final build review](places/qa/final-build-review.json), [national validation](places/qa/national-validation.json), [actual browser review](places/qa/browser-review.json), and [the national implementation register](history/national-place-review-register-2026-10-17.json). This records the local implementation snapshot and its limits; publication remains separate.

Final scoped acceptance: all 2,081 registered contracts passed (2,080 new structural route/identity declarations plus the existing Redlands contract). The actual public-only copy also passed the national validator with saved evidence unchanged; its freshness guard checked 2,228 mandatory public artifacts and separately recorded 830 intentionally absent local-only originals. No remote workflow was run. Upload preparation has its own external manifest, outside this checkout.


## 17 October 2026: correct national directory styling after user review

The user screenshot exposed a visible failure missed by the earlier smoke review: national directory H2s inherited the global cinematic size/stretch/case, while `overflow-wrap:anywhere` split state names into oversized fragments. This was an implementation and visual-review mistake. Applied the original state-card Archivo scale/title case, normal name wrapping, original panel/width/radius tokens and the actual self-hosted mono font token. The global style guide, canonical people/events and exact geometry were unchanged.

Fresh browser evidence checks eight actual shared-style fixtures, including all eight national card titles after fonts settle at 390, 680 and 1200 CSS px, a long ward, council person/clock styling, TAS search/select/Open and shared Index. No broken heading words, page overflow or measured map-control overlap in those samples. The default full national structural/source validation passed again. Prior evidence and the earlier upload snapshot remain historical; corrected contracts and the separate typography-corrected package bind the current bytes. Broader per-place source, physical touch and accessibility gaps remain explicit.

After the typography correction, all 2,081 registered contracts passed again with zero failures, binding 3,058 national artifacts and 15 fresh browser artifacts. The corrected public-source package is prepared separately under `national-expansion-2026-10-17-typography-corrected`; its external manifest records the actual archive integrity result. No staging, commit, push or deployment.


## 17 October 2026: restore the original shared Index hierarchy

The user identified council/electorate navigation overtaking Start here and the original thematic navigation. Restored the six primary themes first in 01–06 order: Start here, The spark, The system, The ground game, Culture, States and territories. The original Start here destinations and unrelated Key policy ideas data remain. Council, electorate and Redlands discovery now sits inside States and the deeper state/map pages. Link lists start collapsed in a responsive grid; native summaries open each list, search reveals matching links, and clearing the search restores the previous expanded groups. Original site font and colour conventions remain.

Removed the Redland generator's shared-navigation prepend logic. The implementation workflow ran it after this change and verified identical shared-navigation bytes before and after. Updated the root and national-place agent rules to preserve this hierarchy on future scoped builds. Canonical source facts, event dates, geometry and the earlier coverage gaps remain unchanged; this is not a new political source review.

The full national validator passed again with 1,002,502 assertions and 3,058 bound artifacts. Fresh navigation browser review and actual fixture/path counts, current contract acceptance and preparation of `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-navigation-corrected` are pending at this documentation step. Earlier typography/browser/contract/package results above remain dated history and do not certify this correction. Record the actual final checks and external archive manifest when they finish. No stage, commit, push, deployment or remote workflow.


### Navigation correction: completed browser and discovery checks

Fresh navigation browser review passed exactly ten fixtures across four HTML paths: home, national places, legacy Redlands and the navigation fixture. Responsive frames used 390, 680 and 1200 CSS px; all six primary themes were visible together at 1280 × 720 after fonts and transitions settled. Keyboard navigation, search/no-results/clear, Escape and the deeper Redlands link passed. Evidence is `content/places/qa/browser-review.json`; screenshots are `nav-original-order-desktop.png`, `nav-original-order-390.png`, `nav-original-order-680.png` and `nav-original-order-1200.png` in the same QA directory. This is a shared-navigation sample, not physical-device, screen-reader or per-place source acceptance.

Fresh discovery passed 2,290 public pages and 2,137 evidenced lastmod dates. Redlands validation passed 19 pages, 1,526 local references, 43 records, 24 existing Twinkles, ten maps and 18 indicators; no new Twinkles were created. Current contract acceptance and the new navigation-corrected package/archive manifest remain pending. Earlier pending-at-documentation wording above records that earlier step; these actual results supersede its browser/discovery placeholders without advancing any political source dates. No stage, commit, push, deployment or remote workflow.


### Navigation correction: final contract acceptance and external package manifest

All 2,081 registered contracts passed with zero failures: 2,080 structural route/identity contracts and the existing legacy Redlands contract. Freshness bound 3,058 national artifacts and 13 browser artifacts; the declarations checked 2,100 routes and 177,871 local references. Contract generation took 34.380 seconds and verification took 409.848 seconds. The ten-fixture/four-path navigation browser review and discovery checks recorded above are complete; the earlier pending-at-step contract/browser wording remains historical.

Packaging outcome authority is the adjacent external JSON manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-navigation-corrected`. It records the actual preparation/archive outcome, included-path hashes and byte verification outside the source tree, avoiding self-referential archive hashes. Package status is external-manifest; this source log does not claim package PASS. Earlier typography/resumed bundles remain superseded historical snapshots. Political source gaps and dates are preserved. No stage, commit, push, deployment or remote workflow.


## 17 October 2026: put the human ideas at the Start here front door

The user rejected a mechanically restored but sparse Start list and asked us to choose the ideas that carry the site's purpose. Chose nine direct entries in order: Aura Genesis Protocol, Truth Engine, Musicverse, C-Hour & Braided Economy, Worker mutuals, Web3 Sensorium, Sovereignty Stack, Purple Synthesis and Cyber-Republic Simulator. Start here opens by default; six major-theme shortcut buttons stay above it, with seven bearings links including the civic pathway below. Council/electorate/Redlands discovery remains inside States. Existing font, colour and panel tokens remain. The choice follows the original homepage/civic-pathway journey through stories, meaning, trust, care and possible futures; it is not a claim that the literal historical Start list held these nine links.

Updated maintenance rules to preserve this conceptual front door and the existing deeper navigation. New national, browser and contract checks are pending; the preceding completed navigation review and its 2,081-contract PASS remain archived history under `content/places/qa/pre-start-here-correction-2026-10-17/`. Target output is `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-start-here-corrected`; its adjacent external manifest records the actual packaging/archive/byte-verification outcome outside source. No package PASS is claimed. Source gaps, source dates, earlier records and publication limits are preserved. No code or QA changes are claimed by this documentation step; no stage, commit, push or deployment.


### Start here correction: completed national and browser review

Final-byte national validation passed 1,002,502 assertions with 3,058 bound artifacts. Fresh browser review passed exactly nine fixtures across eight tested HTML paths with 17 browser fingerprints. It verified all nine ideas visible at 1280 × 720; direct Genesis, Truth Engine and Musicverse journeys with Start breadcrumbs; keyboard theme-shortcut and first-idea navigation; search/no-results/clear; States jump, Escape and reopening at the Start here top; 390/680/1200 CSS-pixel frames; and home, national places, rabbit-hole policy and legacy Redlands contexts. Evidence is `content/places/qa/browser-review.json`, with `nav-start-here-desktop.png`, `nav-start-here-390.png`, `nav-start-here-680.png` and `nav-start-here-1200.png`. This remains a shared-interface sample, not physical-device or full per-place source acceptance.

Maintenance rules now require each Index reopen to return to Start here at the top. Earlier pending national/browser wording records the prior documentation step and is superseded by these actual results. Current contract acceptance remains pending. The start-here-corrected output keeps external-manifest packaging outcome authority; no package PASS, source-date advance, stage, commit, push or deployment is claimed.


### Start here correction: final current contracts and discovery

All 2,081 current contracts passed with zero failures: 2,080 structural route/identity declarations plus the existing legacy Redlands contract. Freshness bound 3,058 national artifacts and 17 browser artifacts; the declarations checked 2,100 routes and 177,871 local references. Contract generation took 33.182 seconds and verification 411.617 seconds, with 444.801 seconds total reported elapsed time. Fresh discovery passed 2,290 public routes and 2,137 evidenced lastmod dates. The final-byte national PASS and nine-fixture/eight-path browser review recorded above are complete; earlier pending-at-step wording remains chronological history.

Package status remains external-manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-start-here-corrected`. The adjacent external manifest is the authority for the actual preparation/archive outcome, included-path hashes and byte verification outside source. This source log claims no package PASS or archive SHA before creation. Earlier source/civic-journey gaps and dated reviews remain intact. No stage, commit, push, deployment or remote workflow.


## 17 October 2026: remove repeated shared navigation destinations

The user identified too much repetition in navigation. Removed the seven-link Key policy ideas category and ten repeated System/Culture links, including the civic-pathway duplicate: 154 entries become 137 entries with 137 unique destinations. The nine Start ideas, six original themes, default-open Start, shortcut/bearings behavior and original style/layout tokens remain. Each destination has one category home; Legal RAG stays in System and the meaningful Victoria query lens is preserved. The rabbit-hole policy generator removes its legacy Key navigation marker without reinserting a category; KEY still supplies policy cards and homepage links.

The actual homepage audit passed 137/137 uniqueness and six footer categories with no Key group. Full current national validation, browser acceptance and contracts are pending. The preceding completed Start here results remain archived under `content/places/qa/pre-nav-deduplication-2026-10-17/`; they do not certify the latest source cleanup. Target is `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-nav-deduplicated`, with adjacent external-manifest authority for the actual package/archive/byte-verification outcome. No package PASS is claimed. Earlier gaps, dates and chronological reviews remain intact; no stage, commit, push or deployment.


### Navigation source cleanup: fresh national and focused browser checks

Fresh national validation passed 1,002,502 assertions and 3,058 artifacts. Focused browser review passed five fixtures across three HTML paths (home, places through the frame and the navigation fixture), bound by nine fingerprints. It checked 137/137 unique destinations; retained chosen nine and six themes; System 40/Culture five distinct pages; retained Legal RAG; single core title entries in search; keyboard first-idea navigation; and no overflow at 390 CSS px. Evidence is `content/places/qa/browser-review.json` and `nav-deduplicated-desktop.png`. Truth Engine full-text search also returns a distinct UAP Twinkle whose description mentions it; this is relevant search coverage, not a repeated menu destination or a claim of one total result.

No CSS or event-handler change, repeated broader browser review or repeated Redlands review is claimed. The earlier Start review remains archived. This supersedes the previous pending national/browser step; current contracts remain pending. Packaging outcome remains external-manifest authority for the nav-deduplicated output, with no package PASS claimed. Source dates/gaps and publication limits remain unchanged.


## 18 October 2026: final navigation-deduplication contract acceptance

Final acceptance completed at **00:05:22 Australia/Brisbane on 18 October 2026** (`2026-10-18T00:05:22+10:00`; `2026-10-17T14:05:22Z`). All 2,081 contracts passed with zero failures, bound to 3,058 national artifacts and nine browser artifacts; 2,100 declared routes and 177,871 local references. Generation took 33.400 seconds, verification 408.147 seconds and total reported elapsed time 441.548 seconds. Fresh discovery passed 2,290 public routes and 2,137 evidenced lastmod dates. The prior 17 October pending-at-step entries remain chronological history. Implementation, source and focused browser dates remain 17 October; no fresh source currentness or repeated broader browser/Redlands review is implied.

Package outcome authority remains the adjacent external manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-17-nav-deduplicated`. The directory date is the implementation phase label; actual `preparedAt` may be 18 October and is recorded by that external manifest with the actual archive outcome, path hashes and byte verification. This source log claims no package PASS or archive SHA before creation. Source/civic-journey gaps, earlier review records and publication limits remain intact. No stage, commit, push, deployment or remote workflow.


## 18 October 2026: delete the misleading Culture navigation category

The user explicitly rejected the Culture category and chose deletion. Removed its shared Index section, shortcut and footer entry. The five remaining themes, numbered 01–05, are Start here, The spark, The system, The ground game and States and territories; the nine Start ideas stay unchanged. The Index now has 132 unique destinations. Five specialist pages remain on their existing Genesis clinical/political/fiction paths, with no relocation, new topic or Musicverse edit. No Culture placeholder or broad multicultural-coverage claim is added. The base shortcut grid uses five columns with existing style tokens. Readable sitemap label becomes Origins, music and imagination, preserving its group id/routes/membership.

Current national validation, actual browser acceptance/fixture counts, contracts and rebuilt discovery checks are pending. The preceding completed review remains archived under `content/places/qa/pre-culture-removal-2026-10-18/`; its 18 October 00:05:22 contract completion and older source/browser dates are preserved. Package outcome authority is the adjacent external manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-18-culture-removed`, outside source. No package PASS or archive SHA is claimed before creation. Earlier gaps and dated history remain intact; no stage, commit, push or deployment.


### Culture category deletion: completed browser and discovery checks

Actual browser review passed seven fixtures across six tested HTML paths with 12 exact-byte fingerprints. Views were native 1280 × 720, the user's 678 × 884 viewport and a real 390 CSS-pixel frame. Checks confirmed five categories/no Culture, 132 unique destinations, unchanged nine Start ideas, all five existing specialist links on Genesis, an actual clinical-page click/breadcrumb, States shortcut 05, and the precise Origins, music and imagination sitemap label with its 18 October date. Evidence is `content/places/qa/browser-review.json` (SHA-256 `627ca42c865e600db4b7c9905a45a6b97931e4698241b9dfa7bf5a643dfe3be3`) and `nav-no-culture-desktop.png`. This is sampled browser acceptance, not physical-device or complete per-place review.

Fresh discovery passed 2,290 public routes and 2,137 evidenced dates. These results supersede the earlier pending browser/discovery step; current national validation and contracts remain pending. Packaging retains external-manifest outcome authority at the 18 October culture-removed target, without a package PASS or archive SHA claim. Political source dates, earlier history and stated gaps remain unchanged.


### Culture category deletion: completed fresh national validation

Fresh national validation passed at `2026-10-18T01:54:30+10:00` in 111.261 seconds: 1,002,502 assertions, zero errors/warnings, 3,058 artifacts and 1,265 retained source hashes across 2,113 pages/2,080 places. The saved 646,636-byte report is `content/places/qa/national-validation.json`, SHA-256 `6c72ffd15887ae65897906cba4784b54cce03a94f04d47ef11a4742748ca3159`. Browser and discovery passes are recorded above. This supersedes the preceding pending-national step; current contracts remain pending and the actual package/archive outcome is left to the adjacent external manifest. No package PASS or archive SHA is claimed.


### Culture category deletion: final contract acceptance at 02:02:02 Brisbane

Final current acceptance passed at `2026-10-18T02:02:02+10:00` (`2026-10-17T16:02:02Z`): all 2,081 contracts, comprising 2,080 national structural declarations and one legacy contract, with zero failures. Freshness bound 3,058 national and 12 browser artifacts, with zero errors/absences. Declarations checked 2,100 routes and 177,871 local references. Generation took 33.454 seconds, verification 399.833 seconds and total reported elapsed time 433.289 seconds. The saved 1,238-byte report is `content/places/qa/contract-validation.json`, SHA-256 `1f48bf1c98ddb68d96b47877352a04fcb6702f1ddae2cc3a68e1c3c47921d350`. National, seven-fixture browser and discovery passes are recorded above; prior pending-at-step text remains chronological history.

Packaging still uses the adjacent external manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-18-culture-removed` as the authority for actual preparation/archive outcome, hashes and byte verification outside source. This documentation does not claim package PASS or an archive SHA before creation. Underlying political source dates, scoped gaps and prior completed reviews remain intact. No stage, commit, push, deployment or remote workflow.


## 18 October 2026: balanced Australia footer with eight state/territory portals

The user's final clarification replaces the interim Queensland-priority plan: the right footer is Australia, with exactly one portal for each of all eight states/territories. The States section uses an explicit STATES-derived footer list rather than its first six Index entries. Removed repeated state chips and excluded Minjerribah, Olympics and specialist Victoria links from that footer column. The full Index remains five themes/132 unique destinations/nine Start ideas, with existing state specialist links untouched. Only shared JavaScript changes; no new or reinvented Queensland topic pages.

Current national validation, actual browser fixture/path counts, contracts and discovery checks are pending. Completed Culture-removal acceptance is archived under `content/places/qa/pre-queensland-footer-2026-10-18/`; its prior dates/results remain historical. Package outcome authority is the adjacent external manifest for `G:\GithubLocal-PC\_upload-ready\national-expansion-2026-10-18-australia-footer`, outside source. No package PASS/archive SHA is claimed. Preserve earlier source dates, scoped gaps and chronology. No stage, commit, push or deployment.

## 23 October 2026: recovered national expansion publication review

Luke explicitly authorised focused publication. The original dirty checkout and later wiki work remain intact; publication is prepared in an isolated checkout of verified remote main 6e924cc. Existing source observations and the intentional absence of new grassroots Twinkles remain unchanged.

Fresh national validation passed 1,001,438 assertions across 2,080 places, 33 directories and 49 lossless map layers. Discovery passed 2,290 public routes and 2,137 evidenced lastmod dates. Victoria, Redlands, geometry, compressed-loader and clock checks passed. The actual sampled Chromium review covers five scenarios across six delivered HTML paths, including responsive directories, Index/footer behavior and council/state/federal maps.

The final complete contract run passed all 2,081 contracts with zero failures at 2026-10-23T11:49:38+10:00, after correcting only two stale shared-navigation pins identified in the preceding legacy Redlands declaration. The final rebuild changed zero files. Exact staged blob bytes match all 2,223 required national/browser evidence artifacts. Forty-two unrelated line-ending-only changes were excluded.

Seven expanded GeoJSON duplicates, totalling 348,541,152 bytes, remain local; exact gzip equality preserves every coordinate/ring/feature while keeping the public tree below Pages' 1 GB limit. No politician, candidate, event date or result was invented. Source/current-office/history and deeper-journey gaps remain documented. See docs/releases/2026-10-23-national-expansion-publication.md and the linked actual reports. This entry records local review before push; GitHub commit/workflow history and the publication handover establish the subsequent remote/deployment outcome.

### 23 October: cross-platform sitemap correction after deployment

Initial national commit a3057c1 deployed successfully; 18 live paths matched exact committed bytes. GitHub's civic workflow passed national validation, every contract and Redlands, then detected different bytes between the human sitemap source and public copy after Linux checkout. Windows text-mode writes combined with differing Git newline filters caused this portability defect.

The sitemap generator now writes one explicit UTF-8 byte string to both mirrors. Fresh discovery passes and the exact staged Git blobs match at 545,363 bytes. All national/browser evidence fingerprints remain unchanged and pass verification. This correction changes newline delivery only; political facts, dates, map geometry and coverage gaps remain unchanged. Its subsequent GitHub checks and Pages deployment require separate verification.


## 23 October 2026 — civic map navigation

Made the national map open state/territory electorate maps directly, moved map choices before state summaries, added reciprocal state/council/federal routes and compact phone controls, and removed public clone/tailoring/setup text. Political records, boundaries, source dates, licence and grassroots Twinkle exclusion are unchanged. Browser review: all eight phone entries/maps, WA layer/selection/Open/Back/Forward, ACT real local arrangements, NT tablet/desktop and federal return choices. See `docs/releases/2026-10-23-civic-navigation.md` and the dated QA files for actual validation and remaining limits. Publication outcome is recorded by GitHub commit and deployment history.


## 23 October 2026 — scoped state research refresh

Latest review is distinct from source publication, event, current-office and historical dates. The prior state snapshots are retained in `content/history/state-research-before-2026-10-23.json`; four official-source review manifests document successful reads, denied targets and partial coverage. No new grassroots Twinkles or geometry changes.

- ACT: 25 MLAs reconciled; summary10Labor/8Liberal/4Green/3independent; former Greens confidence-and-supply arrangement ended. June Kurrajong countback retained; formal declaration5June clarified. Redistribution suggestions close3Nov, comments4–17Nov; current geometry retained. Federal profiles inaccessible.
- NSW: Scruby/Pittwater corrects old named independent list; Govind elected15Oct to Council casual vacancy, resolving41/42roster gap. This is not a public by-election. Cobar28Nov; CoffsHarbour/HuntersHillSouth12Dec polls added; named roster removals remain follow-up after denied resignation reads.
- NT: September roster confirms17CLP/6Labor/2independent; Johnston identity join corrected toJustineDavis, Paech retained inGwoja. Mulka12Sep results already detailed and now in overview; Nightcliff official support retained. NTEC current-election index lists none. Milngin failed nomination round still no replacement date; local/federal review partial.
- QLD: 20Oct official roster confirms unchanged93party totals; Stafford result percentages retainJulycheck. TablelandsMayorKevinCardew, vacantDiv1 and TownsvilleDiv1MichelleHobson verified independently. Tablelands postal completion31Oct18:00, receipt10Nov17:00Brisbane; separate past mayoral/councillor polls preserved. Other local/federal records partial.
- SA: CurrentHA feed(lastupdated22May) verifiesALP33/IND5 includingSpeakerNatCook; historicalALPballot unchanged. Council summary alignsretained17OctON3/FamilyFirst1roster; freshcompleteLCAPI403. Final2026elected-orderCSV unchanged; council postalclose7Apr2027 17:00Adelaide rechecked; old404resultslink replaced.
- TAS: Currentofficial35MHA/15MLC lists checked; HelenBurnetIndependent and CaseyHiscuttIndependent. Huon/Rosevears countcompleted12May. Unsupportedexact2029House/May2027Council polls removed; no invented replacementdates. Ordinarycouncilpostalreceipt27Oct14:00Hobart(13:00Brisbane); individualcouncil/federalcoveragepartial.
- VIC: All127currentmembers/electorates/partiesmatchofficialCSV; Brunswickvacancyretained. CandidateHelpernowavailable; state nominations4Nov09:00–9Nov12:00Melbourne, poll28Nov. Sevennamedcouncileventshistory/processadded, includingOctoberBeale/Lockwood/Briarsresults andKinglakenominations27Octnoon/postalclose4Dec18:00. Candidatecampaign/legalchecksretainolderdates.
- WA: SecretHarbour29Augby-election/9Sepdeclaration added separately;16ballotnamesretainacceptedaffiliations andfinal2CPmeasure. DecemberCarnarvon/Coolgardie/Esperanceextraordinarypostalclose3Dec18:00Perth;Septemberaggregatecouncildeclarationsaddedwithwinner/rostergaps. Statepartyoverviewalignsretained17Octroster;freshParliament403, no blanketfreshcurrent-rosterclaim.

Integration and generators completed; validation, browser, staged evidence and publication outcomes are recorded in the release note and actual QA/GitHub reports. No earlier PASS is treated as acceptance of these new facts.

### 23 October 2026 - Layered council directories

At Luke's request, replace flattened statewide inventories with existing council, ward/division and detail pages. Victoria formerly listed 531 records (79 councils, eight unincorporated areas, 444 children). Apply council-first lists across all eight jurisdictions, separately label exceptional areas, preserve ACT/NT arrangements and all map layers, and retain child/parent links. No additional factual research or new pages is implied by this navigation correction. Validation/publication recorded with the state-research release.

### 23 October 2026 - Your Relevance private questionnaire

Adapt the completed source at australian-law-2012-lukes-relevance commit 97b523a9253f968dfe901b144cea8c32a52a9ed4, with attribution and retained licence. Twelve optional sections create an editable research brief; add explicit council/ward, state/territory and federal context and separate existing map links. Source observations, historical/future area identities and the earlier count reports remain unchanged. No answer upload, backend, political scoring, actual membership or electoral enrolment is added. Device saving is opt-in under a separate P4A key. Native rebuild/reset confirmation acceptance remains untested because approval to replace or clear synthetic QA data was not given; no alternative route is used. Functional/mobile review and publication outcomes are recorded in the questionnaire release/evidence.

## 28 October 2026 — Redland City mayoral vacancy

Scope: existing Redlands overview, People & elections and Sources & dates; news, process and polling/nomination countdown status only. Council confirms vacancy and a required by-election; ECQ event dates remain unannounced in the checked event listing. Canonical timing: content/local/redland-election.json, event redland-mayoral-vacancy-2026-10-28. Earlier conditional record retained. No national roster/geometry refresh or pending directory-cleanup publication. See docs/releases/2026-10-28-redland-mayoral-vacancy.md for sources, update instructions and actual validation/publication status.

## 29 October 2026 (Brisbane) — Capricornia future retirement announcement

User request received 28 October UTC. Michelle Landry's official announcement of 23 October says she will not recontest at the next federal election and intends to serve until then. Current Parliamentary Handbook API confirms PHID249764 in the current Parliament for Capricornia. Scoped canonical record: content/places/federal.json, federal-house-157. Existing member card/source list updated; 2025 results, boundaries and unannounced future election remain unchanged. No successor, new candidate, vacancy or by-election clock inferred. The prior place record and minimal verification facts are retained under content/places/history/ and sources/. Repository/source checks replace a new browser trial under the user's requested workflow; no personal browser used. See docs/releases/2026-10-29-capricornia-retirement.md for source/access details and actual publication handoff. Unrelated directory, seating and G: work untouched.

## 2026-10-29 — daily national election-notice review (Australia/Brisbane)

- VIC: CHANGED — Kinglake Ward's Jordyn Princi declared elected unopposed 28 October, 10am AEDT; no December vote. Reconciled existing event and current role, preserving prior timetable/history. State 28 November poll and 9 November noon AEDT nomination close reverified; no speculative candidates.
- TAS: CHANGED — all 29 council postal elections closed 27 October at 2pm AEDT; counting began 28 October at 9am. Progressive results, not a statewide final declaration. Individual winners/current offices not inferred.
- NSW: CHANGED — Cobar nominations closed 28 October noon AEDT; 28 November poll remains published. Paul Amos's Coffs Harbour resignation effective 14 October reconciled against the confirmed 12 December by-election. Coffs Harbour/Hunters Hill dates and 13 March 2027 state poll reverified.
- WA: CHANGED — removed resigned current-role entries for Simon Robinson (effective 9 October) and Gemma Johnston (August; exact day not confirmed). Bridgetown replacement process/date awaits WAEC advice; no poll assumed. Existing 3 December Carnarvon/Coolgardie/Esperance postal timetable retained; Carnarvon unopposed wards are not additional polls.
- QLD: NO MATERIAL CHANGE — Tablelands Division 1 postal completion 31 October 6pm AEST and receipt 10 November 5pm retained. Redland mayoral election and nomination countdowns remain “Awaiting confirmation to begin”; no official timetable located.
- SA: NO MATERIAL CHANGE — council receipt deadline 7 April 2027 5pm ACST and January/February ACDT enrolment/nomination milestones reverified; no additional supplementary poll found in inspected hubs.
- ACT: NO MATERIAL CHANGE — 21 October 2028 Assembly poll reverified. Redistribution milestones are administrative; the Rattenbury vacancy was already filled by countback, not a future poll.
- NT: NO MATERIAL CHANGE — NTEC homepage reports no current election. Mulka September election is past; no new future poll verified. August 2028 Assembly/August 2029 local-government months do not establish exact polling countdowns.
- Federal: NO MATERIAL CHANGE — AEC event/media review found no new future federal poll. The 26 October Farrer item concerns disclosure, not a new election. Capricornia future retirement remains distinct from an effective vacancy.
- Coverage: official AEC and all eight commission hubs/notices plus targeted parliament/council/government notices; not an exhaustive crawl of every council or gazette. Source links and scoped facts are in `content/places/sources/election-review-2026-10-29.json` and existing canonical event sources. APH homepage/House media returned403; direct Redland release access blocked (official index available); NTEC16September declaration timed out and inconsistent Milingimbi/Milngin label was not propagated. WA individual event-detail endpoints were empty, so WAEC22October notice and council corroboration were used; non-WAEC council coverage remains incomplete. Cobar snapshot lagged nomination close, so no ballot/outcome inferred. TAS individual declarations not checked. These gaps preclude exhaustive national vacancy assurance.

## 2026-10-30 — scoped election-notice reconciliation (Australia/Brisbane)

This entry supersedes the current-status conclusions of the 29 October entry where noted; that earlier check remains historical evidence. It does not certify a new exhaustive national vacancy audit.

- NSW: CHANGED — NSWEC's 29 October Cobar declaration elects Barry Knight unopposed; no vote is required and the earlier 28 November poll is superseded. Council minutes independently establish Harley Toomey's resignation effective 9 September. Hunters Hill's dated official news index confirms Marc Lane's immediate resignation on 15 October; his current-role entry is removed. Coffs Harbour and Hunters Hill South Ward polls remain 12 December, with nominations closing 11 November noon AEDT. Other councillors retain their earlier checks; no accepted ballot is inferred.
- QLD: CHANGED — Redland's 28 October mayoral vacancy and Julie Talty's acting arrangement are reconciled across the affected records. Council's 29 October decision is a request for a full postal ballot, subject to electoral approvals, not an approved method or timetable. ECQ polling and nomination dates remain unconfirmed; both targets are null and awaiting confirmation. The ordinary 2028 cycle remains separate.
- NT: CHANGED — Victoria Daly's direct official article confirms the Milngin Ward vacancy and a replacement by-election being arranged, with timetable awaiting NTEC. Conflicting indexed December dates are excluded. The failed August zero-nomination round remains historical and separate from the new pending event. No effective vacancy day, nominee or poll date is inferred.
- RETAINED 29 OCTOBER CHANGES — Kinglake unopposed declaration; 29 Tasmanian council events closed/counting with no inferred individual results/current office; Coffs Harbour, Bridgetown-Greenbushes and Esperance resignation corrections. Their actual source-check dates remain 29 October. Bridgetown's replacement process/date and Tasmanian individual declarations still need separate review. Unrelated state/federal records and geometry are not refreshed.
- Evidence/history: exact source references and event IDs are in [the 30 October release record](../docs/releases/2026-10-30-election-notices.md), `content/places/sources/election-review-2026-10-30.json` and the retained 29 October manifest. Council/ward histories preserve all 40 changed baseline records. Missing pre-29 October state overview snapshots were recovered exactly from baseline `923db63` on 30 October, with that reconstruction date explicitly labelled; prior NSW/QLD intermediate snapshots and older histories remain intact.
- Validation/delivery: intermediate read-only national validation reported 2,080 canonical places, 2,113 generated pages, 4,465 events and 18,382 contestants; these figures await the final rerun after corrections/regeneration. Focused Redland/VIC/clock tests and snapshot/mirror checks passed at their intermediate review points, not final aggregate acceptance. Cloud HTTP preview now works and fresh actual browser QA is underway. Final validation, browser evidence, contract/discovery reconciliation and publication remain pending; no final PASS or live-success claim is made.
- Access/coverage: Hunters Hill's detailed resignation page returned 403, but its dated official index was available. Redland's postal-request article was available through indexed official-publisher text while direct retrieval failed. Milngin's directly read article gives no confirmed timetable. The earlier scan's access gaps and incomplete individual council/roster coverage remain explicit; failed access is not a no-change result. Next triggers are official Redland/Milngin timetable notices, NSW accepted ballots, Tasmanian declarations and WA replacement-process/results notices.


### 30 October cloud validation follow-through

The cloud-only HTTP preview now passes focused actual-browser review at400/683/1191CSSpx (narrow400 uses ordinary zoom/window sizing, not a physical phone). Redland waiting clocks, Cobar completion, Milngin failed/pending separation, Talty role, state summaries and navigation were observed. Final national data validation passes2080places/4465events/18382contestants; all2081 scoped contracts pass. Prior snapshots and browser evidence are retained. Publication/CI/live verification remain separate pending steps; see `docs/releases/2026-10-30-election-notices.md` for scope and source-access gaps.

## 2026-10-31 — nine-commission election-notice review (Australia/Brisbane)

Checked 30 October UTC / 31 October Brisbane. Bounded official AEC and eight state/territory commission hub review with targeted notices; not exhaustive vacancy, gazette, minutes or individual-roster certification.

- **VIC changed:** Knox confirms Peter Lockwood's immediate 29 October resignation, Baird Ward vacancy and a required VEC by-election. Timetable and nomination dates remain unconfirmed.
- **NSW changed:** David Harris will not recontest Wyong at the 13 March 2027 election, but remains MP and continues ministerial duties until then. No current vacancy or by-election inferred. Earlier Cobar/December council events unchanged.
- **TAS changed:** TEC's 30 October update confirms all mayoral and most deputy mayoral counts complete; councillor outcomes mix final and provisional results. No individual winners/current offices, statewide final declaration or completion date inferred.
- **QLD retained:** Tablelands Division 1 completion 31 October 6 pm AEST and receipt 10 November 5 pm AEST; deadlines not elapsed at review. Redland postal request is not approval; timetable remains unknown.
- **WA retained:** 3 December 6 pm AWST contested extraordinary polls; Carnarvon Coral Bay/Plantation unopposed positions distinct. Bridgetown replacement process and timetable still await advice.
- **SA retained:** Supplementary-election list readable, no new material change found; April 2027 council timetable unchanged.
- **ACT retained:** Rattenbury vacancy already filled by Vassarotti countback; 3 November redistribution deadline is not a poll.
- **NT retained:** Current-election hub reports none; Milngin failed zero-nomination round and pending replacement remain separate, with no new date verified.
- **Federal retained:** No new future poll or vacancy found in targeted AEC/APH checks; Farrer May election and October disclosure item are not new polls.
- **Coverage gaps:** APH individual profile 403; Queensland Gazette PDFs not inspected; ACT reminder article cache miss with homepage available; differing crawl ages; TEC individual result tables not exposed. Vision6 release was read through direct retrieval after web-reader failure. NSW's announced maintenance was upcoming, not a failed check. No failed access is converted into no-change assurance.
- **Implementation:** prior state/council/ward records archived; scoped canonical facts and affected state summaries/mirror updated, with narrow HTML dependency substitutions because PowerShell is unavailable. Unrelated dates, geometry, officeholders and historical ballots preserved. State parity/syntax and scoped checks pass; current-run aggregate acceptance/publication remains separate. See [31 October release note](../docs/releases/2026-10-31-election-notices.md) for source links, exact scope and integration status.
- **Prior delivery correction:** the retained 30 October `final-retention-report.json` establishes commit `d83e0020240e1de649982557f2933667d547b361` published, successful civic CI/Pages and 56/56 live-file matches at 09:37:01 UTC. Earlier pending prose is historical. This does not establish publication of the current 31 October edits.
- **Final local acceptance:** all 18 aggregate checks and 2,081 registered contracts pass. Actual cloud-browser review covers 11 named pages and narrow navigation. Publication requires the exact remote commit, successful CI/Pages and live-byte match; local acceptance alone is not delivery.
