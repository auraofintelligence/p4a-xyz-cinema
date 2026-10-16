# Civic place expansion report template

Version 1.0. Created 17 October 2026, Australia/Brisbane. Use with the [shared core](local-place-pattern.md), relevant separate guide and [acceptance gates](council-build-acceptance.md). The filename retains council-reference compatibility. Copy into the target's maintained report, replace placeholders and remove prompts. Never copy example counts, dates or source claims as new research.

## Identity and declared scope

| Field | Reviewed value |
| --- | --- |
| Official place/institution and kind | `<council/ward/state district/state region/federal House division/Senate area/other>` |
| Stable ID, parent/context and aliases | `<values; distinguish institutional relationships>` |
| Source/ABS codes and editions | `<separate identities; no assumed join>` |
| Public route / local preview | `<relative route; preview URL>` |
| Pattern / adapter version | `<version/revision>` |
| Registered contract manifest | `<reviewed content/.../<place>-pattern-contract.json; never a placeholder>` |
| Requested scope and authorisation | `<exact boundary; build/refresh/GitHub preparation/etc.>` |
| Existing implementation reused / missing depth | `<atlas/profile/data versus complete civic journey>` |
| Started / implementation updated / timezone | `<ISO dates; target timezone>` |
| Page and rule review register | `<per-route first verified build/update dates, change notes, rule versions and review triggers; distinguish new pages from modified entry pages>` |
| Research scope / actual checked dates | `<what was actually reviewed>` |
| Delivery state | `<complete/partial/blocked; affected scope and reason>` |
| Publication state | `<prepared/staged/committed/pushed/deployed; actual revision if any>` |

## Jurisdiction and evidence

For each row record finding, exact primary source and checked date. Mark unknown with its effect, never fill from Redlands assumptions.

| Item | Finding | Primary source / checked |
| --- | --- | --- |
| Official identity/governance/chamber | `<actual arrangement>` | `<URL; date>` |
| Child areas or no-child arrangement | `<names/counts/member numbers/edition/effective date>` | `<URL; date>` |
| Selection of mayor/leader/representatives | `<direct/indirect/single/multi-member as applicable>` | `<URL; date>` |
| Election administrator/system/terms | `<finding>` | `<URL; date>` |
| Ordinary event date/status/timezone | `<announced/rule-derived/unknown>` | `<URL; date>` |
| Vacancy/replacement/special event | `<separate stages; no inferred poll>` | `<law/minutes/notice; date>` |
| Nomination/withdrawal sources | `<applicable process; no personal candidacy inference>` | `<URL; date>` |
| Cross-level overlaps | `<edition/method/denominator or qualitative only>` | `<URL; date>` |
| Country/cultural context | `<public self-description; cultural/statutory distinction; permission basis/gaps>` | `<source; date>` |

## Map/source inventory

Repeat per layer or link a detailed source manifest containing all fields:

- Publisher, layer identity/purpose, exact original page/service/query, filters/pagination and completeness check.
- Boundary edition/effective date; native/delivery/display CRS, axis/datum transformation.
- Raw path, SHA-256/bytes, actual feature/ring/coordinate counts and unique identities.
- Delivery path, lossless coordinate comparison method and result.
- Geographic raster/style/optional roads, unchanged asset/hash/size and **actual returned extent**.
- Source-specific licence/terms/attribution and disclosed conversions.
- Separate publisher-update, observation, retrieval and verification dates and meanings.
- Independently expected mainland/island/water/hole/neighbour picking fixtures.
- Rights/alignment/freshness gaps and their effect on scope.

## Content and implementation inventory

- Canonical place, connections, child areas, elections, people and source records: `<paths>`.
- Adapter/generator/component changes: `<paths; hardcoded dependencies removed/isolated>`.
- Generated routes and actual child coverage: `<list/manifest/count; honest unbuilt status>`.
- Parent/shared-navigation integration, one overview map and historical-map location: `<routes>`.
- Reviewed indicators/datasets/periods and unavailable child statistics: `<coverage>`.
- Local issue/Twinkle/system records: `<actual counts; spoken-seed review/status>`.
- People/candidates/votes/reasons: `<public sources/status; explicit missing histories>`.
- Substantive proposals/outcomes with three braided accounts: `<record IDs; unknowns>`.
- External systems/lyric meanings and present implementation stage: `<context; no implied deployment>`.
- Static/no-JS/private export/external requests: `<actual behaviour and limits>`.
- Unrelated files/routes intentionally preserved: `<scope>`.

## Verification results

Attach the completed acceptance gates. For each check record exact command/method, pass/fail/not tested/N/A, evidence path and limitation. One PASS must not obscure untested requirements.

| Check | Command or method | Actual result / evidence |
| --- | --- | --- |
| Primary arrangement/facts/rights review | `<sources; dates>` | `<result>` |
| Manifest structure | `python tools/verify-council-pattern.py --manifest <target-manifest>` | `<result; actual coverage>` |
| All registered place contracts | `python tools/verify-place-contracts.py` | `<result; automatically discovered manifest paths>` |
| Source geometry/delivery/raster/picking | `<data-aware validation>` | `<counts/hashes/fixtures>` |
| Routes/anchors/case-sensitive links | `<method>` | `<report>` |
| Clock fixed before/on/after cases | `<command; times/timezones>` | `<real versus synthetic dates>` |
| Relevant syntax/source assertions | `<commands>` | `<report>` |
| Repeat deterministic generation | `<two builds; scoped comparison>` | `<hash/diff evidence>` |
| Parent/direct/child CYOA journeys | `<browser/method>` | `<screenshots/notes>` |
| Map controls/search/select/style/fallback | `<actual interactions>` | `<results>` |
| Keyboard/no-JS/static privacy/export | `<synthetic input only>` | `<results; no URL leakage>` |
| Phone/tablet/desktop overlap/overflow | `<viewport sizes; measurements>` | `<results/screenshots>` |
| Physical touch versus synthetic DPR | `<actual environment>` | `<hardware gap stated>` |
| All new Twinkle meanings | `<editorial read plus mechanical guard>` | `<IDs/care exceptions>` |
| Braided accounts/system stages | `<record review>` | `<results>` |
| GitHub diff/rights/privacy/file sizes | `<inventory/diff review>` | `<prepared files/exclusions>` |

## Unresolved gates

| Exact gap | Affected route/public label | Required source/action | Owner/trigger | Delivery effect |
| --- | --- | --- | --- | --- |
| `<gap>` | `<unavailable/partial>` | `<concrete requirement>` | `<owner/trigger>` | `<partial/blocking/non-blocking>` |

Complete means all mandatory gates for the declared scope pass. Partial means useful reviewed work with named unmet requirements. Blocked means the scope cannot progress until a named source, right, capability or decision changes. Stopping work or passing a structural script does not mean complete.

## Refresh, handoff and GitHub

- Human purpose/chosen thread, current stage and relevant record IDs: `<plain words; no inferred political profile>`.
- Source versions, latest meaningful changes, differing interpretations and uncertainty: `<references>`.
- Existing authority and its boundaries: `<what is permitted; outside actions not authorised>`.
- Useful next choices and next maintainer's first checks: `<a few specific actions>`.
- Refresh triggers/original sources: `<boundary/election/representation/ABS/budget/terms/etc.>`.
- Append-only history/refresh entries: `<paths/dates; include no-change checks>`.
- GitHub-ready source/generated files, excluded private/local material, required build commands and third-party terms: `<inventory>`.
- Exact prepared/staged/committed/pushed/deployed state, local review link and verified live link only if deployed: `<status>`.
- GitHub preparation followed: `<review against [GitHub upload preparation](../github-upload.md)>`. Record the read-only civic workflow revision/result if run, separately from fresh source, browser and editorial checks.

An optional machine-readable summary may accompany this report. Use the actual manifest/validator keys rather than inventing another configuration system. Include pattern/place identity, dates/timezone, declared scope, source manifests, actual verification results, unresolved gates, output routes, history and publication state.
