# Council journey rules

Version 1.0. Updated 17 October 2026, Australia/Brisbane. Read with the [shared core](local-place-pattern.md), [acceptance gates](council-build-acceptance.md) and [report template](council-expansion-report-template.md). This guide covers local government and genuine local electoral subdivisions. State and federal seats have separate guides.

## Before implementation

Source-check the official council/body, its current boundary and its actual elected or administrative arrangement. Primary sources must establish the electoral administrator, current legislation, ordinary timetable, vacancy process and mayor/leader selection. Do not assume Queensland law applies nationally. Handle undivided, ward/division, multi-member, direct/indirect mayoral and exceptional administration arrangements as actually documented. ACT, unincorporated and special-body contexts must not be turned into fictional councils.

Record official source IDs separately from ABS codes, actual ward/division names/counts and effective boundary edition. A suburb is orientation, not an official address assignment. Keep Country and service areas distinct.

## Required journey

State/territory -> council map/search -> council inspect/open -> one council overview map -> real ward/division inspect/open where applicable. Every real child overview reconnects to local questions, systems, people, evidence, contribution and outcomes. For an undivided council, state the council-wide arrangement and preserve the content journey without inventing children.

Council-specific substance includes rates/charges, budgets and actual spending, service delivery, planning, assets, resilience, participation and meeting records where locally relevant. Distinguish council authority, state/federal responsibility and external-provider dependency for each issue. Link wider P4A systems only with their present stage and local relevance. Follow canonical Twinkle rules and the three accounts: cost, freely given contribution, change.

## People and evidence

Use the current official councillor/mayor directory and election declarations/results. Names are dated published listings, not independent verification of every profile claim. Public meeting records must preserve motion/stage and individual-vote availability. Reasons need attributable sources; plausible interpretation remains labelled. Do not infer a prospective candidate from this project's author or private discussion.

A possible mayoral by-election stays conditional until a primary source establishes the actual vacancy process and poll. Leave decisions/absences do not themselves supply a poll date. Direct election and selection by councillors require different branches. Keep ordinary/extraordinary events and their early/postal windows separate. Never copy Redlands' 2028 date or hypothetical vacancy threshold.

Ward statistics require compatible official data/methods. Council-wide Census/ERP cannot be divided by ward count or relabelled as ward data. Historical enrolment printed on a review map is historical.

## Adapter and acceptance

Supply actual entity kind, IDs, labels, source fields/CRS, boundaries, child count/routes, representative sources, election/selection context, timezone, official links and built flags. The Queensland renderer still has Redland-specific dependencies; isolate them before reuse. Keep raw authoritative geometry unchanged, official raster registration and the quiet optional-road style contract. One overview map, no SVG maps.

MUST pass the shared gates plus council-specific checks: all genuine child units covered; undivided arrangement explicit; no assumed direct-mayor/vacancy rule; council and councillor powers differentiated; ward-data gaps honest. Record exact source checks and browser results. Build one council fully before expanding the next. A source-rights or geometry gap is partial, never a reason to invent the map.

Reference: `tools/build-redland.py`, `content/councils/redland.json`, `content/local/redland-divisions.json`, and `docs/agents/local-place-pattern.md`. These demonstrate implementation and acceptance behaviour, not universal local law.
