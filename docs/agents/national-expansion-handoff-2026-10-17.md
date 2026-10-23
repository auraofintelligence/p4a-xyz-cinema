# National civic expansion handoff

**Historical stop snapshot, superseded for current implementation status.** The user explicitly resumed work later on 17 October after changing authorization settings. See [the resumed report](../releases/2026-10-17-national-expansion-resumed.md) and its linked current evidence. The original handoff below is preserved as the record of the stop; its counts, missing integrations and pending checks describe that earlier point.

17 October 2026, Australia/Brisbane. Repository: `G:\GithubLocal-PC\p4a-xyz-cinema`.

**Status: stopped at the user's request for a handoff. The national expansion is unfinished. No changes from this expansion have been committed, pushed or deployed.** The user is tired of repeated Allow prompts. Do not resume downloads merely by reading this document; wait for an instruction to resume, then address the permission workflow before beginning further acquisition.

## Requested outcome and constraints

Follow [Victoria/Redlands lessons](victoria-redlands-lessons.md) to build the other states and territories through real councils, council electoral areas, state/territory electorates and federal electorates. Include maps, dedicated pages, links, countdowns, dated current elected members and public profiles/sites, and previous-election contestants. Preserve Victoria's deeper atlas and the existing Redlands journey. **Create no new Twinkles; those belong to grassroots implementation.**

The user approved implementation after seeing a plan. They also requested an agent guide with a fractal maintenance process for a single future by-election, including sitemap/link updates and boundary changes. Use only legally accessible data, honour source rights/access restrictions, retain attribution and avoid publishing private contact data. Approval to implement locally does not establish publication authorisation for this expansion.

## What exists locally

Last completed national page build: **1,782 dedicated place pages plus 33 national/jurisdiction/institution directories**. The generated route registry has **44 layers**. The human/XML/assistant discovery build covers **1,992 public HTML routes**, including existing site pages. These counts describe built routes, not complete individual data or fully reviewed local journeys.

At the local handoff inspection, canonical inputs contained:

| Input | Place records | Representative records | Event-specific contestant records |
| --- | ---: | ---: | ---: |
| `content/places/councils.json` | 1,182 | 2,372 | 7,639 |
| `content/places/state.json` | 441 | 480 | 3,278 |
| `content/places/federal.json` | 159 | 226 | 1,468 |

These are **records**, not unique people: council/ward contexts and separate contests can repeat a person. Named vacancies can also be roster records. The level-specific handoffs below give the latest saved state if their local finalisation changed these counts.

- [Council handoff](../../content/places/qa/council-handoff-2026-10-17.md).
- [State/territory handoff](../../content/places/qa/state-handoff-2026-10-17.md).
- [Federal and ward-source handoff](../../content/places/qa/federal-and-ward-handoff-2026-10-17.md).

### Shared implementation

- Canonical inputs: `content/places/{councils,state,federal}.json` with stable IDs, sources, dated representatives, event-specific contestants, primary geometry joins and alternate-edition `mapRefs`.
- Generator: `tools/build-national-places.py`. Supports `--place <stable-id>`, `--jurisdiction <slug>` and `--scope councils|state|federal`. A place update also rebuilds genuine shared/same-layer dependants; it does not promise that only one file changes.
- Presentation: `assets/civic-places.js` and `.css`. One Canvas map per overview, pan/zoom/keyboard/touch handling, whole original polygons, holes/multipart picking, source-layer switching, search → select → inspect → Open, URL selection and Back, linked static text directories, source credits and clocks using local time zones. Exact postal deadlines use canonical `dateTime` and `milestoneLabel`.
- The latest renderer/generator supports **several original features sharing one place** through grouped `featureIds`, preserving all original geometry. This fixes NSW unincorporated areas and is needed for the NT/WA multi-part ward supplement. The full pages have not been rebuilt since this final implementation change.
- Official Geoscience Australia raster context is retained with its actual EPSG3857 returned extent and copyright/licence record; online zoom detail has a local fallback. Shapes remain source geometry, with CRS/display limits stated.
- Senate/statewide upper-house maps use expressly labelled jurisdiction geographic context, not invented electoral subdivisions or legal voting-entitlement polygons.
- Original Queensland council search/Open now links into new council pages through `assets/qld-place-routes.js`; code 6250 still opens the existing Redland hub. Legacy generator hooks restore these additive links.
- `assets/site-nav.js`, both discovery builders and existing state/maps entry pages contain national place gateways. Do not hand-edit generated copies and forget their generators.

### Federal portion

The federal data acquisition is complete within its declared source scope: 150 serving House divisions, eight Senate areas, and a separate future O'Donoghue record. Current 226 parliamentarians are independently sourced from the official Parliamentary Handbook roster. Prior data includes 2025 House/Senate contestants and the 2026 Farrer by-election. Current versus next-election 2026 SA/TAS/ACT maps remain separate. Grey retains serving representation/history; O'Donoghue has no invented current member or previous election under the new edition.

Some official APH profile URLs reject automated HTTP reads; canonical public links are supplied without claiming they all returned200. This portion has its own source/hash/coordinate and AEC link checks. It is still affected by shared final-page QA and regeneration requirements below.

### Maintenance guidance

[Fractal election updates](fractal-election-updates.md), currently version1.1, and [the canonical-data agent file](../../content/places/AGENTS.md) document the same identify → verify → canonical edit → dependants → check → record process at every scale. They cover by-elections, current office versus contestants, exact deadlines, source dates, boundary proposals/final/effective/first-election stages, predecessor/successor routes, histories, geometry preservation, sitemap/navigation and handover.

Root `AGENTS.md`, README, refresh instructions/watchlist and the refresh log link to the guide. The rule register still needs reconciliation with the latest guide version and final national page review; do not claim this has already been completed.

## What remains

1. **Complete source integration and coverage.** Council rosters and historical ballots remain the largest gaps, especially QLD/SA/WA/NT and some VIC/NSW exceptions. State data has substantial current-member/results additions, but WA has no current members entered, NSW upper house is missing, NT Karama is missing and SA's old Frome map does not join the current Ngadjuri member. State historical data has no SA contestants entered yet. **Remove three erroneously parsed TAS2025Shooter/Fisher/Farmer group-header rows from the candidate records using the source; these are not three people.** Preserve the official current roster independently of past winners. See the exact state handoff audit before describing completeness.
2. **Merge already acquired ward supplements.** `content/places/council-ward-supplement.json` supplies51NT wards and113WA wards with1,032 original polygon parts and exact nativeEPSG4283 coordinates. `content/places/sources/council-sa-ward-supplement.json` plus `assets/maps/national/council-sa-wards.geojson` supplies140LocationSA source features. Join only real wards to verified parents; undivided/administrative placeholders become parent context, not invented wards. NSW ward coverage is still incomplete. Do not republish restrictive Landgate/NorthSydney data merely because it can be read.
3. **Resolve current boundary editions using already cached sources first.** The state agent identified that the May2025 national SA layer still contains Frome whereas the current2026 roster uses Ngadjuri. **The official2026SAgeometry and HA/LCresults are already downloaded and registered**, but still need normalisation/integration; preserve the older edition and do not rename an old polygon. **All15officialTASLegislativeCouncilZIPs are already downloaded in nativeEPSG28355**, alongside13successfulEPSG4326feature queries. Convert the complete licensed original ZIP data faithfully and verify source coordinates/parts rather than repeating the two failed query requests. All15LCpages currently lack layer IDs. The state handoff lists the actual retained paths.
4. **Finish the root's Tasmania council supplement.** See the precise WIP below. It is not merged into `councils.json` yet.
5. **Regenerate all affected pages.** Canonical data and shared code were changed after the last full build; generated pages/registry/geometry delivery are not the final synchronised build. All acquired-but-unmerged supplements must be handled first.
6. **Run fresh final QA.** The saved national validation is a FAIL from an earlier data snapshot, with16,731errors dominated by missing vote-measure labels and duplicated VIC event IDs. At stop, the council agent locally confirmed zero duplicate event IDs and zero votes lacking a vote measure after fixing its import/upsert. This is not a full final validation. Do not assume every failure is fixed, delete the report, lower checks or copy a PASS. Rebuild and rerun the default validator with source hashes.
7. **Finish browser evidence/contracts.** Save actual browser fixtures in `content/places/qa/browser-review.json`; this file has not been completed. Generate per-place contracts only after fresh default structural validation and genuine browser evidence pass. The original Redland contract fingerprints for changed Queensland map/widget code are stale and need an affected recheck and a truthful evidence update.
8. **Finish discovery/review records.** Register the new national pages and reviewed implementation dates, update guide versions/level-specific coverage and release notes, regenerate the legacy source register where affected, then rebuild human sitemap, inventory, XML sitemap and `llms.txt` and rerun discovery. Preserve original research dates, historic review evidence and crawler/licence policy.
9. **Final review.** Check intended diff/untracked files, large-file/public-source packaging limits, source rights and local-only exclusions. Run a deterministic second build only after final changes. Report remaining inaccessible factual coverage honestly. No commit/push/deploy has been performed or prepared as an approved final publication step.

### Root's unfinished Tasmania supplement

`tools/acquire-tas-council-details.py` uses BeautifulSoup4, available in the existing Python3.9 environment. The bundled Python has no BeautifulSoup4. It safely uses normal verified HTTPS and has already retained all29 official TEC MyReps council responses through the published council-selection form, using council codes only: **no street addresses or authentication**. MyReps explicitly says its roster was last updated31July2026; keep that as-at date distinct from17October checking.

The council agent already retained all29TEC2022 results pages and their live include fragments under `content/places/raw/council-tas-2022*`. The script reuses them, parses councillor first-preference tables and mayor/deputy horizontal first-count tables, checks published candidate counts, ignores commented-out fragments, and handles explicitly named unopposed declarations. Do not infer current members from these2022 winners.

**The script currently fails** at Kingborough current-roster reconciliation `(12,10)`, so `content/places/tas-council-details.json` has not been successfully produced. Previously fixed DerwentValley has six named councillors plus two expressly stated vacancies. Kingborough requires a careful, sourced correction:

- The TEC source lists a mayoral vacancy, DeputyMayor `Christian Street`, and ten councillor positions, including `Christians Street` (source spelling) and two councillor vacancies. Counting a mayoral vacancy as an extra councillor and treating the spelling discrepancy as another person produces the failure.
- Verify council positions separately from leadership roles; an acting mayor/vacant mayoral office does not create another councillor seat. Retain explicit vacancies accurately.
- Independent official Kingborough publications support **Christian Street**, ActingMayor: [19June2026budget](https://www.kingborough.tas.gov.au/2026/06/council-budget-26-27/), [4August2026notice](https://www.kingborough.tas.gov.au/2026/08/names-to-go-the-distance/), [7September2026notice](https://www.kingborough.tas.gov.au/2026/09/turf-maintenance-program-underway-across-kingborough/), and [15June2026agenda](https://assets.kingborough.tas.gov.au/uploads/2026/06/Agenda-No.-11-15-June-2026-Public-Copy.pdf). These were read through the web tool; download no full document unless necessary and keep originals local-only.
- Fix that specific supported discrepancy with recorded provenance; do not add a broad fuzzy name merger. Continue reconciling all29rosters and87contests. Keep each event/office distinct, then deliver the minimal supplement to the council adapter for merging. The current script depends on the other adapter's retained fragments and needs that dependency documented or a controlled missing-source acquisition option.

## Verification actually completed

- Delivered civic countdown code:14fixed-time cases passed, including before/on/after local dates, Australian DST, Perth/Brisbane, leap year, unknown date and exact TAS/SA postal deadlines.
- Delivered Canvas controller: synthetic holes, multipart components, several original features sharing one page, neighbour/water, projection round trips, zoom/reset passed. Synthetic fixtures do not certify every real polygon or physical touch behaviour.
- Existing Victoria map validator and original Redland geometry/journey/clock checks passed earlier in the build. Later shared/source changes still require appropriate reruns; no blanket final PASS is claimed.
- Discovery passed for1,992routes and24previously evidenced lastmod dates. New national page review dates are not yet registered. Crawler policy and project licence remained unchanged.
- Browser smoke checks used the actual local preview: originalQLDmap searchBrisbane → select → OpennewBrisbane page; SA2025 →2026layer switching, searchO'Donoghue →Open preserving the edition query; correct future-edition no-member/history text; Back; shared Index open/close. Earlier narrow viewport was663px; a later hidden QA tab had1265px client width and matching settled scroll width. Do not claim390px mobile or physical-touch testing occurred for the new renderer.
- Saved screenshots: `content/places/qa/qld-existing-map.png` and `national-federal-map.png`. A final structured browser-review record is outstanding.
- Full earlier national structural run checked859,186assertions,173,360local references,12,557fragments and44gzip round trips, but **FAILED**, as noted above. Its size/counts belong to that earlier snapshot.

## Data access, rights and approval fatigue

Raw public HTML/PDF rosters can contain contact details and retain publisher copyright. `.gitignore` now ignores **all `content/places/raw/`**, and `scripts/prepare-github-upload.py` explicitly excludes it. Public minimal facts/source manifests and licensed map delivery assets remain separate. `content/places/source-retention.json` documents this. The validator checks/hash-verifies available local originals and records an absent local-only original separately in public checkouts; delivered map assets remain mandatory.

The council acquisition script briefly introduced an unverified-TLS fallback for two QLD downloads. It has been removed. Normal bundledPython3.12 and current trusted CA verification still found those certificates expired. The original audit and re-verification failures are retained. **No canonical Queensland ballot/roster facts use those two downloads.** Do not use them for new published facts unless independently verified through an appropriate official source. Do not bypass certificates,403responses, authentication, paywalls or CAPTCHAs to finish the task.

Repeated Allow prompts persisted despite the user's permission-setting change. Network access remained restricted by the execution environment. Narrow approved acquisition-script prefixes reduced neither the user's actual prompt burden nor the need to respect the sandbox reliably enough. Do not tell the user that the setting has fixed it, repeatedly ask to proceed, weaken security controls, or start one-off download commands again. **Most already acquired data and every local integration/build/check can be worked on offline after a resume instruction.** Use the retained manifests to identify what genuinely needs further external access, then consolidate only necessary acquisition with the applicable permission mechanism. The user has not authorised changing security protections.

## Runtime, commands and working tree

Run from the repository root. System `python` is Python3.9.5 with BeautifulSoup4; several legacy tools require Python3.12+. The configured bundled runtime is:

```powershell
$civicPython = 'C:\Users\Aura2020\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
& $civicPython -B tools/build-national-places.py
& $civicPython -B tools/verify-national-places.py --source-hashes
node tools/check-civic-clocks.mjs
node tools/check-civic-geometry.mjs
& $civicPython -B tools/build-human-site-map.py
& $civicPython -B tools/verify-discovery.py
```

After genuine browser/default national validation passes:

```powershell
& $civicPython -B tools/build-national-contracts.py
& $civicPython -B tools/verify-place-contracts.py
```

Read each acquisition script's help/source before using it; **do not run a network-acquiring default unintentionally**. Council has `--offline`; federal has `--build --verify`; the root TAS script without `--acquire` uses its cache but currently fails as documented. A final public-source packaging run has not been performed.

The original tracked tree was clean when this expansion began, but unrelated pre-existing untracked QA files existed. There are now many legitimate new untracked place pages, map assets, canonical records and tools, plus those unrelated QA files. Do not use `git add .`, reset/clean the tree, delete the research cache or archive the checkout. Preserve and inspect intended files explicitly. No new branch/worktree was created by root.

The owned preview server was stopped for this handoff. Restart with `node scripts/serve.mjs` when needed; it previously served `http://127.0.0.1:8768`. Browser QA must use the available computer-use interface, with actual evidence rather than invented device checks. Do not assume an old browser tab/session is still live.

## Resume brief

```text
Resume the unfinished national civic expansion in G:\GithubLocal-PC\p4a-xyz-cinema.
Read docs/agents/national-expansion-handoff-2026-10-17.md and its three level
handoffs first. Preserve the working tree. Complete already acquired offline
integration before requesting further network access. Address the repeated-Allow
problem before any new acquisition; do not weaken security or bypass restrictions.
Finish council/state current rosters, previous event ballots, true ward and current
boundary editions; preserve separate serving/future/historical records and dates.
Create no new Twinkles. Rebuild pages, run genuine data/map/clock/link/browser QA,
bind contracts only to actual passing evidence, finish review/discovery records,
and report remaining source gaps and exact local/publication state honestly.
```
