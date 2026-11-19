# 19 November 2026 Victorian state election notices

## Scope and source observations

This scoped update adds two official notices to the existing 2026 Victorian state election guide. The canonical input is content/elections/vic-2026.json; its generator is tools/build-vic-election.py, which produces the guide and assets/vic-election-data.js. Candidate records, official ballot data, nomination stages, polling deadlines, geography and the broad 2 October candidate snapshot are unchanged.

- [VEC Electoral Commissioner statement, 19 November](https://www.vec.vic.gov.au/about-us/media/media-releases/media-statement-from-the-electoral-commissioner): the Commissioner reported a staffing-protocol breach involving an unauthorised individual at Victoria Street early voting centre in Richmond on 18 November. He said all activities were supervised and the voting process was not compromised. Sealed boxes with approximately 700 in-district votes were isolated as a precaution and will be tracked into the count as a separate parcel. The guide attributes this account to the VEC; it does not imply a changed ballot, invalid votes or an election result.
- [WAEC Perth interstate-voting notice, published 18 November](https://www.elections.wa.gov.au/about-us/media/whats-new/2641): eligible Victorian voters in Western Australia can vote at Level 2, 66 St Georges Terrace, Perth, on weekdays from 8:30 am to 4:30 pm, Perth local time, through Friday 27 November. The timeline uses a date-only entry and identifies the Perth venue; it creates no Melbourne-time countdown.

Both sources were directly read on 19 November 2026. The page implementation date is 19 November; this is not a broad candidate or source refresh.

## Daily check context

The final dedicated Redland evening check read ECQ event 653 at 5:00:02 pm and 5:00:49 pm AEST. Its 12 current certified listings and normalized register hash matched the earlier 4:06 pm check. No further Redland content or source dates were changed. A directly readable primary withdrawal statement for Liela D’Rose remains unverified; the existing uncertainty is retained.

The daily check read the AEC and eight state/territory commission hubs and targeted official event and vacancy sources. It did not establish a new Kempsey timetable, an adopted Gingin vacancy resolution, or a confirmed Bridgetown–Greenbushes poll date; existing distinctions remain. This is not a claim to have checked every Australian vacancy notice.

## Delivery and review

Generated dependants, preserved candidate and ballot data, source links, timing semantics, discovery, maintenance, civic navigation, JavaScript and site size are checked before publication. The exact content commit, Pages result and served changed files will be recorded in content/history/site-publications.json.

Cloud browser access is unavailable to this run. Post-deployment responsive and interaction review remains outstanding; HTTP and structural checks do not replace that review.
