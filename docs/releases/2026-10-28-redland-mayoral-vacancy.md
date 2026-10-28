# Redland mayoral vacancy and timetable watch

Scope checked 28 October 2026, Australia/Brisbane: the existing Redlands overview, People & elections and Sources & dates. This update is isolated from the prepared directory cleanup and the original G: checkout. No boundary, statistical, historical-contestant or site-wide roster refresh is claimed.

Council's [28 October announcement](https://www.redlandscoasttoday.com.au/2026/10/council-confirms-mayoral-vacancy-following-resignation/) confirms the vacancy following Jos Mitchell's resignation, the required by-election and Julie Talty continuing as Acting Mayor. The [ECQ event listing](https://www.ecq.qld.gov.au/elections/election-events) did not list a Redland timetable at this check. The [Local Government Act 2009, ss 161, 164–165](https://www.legislation.qld.gov.au/view/whole/html/current/act-2009-017#sec.164) and [Local Government Electoral Act 2011, ss 24–25, 27](https://www.legislation.qld.gov.au/view/whole/html/inforce/2026-09-03/act-2011-027#sec.25) explain the replacement and notice/nomination process. [ECQ candidate guidance](https://www.ecq.qld.gov.au/election-participants/local-election-participants/candidates) is linked without implying any person's candidacy. No estimated polling day is published.

## Daily update handoff

- Canonical public page: <https://p4a.xyz/states/qld/councils/redland/index.html#redland-mayoral-update>.
- Companion page: <https://p4a.xyz/states/qld/councils/redland/candidates/index.html#redland-mayoral-update>.
- Canonical data: `content/local/redland-election.json`, `byElection` record `redland-mayoral-vacancy-2026-10-28`.
- Poll: `byElection.date`, `countdownTarget`, `timingStatus`, `source`, `dateBasis`, `checked`; optional `pollEndsAt` only with a sourced close time.
- Nominations: the same fields under `byElection.nominationDeadline`.
- Renderer: `tools/redland_election.py`; browser clock: `assets/redland-election-clock.mjs`. The existing full Redlands generator imports the renderer too.

Check the event-specific ECQ notice before changing a milestone. Use `date` as `YYYY-MM-DD` and the exact confirmed time as `YYYY-MM-DDTHH:MM:SS+10:00`; record the original notice URL and what the time means. Never activate from a date alone, a media estimate or the statutory two-month interval. Until both date and time are supported, keep the milestone's `timingStatus` as `awaiting-confirmation` and both date fields null. The public status is exactly “Awaiting confirmation to begin”. Each milestone activates independently with `timingStatus: confirmed`. Cancelled/completed events remain explicit. The clock stops at deadlines, shows a nomination-closed or polling-status message, and never infers a winner.

When a checked official source changes, preserve the prior canonical snapshot under `content/local/history/` with its actual date. Update the affected source entries, `byElection.checked`, overall `checked`/`changed` and the three affected page-review entries. Do not advance other research dates merely because a daily check ran. If nothing changes, record the scoped check without rebuilding or publishing. Do not contact officials or submit forms.

Build only the existing sections with Python 3.12+:

```text
python -B tools/build-redland-election.py
python -B tools/verify-redland-election.py
node --test tests/redland-election.test.mjs
node tools/check-redland-clock.mjs
python -B tools/verify-redland.py
```

Check local links, explicit Brisbane offsets, before/at/after deadlines and affected phone/desktop rendering. The Node fixture uses synthetic dates; they are not an event announcement. If a confirmed milestone changes the legacy `/byElection/date` pin, update that reviewed pin in `content/local/council-pattern-contract.json` deliberately after checks. Maintain actual page dates in the review register and rebuild discovery dates with `python tools/build-discovery.py`. The existing national evidence includes the Redlands page and its assets: refresh its affected checks and evidence/contract bindings before committing; do not copy another review or claim a structural run proves current sources or browser layout.

## Verification and publication

Implementation, automated tests and source reads are separate from rendered-browser acceptance and deployment. Actual results and any remaining limitation will be recorded before handoff; local files do not establish publication. The earlier questionnaire confirmation tests remain untouched. No other queued work is included.


Completed local checks: the scoped renderer/data/unique-ID/idempotence check; three Node timing tests (unconfirmed/invalid time, exact nomination cutoff, poll transitions); existing Redlands structural checks (19 pages, 1,537 local references, 78 council features, 10 divisions, unchanged geometry and private-form guard); existing AEST/early-window tests; discovery (2,291 public routes, unchanged licence); isolated headless Edge at 390/680/1280 px on all three pages, process disclosure, People link/Back and no-JavaScript waiting states; actual phone screenshot inspected. No horizontal overflow or page-script exceptions were observed. National structural validation passed 997,937 assertions. Contract and publication results are recorded separately when completed; physical touch/screen-reader hardware is not claimed.

Contract verification passed: 2,081 registered contracts, zero failures (28 October 2026, 16:40 Australia/Brisbane). These are declared structural/evidence checks with their recorded limitations.

Publication integration: remote main advanced to ecbf94e6dd8c9c5ec21aee4f4d3af48dad8c30ab for portrait media while approval was pending. Its existing changes are preserved by a normal merge; the approved Redlands HTML, timing data and countdown module remain byte-identical to 93a1fa81. Affected 390/680/1280 px checks were repeated with the current shared stylesheet, and national validation again passed 997,937 assertions. Evidence is rebound to the actually tested shared CSS; no additional political research or directory changes are included.
