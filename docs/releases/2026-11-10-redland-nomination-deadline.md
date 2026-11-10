# Redland nomination deadline and certified-candidate search, 10 November 2026

Scope: Redland City mayoral by-election, event `redland-mayoral-vacancy-2026-10-28`, council `qld-council-6250`. This is a narrow correction from published main `9ba19a3bf5400acd2022ec6b46e17b913f617a08`, not the separate unpublished national election review.

## Confirmed facts and routes

[ECQ event timetable](https://www.ecq.qld.gov.au/elections/election-events/redland-city-council-mayoral-by-election) confirms nominations from 10 November until **noon AEST on Thursday 19 November 2026**, without an opening clock time. The full-postal election is on 12 December; votes must be completed by 6pm that day and received by ECQ by 5pm on 22 December.

The [official candidate search](https://event.elections.qld.gov.au/Events/VoteCardsView?EventID=653&EventType=8), linked from ECQ event details, says nominations appear after certification by the Returning Officer. A submitted form is not a certified nomination, and public intentions are distinct. No rows were exposed in text retrieval, so neither candidate acceptance nor an empty field is inferred. The existing five announcements and display order are unchanged.

Canonical inputs: `content/local/redland-election.json`, Redland’s event in `content/places/councils.json`, and the existing renderer. Rebuild the overview, candidates, sources and national elections page. Previous local facts are retained in the before-deadline snapshot. The prior national record remains in [the published base revision](https://github.com/auraofintelligence/p4a-xyz-cinema/blob/9ba19a3bf5400acd2022ec6b46e17b913f617a08/content/places/councils.json); no duplicate national snapshot is included. [Source record](../../content/places/sources/redland-timetable-2026-11-10.json) carries exact scope and gaps. Ordinary 2028 timing, unrelated source dates, geometry, styling and advocacy are unchanged.

## Checks and publication

Pre-publication checks passed: 999,291 national assertions; all 2,081 registered place contracts in publication mode; the independent civic workflow checks; five Redland election tests; four publication/browser-binding regression tests; and the whitespace check with the repository’s preserved CRLF convention. Only Redland’s national record changed, all five candidate records retain their exact prior order/content, and ordinary-election timing, early-voting data and whole-site audit history are unchanged. Storage checking retains the existing less-than-5% headroom warning. Publication and live browser acceptance are not yet claimed; they will be recorded against the actual deployed revision. The historical election JSON and renderer browser-only fingerprints retain their old hashes/dates and are explicitly deferred only in publication mode. Current factual/data/build checks remain required; regressions preserve non-browser fingerprint enforcement and strict post-live rejection of stale browser evidence. Cloud-only browser acceptance follows deployment.

The duplicate national history snapshot was omitted after publication review declined its upload. The current canonical inputs and generated pages are unchanged by that omission. Historical facts remain recoverable in the published Git revision linked above.
