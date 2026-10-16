# Civic place journey rules: shared core

Version 2.1. Updated 17 October 2026, Australia/Brisbane. This replaces the earlier local-place guide and its addendum. It is the shared implementation contract; use it with the separate guide for the work actually requested:

- [Council and ward/division journeys](council-journey-rules.md).
- [State and territory electorate journeys](state-electorate-journey-rules.md).
- [Federal electorate journeys](federal-electorate-journey-rules.md).

Keep these scopes separate. A council page, state seat and federal division are different institutions and geographies; linking them does not merge their powers, data or elections. The [acceptance gates](council-build-acceptance.md) and [completion report](council-expansion-report-template.md) apply to each declared build. Their filenames retain the original council pattern for compatibility.

## 1. Read before building

Read the operator's current request, `README.md`, `LOCALISE_WITH_AN_AGENT.md`, this core, the relevant separate guide, `content/refresh-watchlist.md`, target source records/history, and the canonical [Twinkle format](../../content/rooms/twinkle.html#format) and [credibility rule](../../content/rooms/twinkle.html#ledger). Inspect existing implementation before copying or replacing it. Preserve unrelated working changes.

**MUST** denotes an acceptance requirement. Fix unmet requirements within authorised scope before calling the declared build complete. If a required source, right or capability is unavailable, deliver an honestly labelled partial result with the exact gap. A structural test pass alone does not prove source accuracy, good Twinkles or a usable map. Do not leave predictable shortfalls for the operator to discover repeatedly.

Expand one reviewed place at a time. A successful example is a pattern, not permission to invent local content nationally. Do not hardcode a national entity count or generate empty destinations as completed journeys. First audit the existing map, data, content and tests: reuse what works and report the missing depth. Do not discard a good atlas because its local issues/system journey is incomplete.

This is a static GitHub Pages archive. GitHub preparation alone does not authorise publishing, outside contact, nominations, spending or disclosure. Follow actual session authorisation without inventing a second approval gate for work already authorised. Never infer a private person's candidacy or political preference from research, authorship or hypothetical branches.

## 2. People first, from any doorway

Orientation may begin at States, a state/territory portal, council, electorate, ward, issue, candidate, statistic or external share. The civic journey begins with a person's experience and chosen relationships. Every page MUST name its place/institution and purpose, retain an obvious overview/parent route, and offer a few meaningful next choices. Avoid forced homepage restarts, compulsory single tiny steps and overwhelming inventories.

Connect six doors in both directions: everyday problems and Twinkles; systems/possibilities; people and decisions; maps/statistics/evidence; contribution/implementation; outcomes. An issue can reach evidence, a responsible body, an alternative and useful action. A system can return to the problems it might address and the outcomes needed to judge it. Related is not solved, funded, adopted or endorsed. Preserve the human's thread through the choices.

## 3. One interaction pattern at every real level

Use **map -> search or select -> inspect -> open** with the same controls and visual language. Buttons linking to static pictures do not satisfy an interactive map requirement.

MUST support drag/pan; wheel/button and supported touch zoom; keyboard controls; official-name/local-alias search; actual polygon selection; a visible area summary; explicit opening links; reset, loading, no-results and unavailable states. Search and clicking select the same stable record. Nested routes and direct-link state must work. Keep a keyboard-operable text directory and parent route usable without the map or JavaScript.

Only implemented destinations receive a local Open link. Unbuilt areas remain selectable with honest status and official routes. Include all areas from the chosen official layer while accurately labelling their kinds. Do not call an unincorporated area a council, a multi-member region a single-member district, or a service area an electorate.

Each overview MUST have one primary interactive map. Historical maps belong on Sources & dates. Style/layer choices share a viewport. Build the actual next level where it exists; do not invent geographic subdivisions to make every journey look identical. If no child electoral layer exists, explain that arrangement and offer the same human-content doors. Self-similar interaction does not mean fictional institutions.

## 4. Exact geography, no SVG maps

MUST use original authoritative boundaries with an attributed official geographic raster, suitable Wikimedia/Wikipedia raster, or raster rendered from an original official PDF. Do not introduce SVG maps, hand tracing, guessed rectangles, illustrative outlines or marker-only picking as boundary substitutes. Existing unrelated icons/archives are outside this map rule.

Retain raw file/response, exact request, filters/pagination, edition/effective date, retrieval/check dates, native/delivered/display CRS, rights, attribution, byte count and SHA-256. Check transfer limits and record completeness. Delivery MUST preserve every source coordinate, hole and multipart component without rounding, simplification, clipping or invented joins. Property adaptation and documented display projection are permitted while original coordinates remain retained and comparable.

Raster registration, drawing and picking MUST share a documented projection and viewport. Use a service's **returned image extent**, not requested bbox. Never hand-align until it looks close. Check axis order, datum and service changes; do not assume longitude/latitude. Verify known mainland, island, water/hole and neighbouring-area fixtures after map changes. Drawing/picking must share the hole rule and handle CSS pixels/device pixel ratio correctly.

Administrative sea is not land. Show real coast/islands beneath transparent area colours. Use a quiet default and restrained distinguishing colours; offer detailed roads as an optional licensed style. Do not call a fused cached map road-free if faint roads remain. Explain categorical colours, selection/hover/focus and any measured colour scale. Arbitrary colours carry no political/result meaning. Preserve source artwork/legends and distinguish local overlays from official styling.

Keep visible attribution, original source/edition/terms, readable alternatives and honest online/offline behaviour. Retain a licensed local raster fallback where possible. A local navigation display is not an official address/eligibility determination. If geometry or rights are missing, retain official links and label the interaction incomplete; never fabricate it.

## 5. Source and record contract

Edit reviewed canonical records first, generate second. Use stable IDs and bidirectional links. Republished service object IDs are not permanent public identity. Separate source geography codes from ABS codes. Minimum record meanings:

| Record | Required meaning |
| --- | --- |
| Place/area | Official identity/kind, parent/context, source IDs, aliases, route, edition/effective date, implemented status |
| Fact | Value or explicit unavailable, unit/denominator, observation period, geography/code, publisher, exact source, checked date, limits |
| Map/layer | Original request/file, edition, CRS, hash/counts, returned raster extent, rights/attribution, conversion, refresh rule |
| Election | Institution/event, status/date basis, polling date or null, timezone, separately sourced early/postal stages |
| Person | Public role/area, status evidence, official/chosen website, candidacy stage and checked date |
| Decision | Exact motion/amendment/stage, institution/date, recorded vote or absence of individual record, result, original record, reason evidence |
| Issue/Twinkle | Place, human gripe/seed, draft/verified status, serious context/evidence, perspectives, unknowns, systems/actions |
| Proposal/action | Source/author, stage/local relevance, alternatives, authority/responsible body, dependencies/burdens, options/measures |
| Outcome | What it cost, what was given freely, what changed; evidence/time window, attribution limits, unresolved work |
| Refresh | Scope/trigger, changed/unchanged/follow-up, source/previous version, check/build dates, actual QA |

Every factual claim MUST trace to supporting records. Keep observation, publication, retrieval, verification, effective-boundary and site-change dates separate. Rebuilding does not refresh research. Unknown is not zero. Preserve historical results/editions rather than overwriting them.

Maintain a route-by-route page and rule review register. Record work started, first verified build, last implementation update, what changed and review triggers; record rule versions separately. Distinguish newly built pages from existing entry/navigation pages updated to reach them. The Redlands reference is `content/history/civic-page-review-register-2026-10-17.json`, rendered on Sources & dates and as a readable release register. Keep it reachable through the sitemap, shared navigation and README.

Use ABS for statistical observations, the responsible commission/body for boundaries/results, institutions for their budgets/records, and original legislation for powers/rules. Secondary reporting gives attributed context, not replacement legal authority. Source-specific rights remain distinct from repository licensing. A snippet or third-party crawler is a discovery aid; keep primary evidence reachable.

## 6. Data and public concerns

Show dataset, period and compatible geography beside ABS values. Census counts, resident estimates, projections, electors, households and samples are different measures. Check official release notices before claiming newer Census data. A 2026 check does not make a 2021 observation a 2026 result. Do not sum medians, divide totals by wards, allocate residents by land area or relabel council data as electorate/ward data. Use supported correspondence methods with disclosed uncertainty for different boundaries.

Overlap claims must say which editions and whether they measure land, administrative area, residents or electors, with denominator and reproducible method. Visual comparison supports qualitative description only. Handle water/topology/date mismatches. A seat result is not a council-wide result. Distinguish primary vote, 2CP, 2PP, redistribution and final/provisional status in historical comparisons.

Include smaller/location-specific questions alongside major issues. Relate household and global pressures to local consequences through evidence. Distinguish scenario, forecast, opinion and observation; preserve competing interpretations without pretending equal evidence. Complaint counts, media frequency and engagement are not representative concern estimates. Quantified concern needs source, population/denominator, method and limits; otherwise unknown. Do not infer views from age, postcode or browsing.

## 7. Twinkles are spoken seeds, not policy cards

Agents MUST read the [canonical format](../../content/rooms/twinkle.html#format):

1. **One ordinary scene.** Use the quiet version without a gag for care, violence, grief or harm.
2. **One actual gripe.** Name it in the title. The self-contained spoken line stays on that gripe. A policy theme/system explanation belongs in a deeper room if people would not say it as an ordinary gripe.
3. **One breath.** Put the spoken seed visibly first. Evidence, policy options, systems and participation belong underneath or through the link.
4. **Punch at machinery.** Systems, forms, deals and doors; never a person, service, culture or grief.
5. **Checkable claims.** Sources/context must survive checking. Label illustrative draft copy; it is not a resident quotation, verified complaint or endorsed ledger entry.
6. **Local adaptation.** Use the actual place and checked experience; preserve approved national copy unless authorised to change it.

Redlands uses a 30-word mechanical guard, not a universal test of good writing. Read every new seed aloud and review meaning. A short briefing, bland question or solution slogan still fails. The described Truth Engine/Civic Ledger endorsement pipeline remains proposed until implemented; links alone confer no endorsement.

## 8. Wider systems and the braided economy

Connect Joyful Responsible Abundance to time, agency, care, belonging, useful work and worthwhile futures. A local problem may reach digital twins/civic mapping, legal-memory/RAG, Truth Engine, C-Hours, learning, cooperative ownership or democratic reform, then return to an accountable outcome. State what the connection might do, present implementation stage, dependencies and actual decision-maker. Do not imply a general proposal is deployed, funded, endorsed or proven locally. Legal-memory tools must expose original law/version/jurisdiction and uncertainty.

Substantive proposals/outcomes MUST distinguish:

1. **What it cost:** money, paid work, materials/resources, continuing obligations and who bears them.
2. **What was given freely:** voluntary time, care, knowledge/resources, with consent and appropriate verification.
3. **What changed:** intended/observed benefit or harm, access, ecology, relationships, skills, time freed and burden shifted.

Keep proposed/committed/spent/observed separate; activity is not an outcome. One C-Hour represents one verified freely given human hour, counted once even if several projects benefit, with no fixed dollar conversion. Static examples do not issue currency or run a shared ledger. Put the accounts in the deeper room, not every one-breath seed.

Lyric meanings may carry repair, choice, consent, care, Country, learning and wider horizons across several threads. Do not flatten each song into one feature or make culture compulsory. Imaginative health/AI ideas are not proven clinical/technical results.

When naming a song to explain its meaning, the title MUST link directly to its reviewed lyric/context page. A general music archive link does not replace the individual destination. Preserve the creator's title, record the source and link-check date, distinguish lyrics from released audio, and test that generated mentions retain their links. Redlands uses `content/local/redland-song-links.json`; other places must review the appropriate creator's destinations rather than inventing slugs or copying unrelated titles.

## 9. People, votes, why and election branches

Use an equal evidence structure for public people: role/area, public history, relevant experience, official/chosen site, primary records/disclosures where available and explicit gaps. Office, intention, announcement, preselection, accepted nomination, ballot, withdrawal, result and taking office are distinct. Do not assume recontesting or infer candidacy from authorship. Optional Aura Genesis/personal reflection belongs inside candidates, never as diagnosis, qualification, truthfulness score or compulsory test; private reflection stays private.

For votes preserve exact motion/amendment/stage and original minutes, division, Hansard or recording. Absence, recusal, abstention and unrecorded individual votes differ. For **why**, prefer dated attributable explanations. Label plausible interpretation and its basis; preserve alternatives; use reason not found where appropriate. Do not infer motives, dishonesty or agreement from a vote alone. Distinguish councillors' meeting votes, MPs' parliamentary divisions and electors' secret ballots.

Explain applicable branches from exploring/choosing not to run through lawful nomination/withdrawal, contest/result, service and handover. Adapt direct/indirect selection and vacancy rules. Absence, rejected leave, legal vacancy, replacement process and announced poll are separate facts. No invented date/countdown for a possible event. A rule-derived ordinary date may carry an explicit qualification and source; it is not an issued timetable.

Keep polling day, early-voting opening/closing dates, eligibility/hours/locations and postal stages separate for each event. Leave unsupported dates null. Clocks MUST share the reviewed event record, target jurisdiction timezone and date basis, including daylight saving where applicable. A day-arrival clock is not booth opening. Test before/on/after boundaries. Passed dates prompt source/status verification, never silent four-year roll-forward.

## 10. Agent continuity, cultural context and static privacy

Carry the human's purpose, place/institution, chosen thread, record IDs, sources/versions, uncertainty, disagreement, permission, stage and useful choices across handoffs. Correct misunderstandings explicitly. Narrative continuity may change with evidence or human intent. Assign ownership to prevent duplicated Civic AI research. Observations, corrections, alternatives, offers and authorised formal actions can all be meaningful contributions.

Country, cultural identity, rights and permission cannot be inferred from electoral/statistical polygons. Use community-authorised public self-description and respect cultural/data permissions and restricted material. Label statutory recognition layers accurately. Missing published polygons do not mean missing Country or rights. Do not contact others without authorisation or impersonate consent.

Distinguish draft/submitted/acknowledged/decided/implemented/observed. A download or prepared letter is not submission or mandate. Do not infer political preferences, create persuasion profiles or transmit private notes. Private note export must require deliberate local download and remain disabled without a safe JavaScript handler; never leak text in URL queries. State actual storage/external-map requests. This archive is not a live database, identity service, nomination portal, lie detector or automated civic authority.

## 11. Existing reference and adapter limits

Redlands: `content/councils/redland.json`, `content/local/redland-connections.json`, `redland-divisions.json`, `redland-election.json`; map provenance in `content/councils/qld-map-sources.json`, `qld-basemap-sources.json`, `redland-divisions-sources.json`; builder `tools/build-redland.py`; UI `assets/local-council.*` and `assets/qld-council-map.*`; widget `tools/qld_council_widget.py`; history `content/history/redland.md`.

Its route is States -> Queensland -> councils -> Redlands -> ten division overviews. Its 19 pages and ten divisions describe this implementation, not national requirements. The official quiet pastel PNG, optional topographic roads, returned EPSG:3857 registration and unchanged geometry are the current standard, replacing the earlier Topo-default description.

The renderer reuses behaviour but still contains Queensland/Redland bundle names, IDs, source fields, counts, routes and special cases. It is **not a drop-in national data loader**. Parameterise or isolate those dependencies without breaking existing routes. Each place adapter supplies actual kind/labels/IDs/aliases, parent/child routes, built flags, official references, source metadata, projection/style and election context. Never copy `6250`, ten children, Weipa handling, Queensland services or AEST universally. Avoid global collisions between widgets.

The existing Victoria atlas is an implementation to audit/reuse, not evidence that every electorate already has a Redlands-depth civic journey. Use the separate guides and the current implementation inventory. The national Wikimedia PNG is orientation, not an electoral dataset; provenance is in `assets/maps/australian-states-wikipedia.json`.

## 12. Mandatory source -> build -> verify -> report loop

1. Inventory requested scope/authorisation, existing work, real arrangement, sources/rights and gaps. Start a report from the template.
2. Review/acquire original evidence with provenance. Keep acquisition separate from deterministic generation; generators must not silently fetch new political facts.
3. Adapt real place data/routes and generate only scoped outputs. Preserve surrounding content/history and source check dates.
4. Maintain and register the place's real reviewed manifest under `content/` with a filename matching `<place>-pattern-contract.json`, for example `content/local/<place>-pattern-contract.json`. Do not register a placeholder or declare unchecked work complete. Run `python tools/verify-council-pattern.py --manifest content/local/council-pattern-contract.json` for the reference; pass the new place's own manifest for another build. Do not alter the reference to hide failures. Run `python tools/verify-place-contracts.py` to discover and check every registered `content/**/*-pattern-contract.json`, plus relevant place-specific source/geometry/clock/link/syntax checks. Read what each check actually covers.
5. Complete all applicable [acceptance gates](council-build-acceptance.md) in the browser and source/editorial review. Save actual results/screenshots. Fix failures and repeat affected checks. A second build must produce identical scoped outputs.
6. Append dated history/refresh results, including no-change source checks. Finish the report: complete only when mandatory gates for the declared scope pass; otherwise partial/blocked with exact unmet conditions. Do not claim a pass for unperformed checks.
7. Prepare GitHub through scoped diff, case-sensitive/relative-link, generated-file, rights, privacy and size review, following [GitHub upload preparation](../github-upload.md). Exclude private source attachments, credentials, local fixtures and machine paths unless intentionally suitable public evidence. Report prepared/staged/committed/pushed/deployed accurately and follow actual authorisation.

`.github/workflows/civic-place-checks.yml` runs the repository's read-only civic checks on push, pull request and manual dispatch, including registered place contracts and existing Victoria/Redlands validation. Add each new place's manifest after its source, browser and editorial self-checks so later agents cannot silently omit it from the recurring gate. CI success means those automated assertions passed for that revision; it is not proof that new sources were reviewed, every browser interaction works or the writing meets the Twinkle rules. Retain the report and actual manual evidence.

Current reference checks: `python tools/build-redland.py`, `python tools/verify-redland.py`, `node tools/check-redland-clock.mjs`, then the manifest validator. Preview: `node scripts/serve.mjs`, `http://127.0.0.1:8768/pages/states.html`. These commands do not validate new jurisdictions automatically.

Refresh on boundary editions/effectiveness, representation, official vacancy/election/timetable/result, law, ABS revision/release, budgets/annual reports, service/project status, corrections, source terms/projection/service changes and Twinkle-format changes. Keep historical versions/conflicts. Recheck only affected scopes, re-run relevant gates and leave a usable handoff. A ticking clock is not a refreshed political fact.
