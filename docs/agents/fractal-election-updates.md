# Fractal election, member and navigation updates

Version 1.2. Created and updated 17 October 2026, Australia/Brisbane. This is the maintenance guide for council, state/territory and federal election pages, including an individual by-election. The national adapter and canonical registries below now exist. Their recorded coverage and verification limits remain separate from a claim that every individual fact or local journey is complete.

Read [AGENTS.md](../../AGENTS.md), the [shared place rules](local-place-pattern.md), the relevant [council](council-journey-rules.md), [state](state-electorate-journey-rules.md) or [federal](federal-electorate-journey-rules.md) guide, and the target's existing source and history. Use the [watchlist](../../content/refresh-watchlist.md) to find triggers and the [existing coverage inventory](existing-place-coverage.md) to find working implementations. This guide replaces the watchlist's former state-only/manual-mirroring recipe for scoped election maintenance.

## 1. Fractal means the same small process at every scale

Repeat **identify -> verify -> edit source -> update dependants -> check -> record** at the smallest affected unit. An update to one ward election should be possible without researching every council or refreshing every jurisdiction's dates.

```text
Australia
  State or territory context
    Local government institution -> real ward/division, if any -> event
    State/territory parliament -> actual chamber/electoral area -> event
    Commonwealth representation -> House division or Senate area -> event
      Event -> contestants, timetable, results and source records
      Current office -> dated role-holder records and public profiles
```

This is a navigation and maintenance pattern, not an assertion that these institutions form one legal or geographic hierarchy. Federal and state areas can cross councils. Upper houses, multi-member areas, undivided councils, unincorporated areas and exceptional bodies need their actual arrangements. Country remains a distinct relationship.

Root instructions hold shared rules. A jurisdiction or place may add a short local `AGENTS.md` when it has real adapter-specific instructions: stable place identity, parent guide, canonical files, source URLs, output routes, build/check commands and exceptions. Inherit common rules; link to this guide rather than copying its whole text into every place. Never create a local instruction claiming an unbuilt adapter works.

## 2. Start with a small update brief

Record these fields in the target's maintained report or refresh-log entry before editing; expand them when a new place is first built:

| Field | What the next agent needs |
| --- | --- |
| Scope | Official place, jurisdiction, institution/chamber, area kind and stable source ID |
| Trigger | Vacancy, announced poll, timetable change, nominations, count, declaration, office change, redistribution or broken link |
| Event identity | Stable official event ID; otherwise a documented local ID linked to its official event page |
| Boundary basis | Edition/effective date used for this event; separate current and historical geography |
| Canonical inputs | Actual place, event, role-holder, contestant and source files; exact record IDs |
| Dependants | Area page, people/election view, map profile, parent summaries, directories and clocks using the changed records |
| Adapter | Existing generator, its actual output footprint, scoped arguments and applicable validators |
| Evidence | Exact official URLs, what each supports, publication/effective dates and actual checked dates |
| Delivery | Changed/unchanged/needs follow-up; verification results and exact local/publication state |

These are handover requirements, not a new executable schema. Reuse existing canonical files and validators. A new adapter must document these relationships so future agents can follow them directly rather than searching the entire site. Search record IDs, event IDs, former names/URLs and distinctive copy with `rg` to find remaining dependants.

## 3. Keep four kinds of record separate

| Record | Maintenance rule |
| --- | --- |
| Current office | Person, institution, represented area/position, start/end/status, dated official roster and public profile links. A vacancy is explicit; the previous member becomes historical. A poll result and taking office can be different events. |
| Historical contest | Everyone who contested a specific event, with ballot name, then-affiliation, result/status, source and boundary edition. Preserve previous general elections and subsequent by-elections separately. |
| Future candidacy | Announced, preselected, accepted nomination, withdrawn and other evidenced stages. Office-holding or a previous contest does not establish recontesting. |
| Election event | Institution/area, event kind, official ID/page, date basis, timetable, timezone, current stage, results and source history. A new by-election does not overwrite the ordinary cycle. |

Link current elected members to their official parliamentary/council profiles and verified public personal or campaign websites where available. Record which type of link it is and when it was checked. For previous contestants retain available public profile/site links and official candidate/result records; an unavailable personal website does not justify omitting the contestant. Do not guess URLs, merge people on name alone or substitute a later party affiliation for their ballot label.

For each previous relevant election, reconcile the contestant roster to the official ballot/declaration, including independents and unsuccessful candidates. Distinguish nominations, withdrawals and actual contestants. Preserve an uncontested event's actual outcome without inventing votes. Record missing coverage explicitly. Candidate order and preference/result tables must retain their official meaning; do not label every result 2PP or every multi-member contest a single-winner race.

## 4. Verify the actual event and replacement process

Use the target's electoral authority for notices, nominations, timetable, ballot and results; the relevant parliament/council for current membership and official profiles; original applicable legislation and official notices for the replacement process. Secondary reporting can identify a lead or discrepancy, but the published status needs supporting primary evidence. Record source disagreements and their effects.

Check whether the trigger creates a poll, appointment, countback, casual-vacancy replacement or another process. Source this for the actual office and jurisdiction. A resignation, absence, leave decision, change of party or redistribution does not itself establish a by-election date. Mayoral, councillor, lower-house and upper-house events may need different adapters.

Follow only evidenced transitions:

```text
Reported change -> verified vacancy/status -> applicable replacement process
  Poll: official notice -> nominations/ballot -> voting -> count -> declared result
  Other process: official process -> confirmed replacement -> taking office
```

An officially verified vacancy, poll-held status or count in progress can be updated before a winner is declared. Leave the winner unknown and label provisional results accurately. Passing polling day never automatically proves a declared result or current office. Archive superseded records and source snapshots with their actual dates.

## Boundary changes and redistributions

Treat a boundary change as a versioned geography update with an explicit impact list. A draft, final determination, legal commencement, first election on new boundaries and the boundaries of currently serving members can be different stages. Keep these stages sourced and labelled; do not switch the current-representation map solely because a newer download exists.

1. **Verify the change.** Read the original determination/notice and geometry catalogue. Record affected institutions/areas, proposal/final status, publication and effective dates, first applicable election, source codes and source CRS/datum. Identify abolished, renamed, created, split and merged areas; never infer a one-to-one successor from a matching name.
2. **Retain both editions.** Archive original geometry bytes, exact requests/pagination, licence, hashes, feature/ring/coordinate counts and provenance. Add the new edition separately. Preserve every ring, island and coordinate; property adaptation and documented display projection do not authorise rounding or simplification. Reuse the lossless delivery approach and prove decoded coordinates equal source coordinates.
3. **Update the place registry and routes.** Use stable identities plus an edition key. Register real successor/predecessor relationships only with evidence. Change map/search feature joins, aliases, labels, Open links, genuine parent/child relationships, layer filters and counts. Keep old public routes and direct-link identifiers usable through a historical page or explicit successor choices. A split can require several choices rather than an automatic redirect.
4. **Review cross-level links.** Recheck council/ward, district/region and House/Senate associations that rely on this geography. Recalculate any sourced overlap with the documented editions, denominator, land/water treatment and method. Mark unrecomputed intersections unavailable; a visual intersection is not evidence of residents or electors transferring.
5. **Protect people and election history.** Serving representatives stay attached to the applicable current-office geography until official records establish a change. New-boundary candidate announcements/accepted nominations belong to their actual event/edition. Preserve prior contestant lists and result tables on their historical boundaries. Do not attach an old winner, party, vote or swing to a new area without an official supported basis.
6. **Review statistical compatibility.** Rejoin geography-coded data only where the edition matches. Keep Census observation periods and ABS/statistical codes separate from electoral IDs. Use a published correspondence or documented supported method where appropriate; otherwise show unavailable on the new geography. Never transfer values by name, land-area ratio, equal ward shares or averaged medians.
7. **Update delivery and geographic context.** Refresh layer manifests, hashes, compression/script deliveries, asset references/cache versions and actual source attribution. Recheck raster coverage, returned extent, CRS/datum/display transformation and island/coast alignment. A boundary change does not automatically require changing a still-valid geographic raster or election date. Invalidate obsolete cached layer data and saved selection IDs safely.
8. **Rebuild affected journeys and discovery.** Regenerate detail/map/directory pages and dependent summaries using the actual adapter. Follow section 7 for shared navigation, parent links, human/XML sitemaps, `llms.txt`, route inventory and supported page-update dates. Preserve unrelated jurisdictions and historical routes.
9. **Verify the new edition.** Reconcile official coverage and stable joins; check duplicates, omissions, multipart components and holes; prove lossless delivery; repeat independent mainland/island/water/neighbour picks, search/selection/Open/deep links and responsive/browser checks. Confirm current versus upcoming layers, historical election results and statistics display the correct edition. Run affected place contracts and jurisdiction validators before updating review fingerprints.
10. **Leave a scoped handover.** Record old/new source editions and hashes, official determination/effective-event sources, changed places/routes/dependencies, actual checks, unresolved correspondence/history gaps and the next review trigger. Update the adapter's impact list so the next boundary change can follow the same process at one place or whole-layer scale.

New national adapters must expose the edition attached to each geometry, current role, contest, statistic and overlap. Keep proposed/upcoming editions available as distinctly labelled comparisons where implemented, with honest limits; never silently overwrite the layer used to explain an earlier election.

## 5. One event record supplies every countdown

- Read the same canonical event/date/status in the area page, map profile, parent card and any election directory. Avoid independent hardcoded timer dates.
- Keep upcoming ordinary elections, extraordinary/by-elections and historical events separate. State the date basis: officially announced, supported rule-derived schedule, estimate or unknown. Only supported dates get an exact countdown; estimates and unknown dates get descriptive status. Distinguish a rule-derived schedule from an announced timetable.
- Retain the previous polling date for days-since display and event history. Use the applicable local calendar and IANA timezone. A national view must label timezone differences rather than assume Brisbane time throughout Australia.
- Polling day, opening of polls, early voting and postal deadlines are distinct milestones with separate sources. Date-only countdowns run to the start of the local calendar date and must say so; do not imply polls open at midnight. Give a precise deadline a sourced local time/offset.
- Test fixed times before, on and after each milestone, daylight-saving transitions where relevant, null dates, postponed/cancelled events and multiple simultaneous events. No negative countdown, automatic winner, guessed next-cycle date or test-only timetable in published data.

## 6. Apply the smallest complete change

1. Inspect the working tree and preserve unrelated work. Establish the target identity, event and existing dependency list.
2. Read the target's canonical source/history and original source URLs. Verify only the requested event and necessary dependencies. If no change is found, append a scoped no-change entry to [refresh-log.md](../../content/refresh-log.md) and stop. A no-change check does not require a date bump or rebuild.
3. Archive the superseded event/role facts using the existing history pattern. Edit canonical records first: event status/timetable, current office, contestants/results and profile links as actually supported. Preserve unknowns, observation periods and historical boundaries.
4. Update parent seat summaries or leadership only if supported and affected. Reconcile members plus vacancies to the sourced chamber/council structure. A councillor or House change does not automatically alter a state government summary.
5. Run the actual scoped generator(s) listed below or in the target adapter. Where no safe generator exists, make a narrow source/output correction and verify exact parity. Do not introduce broad replacements across unrelated places. Inspect shared output diffs even when a command accepts a place argument.
6. Follow the navigation/discovery procedure below when names, routes, directories or public pages change. A results-only update still needs link and direct-arrival checks on its affected pages.
7. Run affected data, clock, link and browser checks. For a map/boundary change also run geometry, raster/picking and performance checks. A person/status-only change should preserve existing geometry byte-for-byte.
8. Record changed files/routes, primary sources and check dates, actual verification, unresolved gaps and publication state. Update the relevant maintained page/rule review records only for changed implementation. Do not copy old passing evidence or claim unrun checks passed.

Current national expansion scope: **create no new Twinkles**. Leave local Twinkle authorship to grassroots implementation, preserve existing seeds and do not invent local grievances during an election refresh. Existing evidence, systems, participation and outcomes links should survive.

### Existing adapters and their footprint

Run from the repository root with its installed Python, Node and PowerShell 7. Inspect the target's current instructions before executing. These are existing tools, not commands for unbuilt jurisdictions:

| Target | Existing build/check entry points | Scope caution |
| --- | --- | --- |
| National council, state and federal place pages | `python -B tools/build-national-places.py --place <stable-place-id>`; `python -B tools/verify-national-places.py --source-hashes`; `node tools/check-civic-clocks.mjs`; `node tools/check-civic-geometry.mjs` | Read [the canonical-data agent file](../../content/places/AGENTS.md). Inputs are `content/places/councils.json`, `state.json` and `federal.json`. A place update rebuilds its same-layer dependent pages and shared directories/indexes. `--jurisdiction` and `--scope` are broader filters; without filters the complete national page set is rebuilt. Shared geometry delivery and route indexes are always complete. |
| State/territory summary | `pwsh -NoProfile -File tools/build-state-sites.ps1 -StateSlug <actual-slug> -SkipHistory` | Also writes shared `assets/state-data.js` and `pages/states.html`. Review their diffs and unrelated state content/dates; a scoped argument does not mean every output is place-local. |
| Victoria map/people | `python tools/build-vic-map.py`; `python tools/verify-vic-map.py`; `python tools/verify-vic-numbers.py`; `python tools/verify-vic-councils.py` | Read [Victoria implementation](../../content/electorates/vic-implementation.md); electorate, representative, council and candidate files carry distinct dates. Run checks affected by the changed data. |
| Victoria candidate directory | `python tools/build-vic-election.py` | Canonical candidate data is `content/elections/vic-2026.json`. This is a specific historical/event source, not a permanent filename for every future election. Rebuild map delivery too when it consumes changed candidate records. |
| Redland journey | `python tools/build-redland.py`; `python tools/verify-redland.py`; `node tools/check-redland-clock.mjs` | Timing is `content/local/redland-election.json`. The build also restores marked council/state entry links and shared navigation; inspect all changed files. |
| Registered place contract | `python tools/verify-council-pattern.py --manifest <actual-reviewed-manifest>`; `python tools/verify-place-contracts.py` | Use the place's real contract and source fingerprints. Source changes require affected rechecks before updating acceptance evidence. |

The national adapter writes `content/places/route-registry.json`, `geometry-delivery.json`, `assets/qld-place-routes.js`, new place/directory pages and marked entry links. `assets/civic-places.js` and `.css` are the shared map, search, navigation and countdown presentation. Source acquisition scripts are deliberately separate: use their actual arguments and the legally accessible official source only when a source refresh is needed. Do not redownload every jurisdiction for a single by-election.

Keep each canonical `id`, `parentId`, primary `layerId`/`featureId` and alternate-edition `mapRefs` consistent. Ward pages are real subdivisions, not equal shares of their council. House and Senate are separate institutions; statewide upper-house and Senate maps use explicitly labelled jurisdiction context rather than invented electoral subdivisions. The route registry is generated and must not be hand-edited.

Use `python -B tools/build-national-contracts.py` only after fresh default national validation and a genuine browser review record pass. It binds each full canonical place record and actual shared implementation/evidence hashes. These contracts explicitly cover structural routes and canonical identity; they do not certify missing biographies, contestants or untested browser/source facts. Run `python tools/verify-place-contracts.py` afterwards. Legacy Redlands generators require Python 3.12 or newer; use the configured bundled runtime if the system `python` is older.

The default report binds canonical inputs, delivered pages/assets, original geometry and available raw sources before and after validation. Save real browser fixtures at `content/places/qa/browser-review.json` with tested HTML paths, fixture paths and their hashes; never borrow a passing review from another place. Changed bytes or a changed required artifact set require renewed checks before contract binding. CI repeats `python -B tools/verify-national-places.py --source-hashes --no-write` without rewriting saved reports. Preserve the scoped `.gitattributes` rules so Windows/Linux checkouts retain exact reviewed evidence bytes.

Future adapters must document their equivalent commands, canonical files, stable joins, generated routes and shared outputs here or in a linked local guide when actually implemented. Missing adapters remain explicit work, not guessed commands.

## 7. Maintain sitemap, navigation and links

### Decide what changed

| Change | Required navigation action |
| --- | --- |
| Same route, new member/result/date | Update generated detail/profile and parent summaries that use the record. Check person/source links and existing deep links. No new sitemap route is needed. |
| New electorate, election/history page or directory | Build the page first; add real parent, breadcrumb, text-directory and map Open destinations; then register it in discovery. |
| Rename or redistribution | Retain stable identity where applicable and explicit edition/history. Preserve old inbound routes/anchors with a compatible page/link or supported redirect strategy; do not silently send an old electorate to a different area. |
| Removed/replaced public site or profile | Find incoming uses, verify the replacement, record the check and keep historical identity clear. Label unavailable links honestly. |

### Update canonical navigation, then regenerate

1. Update each affected page's generator/template and canonical content, including relative asset paths at its real nesting depth. Keep an obvious parent route and useful direct arrivals. Map selection and text search must open the same stable record.
2. Review `assets/site-nav.js`, especially `SECTIONS`, for shared search/index, breadcrumbs and footer destinations. Add appropriate directories/entry pages and preserve place-level text navigation. If a marked section is generator-owned, edit that generator too so the link survives regeneration. Do not force thousands of individual records into the top-level menu.
3. Update [the page/rule review register](../../content/history/civic-page-review-register-2026-10-17.json) or its documented successor with reviewed route dates and change reasons. Preserve original work-started and first-verified dates. Only assert a sitemap last-modified date supported by an implementation review; do not use today's build date for unknown content dates.
4. Inspect `tools/build-human-site-map.py`, `tools/build-discovery.py` and `tools/verify-discovery.py` before new route families or navigation groups. They currently discover root `index.html` plus HTML under `pages/` and `states/`; new public directories outside those trees need explicit support in both builders and the verifier. The human builder and discovery builder maintain separate group definitions: update both sets of grouping/labels, the discovery inventory rules and assistant-directory grouping as applicable. Its navigation date/wording is currently explicit; change it only for an actual navigation review.
5. Run `python tools/build-human-site-map.py`. It regenerates the readable `pages/site-map.html`, its canonical `content/rooms/site-map.html`, `content/site-page-inventory.json`, `sitemap.xml`, `robots.txt` and `llms.txt`. The builder invokes the discovery builder; inspect the complete output diff. Preserve crawler policy, licence wording, third-party rights and unrelated groups.
6. Run `python tools/verify-discovery.py`. Also check actual relative links/assets, case-sensitive filenames and fragment IDs in delivered pages; discovery coverage alone does not check every link or current political fact. If shared JavaScript changed, run `node --check assets/site-nav.js` and other affected scripts.
7. Follow States -> target institution/map -> select/search -> Open -> people/event -> sources -> parent. Test direct person/event/area links, URL selection and Back, no-JavaScript text navigation, keyboard access, phone/tablet/desktop layout and external profile links. Same-site links keep their intended behaviour; external web links follow the existing [link policy](../../assets/external-links.js).

For new place journeys use the [acceptance gates](council-build-acceptance.md), [report template](council-expansion-report-template.md) and a genuinely reviewed place contract. For a docs-only update with no public HTML, route or navigation change, validate the documentation links and rule register; a site-wide rebuild is unnecessary.

### Retained sources, browser extraction and large layers

Complete cached integration before new acquisition. Register the genuinely missing official requests, then use a bounded source batch with the applicable permission mechanism. Existing user authorization persists; do not ask again for each ordinary website read. Network settings may still restrict a command, so record its actual outcome rather than promising that prompts are fixed. Never change security protections or bypass certificate warnings, access denials, authentication or CAPTCHAs.

An official page may work through ordinary browser navigation when a direct downloader fails. A minimal factual extraction from that rendered public page is a distinct source artifact: retain its URL, checked date, method, count and hash; distinguish it from downloaded original HTML. Extract only the public names, roles, election values and links needed for the task. Keep full research originals and contact directories under the excluded `content/places/raw/` cache. Public manifests and normalized facts remain separate.

Gzip-only geometry is a complete lossless delivery when decoded bytes, coordinates, parts and joins are verified. Do not generate a plain duplicate that exceeds the public-source size limit. Keep native geometry/projection evidence and exact compressed assets; document browser support and text-directory fallback. Run `node tools/check-civic-delivery.mjs` after loader changes alongside the geometry and clock checks.

The original Redlands page register may link separately scoped national registers through `additionalPageRegisters`. Discovery reads those explicit entries, preserves their implementation dates and rejects duplicate routes. Add dates only after the declared build review; a shared browser fixture does not certify every place's sources or complete local journey. Do not fill unknown source dates from the build clock.

## 8. Finish with a small, truthful handover

Append every check to the shared refresh log; append to the relevant place history when facts or implementation changed. A no-change check touches only the shared refresh log. Include scope and event ID; changed/unchanged/needs-follow-up; evidence URLs and dates; affected canonical files and generated routes; actual checks; unresolved questions and next trigger; exact local/committed/pushed/deployed status. A source access failure is needs-follow-up, not a no-change check. Do not advance unrelated research dates or overwrite earlier log entries.

Routine refreshes do not create duplicate place-contract manifests. Update the existing reviewed contract when its inputs change and retain the previous evidence/history. A structural pass is separate from fresh source review and delivered-page/browser checks. Use existing session authorisation for commits/publication; this guide alone authorises neither and schedules no monitoring.

### Short prompt for a future individual update

```text
Refresh only <official place/institution/chamber> for <event or reported change>.
Follow AGENTS.md and docs/agents/fractal-election-updates.md, then the target guide.
Find the stable area/event IDs, real canonical inputs and affected output routes.
Verify the official process, timetable, current officeholders/public profiles and
contestants/results for this event; preserve the previous general election and
any subsequent by-elections as separate histories. Update shared countdowns and
only affected parent summaries. Maintain real links, navigation and discovery.
Run the actual scoped adapter/checks, review all diffs and record sources/gaps.
Preserve unrelated dates/geometry and existing Twinkles; create no new Twinkles.
Report the exact delivery/publication state and next verification trigger.
```
