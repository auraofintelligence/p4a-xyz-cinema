# State and territory electorate journey rules

Version 1.0. Updated 17 October 2026, Australia/Brisbane. Read with the [shared core](local-place-pattern.md), [acceptance gates](council-build-acceptance.md) and [report template](council-expansion-report-template.md). Keep this work separate from council and federal journeys; links between them preserve their distinct institutions.

## Audit before extending

Inspect the target portal, atlas, reviewed data, generators, source licences and QA first. The existing Victoria workbench is a substantial map/data baseline; it is not automatically a complete issues, systems, Twinkle, braided-account and implementation journey for each seat. Reuse working selection/search/representation/data and name missing depth. Do not rebuild blindly or label a profile popup a completed local journey.

## Establish the actual parliament

Primary sources must establish chamber(s), electoral structure, current district/region boundaries, seats per area, voting system, election administrator, terms/timetable, vacancy rules and current representation. Do not assume every jurisdiction has two houses, single-member districts, a directly elected head of government or Queensland election rules.

Distinguish lower-house districts, upper-house multi-member regions or whole-jurisdiction arrangements, and any other actual structure. A district and overlapping region are separate lenses, not a parent/child constituency hierarchy unless the geography actually supports that relationship. Select a chamber explicitly and label representative seat counts correctly. Never invent an upper-house layer or duplicate the lower-house map under a new label.

## Required journey and sources

State/territory portal -> chamber/area map and search -> select/inspect -> electorate/region journey. Use official commission boundary editions/results, parliamentary membership/Hansard/divisions, candidate declarations and attributable candidate websites. Give one coherent map viewport with clearly labelled layers and source editions. Only implemented deep journeys have an Open link; other profiles have honest coverage status.

Connect a resident's questions to actual state/territory powers, portfolios and delivery bodies. Include relevant council/federal dependencies without assigning every problem to the local member. A representative may advocate; parliament, executive, departments and councils have distinct powers. Demystify evidence, questions/submissions, proposal stages and outcomes through the same six doors. Twinkles remain one scene/gripe/breath, not miniature manifestos. Proposals/outcomes retain all three braided accounts.

Electorate ABS data must match a declared edition or documented correspondence. Do not substitute council/suburb values. Compare election results with primary/2CP/2PP/provisional/final and redistribution caveats. A multi-member region's result cannot be compressed into a fictitious single winner or council-wide political judgement.

## Candidates, decisions and clocks

Separate current MPs, public announcements/preselection, accepted nominations and ballot/result stages. Link public history, websites, interests/disclosures where available, precise parliamentary motions/divisions and stated reasons. No inferred motive; no unrecorded vote converted into a position. Optional personal learning remains within candidates.

Source the real general-election schedule and date basis, any early/postal timetable and jurisdiction timezone. Parliamentary vacancy and electoral vacancy rules can differ by chamber; source the applicable replacement/by-election branch before displaying it. Do not invent a by-election for a chamber where a different process applies. Test day-arrival/early-voting clocks at boundary times and daylight-saving transitions where relevant.

## Adapter and acceptance

Configure place kind, chamber, member count, area IDs, boundary edition, actual route relationships, representative/candidate schemas, sources, election stages and timezone. Keep these separate from council ward fields. Audit existing Victoria tools such as `tools/build-vic-map.py` and reviewed `content/electorates/`, `content/representatives/`, `content/elections/` before choosing integration points.

MUST pass shared gates plus actual-chamber coverage, multi-member representation, result measures, parliament-vote sourcing, edition-compatible statistics and honest atlas-versus-deep-journey status. Report any missing source or journey as partial. This guide authorises no bulk build or publication by itself.
