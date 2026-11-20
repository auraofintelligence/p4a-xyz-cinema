# 20 November 2026 Redland current candidate list

## Scope and cause

The Redland overview and candidate pages displayed all thirteen historical and current candidate records in one grid. Twelve records had accepted-nomination status. Liela D’Rose retained previously-certified status after her entry stopped appearing in the current ECQ register. Although that card explained the uncertainty, placing it alongside current candidates made the visible field look like thirteen.

The corrected renderer counts and groups only accepted nominations in the current ECQ-certified list. Announcements awaiting certification have their own group. Previously certified and withdrawn records are retained in a separate collapsed earlier-records section and are excluded from the current count. This preserves dated history without treating earlier certification as a current listing.

## Evidence and dependants

The ECQ event 653 candidate register was directly read on 20 November at 12:54 pm AEST and returned twelve current rows. Its current candidate IDs match the twelve recorded in the 19 November source review. The event remains the 12 December 2026 Redland mayoral by-election.

- Official register: https://event.elections.qld.gov.au/Events/VoteCardsView?EventID=653&EventType=8
- Prior verified roster: content/places/sources/redland-candidate-review-2026-11-19-final-noon.json
- Canonical records: content/local/redland-election.json
- Renderer: tools/redland_election.py
- Affected pages: states/qld/councils/redland/index.html and candidates/index.html
- The sources page carries the shared implementation review register and is regenerated for its changed page dates.

No source check date, candidate status, original announcement, certification date, affiliation, timetable or national election record is changed by this presentation correction. An absence from the current register is not re-labelled as a formally verified withdrawal.

## Verification and delivery

Regression checks cover current counts, status separation, preserved earlier records, safe rendering and dates. Applicable discovery, civic, publication-contract and storage checks run before publication. Publication evidence is recorded in content/history/site-publications.json after exact-commit deployment and live-file verification.

Cloud browser access is unavailable. Responsive browser review remains outstanding and is separate from structural and live HTTP verification.
