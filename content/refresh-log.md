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
