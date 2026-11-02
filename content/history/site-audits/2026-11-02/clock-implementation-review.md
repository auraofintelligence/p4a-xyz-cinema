# Countdown implementation review — 2 November 2026

## Scope and result
Read-only independent second pass over the combined audit checkout, including the preserved pre-correction records, actual delivered JavaScript, canonical data, generated HTML parity and source worker's official evidence in `state-federal-review.md`. This pass does not claim an additional independent nationwide live-source search.

`clock-classification-proof.json` enumerates every one of the **489** changed national events, with original date, exact original date basis, source URL, timezone and eight asserted safeguards. All pass:

| Group | Events | Original support |
| --- | ---: | --- |
| Queensland council/ward | 263 | Explicit ECQ four-year / last-Saturday rule, subject to regulation and official timetable |
| Queensland state | 93 | Explicit rule-derived constitutional normal date; expressly not a published writ/timetable |
| Western Australia state, including Council | 60 | Ordinary statutory second-Saturday date; source is a 2021 writ release, not a 2029 timetable |
| South Australia state, including Council | 48 | Ordinary statutory third-Saturday date |
| Northern Territory state | 25 | Ordinary statutory fourth-Saturday date; reviewed timetable did not confirm 2028 date |

These dates are not declared arithmetically incorrect. They remain recoverable in original history and `indicativeDate`; their active dates become null and the display reads **Awaiting confirmation to begin**. QLD social-feed claims remain unauthenticated leads, as recorded by the source worker.

No existing dated NSW, VIC or ACT national event is suppressed compared with Git baseline. The separately confirmed NSW 13 March 2027, VIC 28 November 2026 and ACT 21 October 2028 calendar dates remain active. ACT's unsupported 08:00 was removed from summary cards: it is a calendar-day countdown, not a claimed polling-opening time. QLD/WA/SA/NT summary 08:00 clocks are inactive. No replacement nomination or polling hours were invented.

## Time and delivered rendering
- IANA zones are retained for every changed national event. State cards expose their correct local IANA zone.
- Date-only arithmetic compares local calendar days, including Sydney daylight-saving midnight for ACT. It does not present hours/minutes to an invented polling instant.
- Existing offset-bearing confirmed deadlines remain instant-based; tests cover Perth deadline before/after expiry.
- VIC's no-JavaScript fallback is the stable date `28 Nov`, not stale `57` days. Actual JS tests cover before/on/after the local polling date, with a days-since label after it.
- Fifty state cards match canonical timing metadata. Scoped script/data cache keys are fresh on nine card pages; VIC has a fresh script key. National unconfirmed events have static waiting text and no clock activation attribute, so older cached civic JS cannot restart them.
- Acquisition code was inspected but not run. QLD derived supplementary events are also waiting; full original supplementary output is preserved. Official source snapshots and hashes were not rewritten.

## Validation observed
- `node tests/election-timing-confirmation.test.mjs`: pass, including all 489 events, four calendar waiting rows, date-only DST boundary, deadline expiry, VIC fallback and 93 QLD supplementary records.
- `python tests/test_state_clock_parity.py`: 2 pass before provenance-field restoration (see defect below).
- `node tools/check-civic-clocks.mjs`: 14 pass.
- `python tests/test_page_review_dates.py`: 6 pass after parent resolved temporary duplicate registry rows.
- JS syntax and Python compilation passed in first pass; CRLF-aware diff whitespace check clean.

## Defects reported promptly
1. Temporary duplicate route entries prevented generator import. Parent resolved them; six date tests now pass.
2. The narrow state-data rebuild accidentally removed the eight generated `sourceMarkdown` provenance properties. Parent notified at 04:49 UTC to restore these fields and make parity tests explicitly validate them separately from canonical Markdown. This does not alter countdown arithmetic, but must be fixed before publication. Reviewer did not edit shared files during the freeze.

No publication or live deployment verification is claimed by this review.

### Provenance repair verified, 04:49 UTC
Parent authorised the narrowly scoped repair. All eight `sourceMarkdown` properties are restored in `assets/state-data.js`. The parity test now asserts each generated path equals its canonical Markdown location, removes only that generated property for content comparison, and passes both tests. Timing regression suite passes again; CRLF-aware diff whitespace check is clean. No outstanding defect from this review remains.

### Browser follow-through corrections, 04:54 UTC
Parent's actual browser preview exposed stale introductory wording and uninitialised secondary metrics for null-date cards without a `data-countdown` attribute. Corrected source/generator and nine delivered card pages; initializer now includes every card's countdown display. All absent-date cases show waiting labels; real independently dated historical references retain local-calendar days-since values. Added actual-JS regressions for both cases. The legacy VIC validator now permits a date-only value only inside an explicitly day-precision card with the correct jurisdiction IANA timezone and a valid calendar date; timestamp validation is otherwise retained. `verify-vic-map.py`, timing regressions, state parity, JS syntax and CRLF-aware whitespace checks pass. Parent owns renewed browser verification and publication.
