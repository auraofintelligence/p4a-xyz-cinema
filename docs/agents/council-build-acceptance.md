# Civic place build acceptance

Version 1.0. Created 17 October 2026, Australia/Brisbane. Apply with the [shared core](local-place-pattern.md) and separate council, state or federal guide. The filename retains the council reference; these gates also apply to declared electorate builds.

Record **pass**, **fail**, **not tested**, or **not applicable with a sourced reason** for every applicable row in the [completion report](council-expansion-report-template.md). This unfilled checklist is not evidence of a completed check. A structural script covers only its actual assertions. Complete requires all mandatory gates for the declared scope to pass; fix failures first. A missing source/right/capability requires a named partial/blocked scope. Honest unavailable data can pass; invented data cannot.

## Mandatory gates

| Gate | Required evidence |
| --- | --- |
| Scope/privacy | Target kind, authorisation and existing changes inventoried; no private candidacy, reflection, credentials or attachment leaked |
| Actual institution | Primary dated sources establish jurisdiction, governance/chamber, representation, boundary edition, election administrator and selection/vacancy rules; no Queensland default elsewhere |
| Separate scopes | Council, state and federal routes/powers/data/elections remain distinct; overlap links do not merge them |
| Existing work | Map/data baseline reused or deliberately adapted; profile/atlas coverage distinguished from complete issues/system journeys |
| Parent/direct entry | Parent portal reaches the actual map and destination; direct issue/candidate/area arrivals name place/purpose and offer useful routes |
| One overview map | One primary interactive map; historical maps on Sources & dates; styles/layers share viewport |
| Real next level | All genuine children open reviewed overviews; undivided/at-large/no-child arrangements explicit; no fictional hierarchy |
| Source geometry | Raw source/request/hash/counts/edition/CRS retained; transfer limits verified; all delivery coordinates/holes/multiparts retained; no SVG maps/tracing/guessed shapes |
| Alignment/picking | Raster/drawing/picking share documented projection and returned extent; known mainland/island/water/hole/neighbour fixtures match expected identity |
| Map controls | Drag, buttons, wheel, reset, search/alias, clear/no-results, select/summary/Open and keyboard work; supported touch checked or hardware limit recorded |
| Identity/routes | Search and polygon click select same stable record; direct-link/nested routes work; unbuilt places have no false Open link |
| Quiet colour | Actual coast/islands visible through transparent administrative water; quiet default; optional detail where available; legend disclaims arbitrary political colour meaning |
| Map alternatives/rights | Text directory/static source/parent links work; online failure/local fallback reviewed; attribution/edition/terms visible and retained |
| Responsive layout | Phone, narrow tablet/split panel and desktop measured; no overlap, clipping or horizontal page scroll, including long names |
| Human journey | Problems, systems, people, evidence, contribution and outcomes connect; no forced restart or generic dead end |
| Twinkle meaning | Every new seed reviewed for ordinary scene, actual gripe, matching title, one spoken breath, machinery target and quiet-care variant; seed visible before serious detail |
| Twinkle status | Draft versus quote/verified complaint/endorsement explicit; no fictional resident quotations or popularity/ledger claims |
| Deeper substance | Evidence, perspectives, authority, alternatives, dependencies and unknowns present; general systems not falsely deployed locally |
| Braided economy | Proposals/outcomes distinguish cost, freely given contribution and change; proposed/observed and unknown/zero distinct; no double-counted hours/fixed dollar equivalent |
| Statistics | Dataset, unit, denominator, period, compatible geography/code and source beside numbers; no ward/seat values invented from council totals |
| Overlap/results | Edition/method/denominator clear; primary/2CP/2PP and single/multi-member results distinguished; no invented percentages or council-wide inference |
| People/votes/why | Roles/candidate stages evidenced equally; primary motion/stage/vote reachable; absence/recusal/unrecorded distinct; stated reason sourced, interpretation labelled, unknown admitted |
| Election timing | Shared reviewed events/timezone/date basis; no speculative countdown or invented early/postal window; before/on/after and daylight-saving cases pass where applicable |
| Cultural context | Country/statutory/electoral layers distinct; public self-description/permissions respected; no consent/identity inferred from polygons |
| Static/private behaviour | Readable no-JS fallback; no fictional backend; private form disabled without safe handler; deliberate local export/no URL leakage; storage/external requests honest |
| Dates/source trail | Observation/publication/retrieval/check/effective/change dates separate; rebuilding does not refresh research; source-specific rights retained |
| Automated gates | A real reviewed `content/**/*-pattern-contract.json` is registered using `<place>-pattern-contract.json` naming; discovery plus place-specific provenance/geometry/clock/link/syntax checks actually run; failures repaired or identified as blocking |
| Deterministic build | Repeated scoped generation identical; existing unrelated content/routes preserved |
| GitHub preparation | Scoped diff, relative/case-sensitive routes, required source/generated files, rights/privacy/file-size review complete; unwanted local/private files excluded |
| Handoff | Completed report, actual evidence/screenshots, dated history, unresolved gates and refresh triggers; publication state exact |

## Minimum browser scenarios

Use delivered pages, not a separate mockup. Record viewport sizes and physical versus synthetic touch/DPR.

1. Follow the full parent map -> selected area -> Open -> real next level if applicable -> local issue -> evidence/system/action/outcome path; return through parent routes. Test direct issue, person and child-area arrivals.
2. Compare polygon selection and official-name/alias search. Clear/search no-results. Exercise drag, zoom buttons/wheel/reset, keyboard and direct-link state. Test independently expected mainland, island and neighbouring picks plus holes/water where applicable.
3. Change optional road/style/layer and pan/zoom; selection remains aligned. Simulate online-detail failure and confirm usable fallback/text routes.
4. Check approximately 390 px, 680 px and desktop, plus actual embedded/split-panel width. Measure overflow/overlap and inspect screenshots; long names and all controls remain readable.
5. Open every actual child destination and each distinct record type. Review every new Twinkle's spoken meaning, not just word count. Verify serious context and braided accounts.
6. Exercise delivered clocks with fixed before/on/after times, early/postal boundaries and daylight saving where relevant. Unsupported dates produce no timer; synthetic timetable dates remain test-only.
7. Check static/no-JS directory, parent/source links and safe private-form guard. Use synthetic text for local export; verify no submission or URL leakage.

## Automatic acceptance failures

- Buttons/pictures passed off as the promised selectable map; duplicate competing overview maps; missing next-level journeys.
- SVG approximation, traced geography, wrong projection, missed islands/holes, opaque marine land or misleading colour.
- Distracting default roads, overlapping/shrinking button labels or sideways page scroll.
- Policy briefings labelled Twinkles, missing spoken seeds, personal attacks, invented quotations or implied endorsement.
- Unverified counts/representatives, fabricated missing statistics, council/state/federal data conflation.
- Universal ten divisions, direct mayor, Queensland dates/laws, upper-house single-member assumptions or House-style Senate vacancy logic.
- Structural PASS reported as source/browser/editorial completion; local files reported as deployed.

## Reference commands

```text
python tools/build-redland.py
python tools/verify-redland.py
node tools/check-redland-clock.mjs
python tools/verify-council-pattern.py --manifest content/local/council-pattern-contract.json
python tools/verify-place-contracts.py
```

For another place, pass its own reviewed `<place>-pattern-contract.json` under `content/` and data-aware validators. The discovery command finds all registered manifests automatically. The read-only `.github/workflows/civic-place-checks.yml` runs on push, pull request and manual dispatch. CI success does not establish fresh source review, new-jurisdiction legal correctness or source/browser/editorial acceptance. See [GitHub upload preparation](../github-upload.md).
