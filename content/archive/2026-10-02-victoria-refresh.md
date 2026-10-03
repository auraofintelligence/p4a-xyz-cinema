# Victoria refresh — 2 October 2026

This records what the repository previously claimed, why it changed and the observation periods. An archived statement is not an endorsement of its historical accuracy. The complete pre-refresh state file is preserved in [vic-state-before-2026-10-02.md](vic-state-before-2026-10-02.md).

| Superseded record / period | Replacement / period | Reason and source |
| --- | --- | --- |
| Research run 8 May 2026, Australia/Brisbane | Checked 2 October 2026, Australia/Melbourne | Fresh source check; use the jurisdiction timezone. The old research date remains in the preserved snapshot. |
| Jacinta Allan as current Premier; tenure start 27 September 2023 | Ben Carroll, sworn in 28 July 2026 | Official [Premier page](https://www.vic.gov.au/premier), updated 29 July. Preserve the former claim as historical; do not infer an unverified exact end date from the old record. |
| Assembly working count after May Nepean by-election: ALP54, LIB20, NAT9, GRN3, named independents2; 88 occupied seats | ALP54, LIB20, NAT9, GRN2, independents2, vacancy1; 87 sitting members | Tim Read died 19 September; [member page](https://www.parliament.vic.gov.au/members/tim-read/) and [Assembly list, 21 September](https://www.parliament.vic.gov.au/4a7318/contentassets/1ed360d4f9984647b7a85d16f2f82d0b/lamemlist-as-at-2026-09-21.pdf). Brunswick is vacant. |
| Council observation attributed to annual reporting at 30 June 2025: ALP15 LIB12 GRN4 NAT2 LCV2 AJP1 DLP1 LIBT1 SFF1 Somyurek1 | CSV checked 2 October, corroborated by 30 September list: ALP15 LIB11 GRN4 NAT2 LCV2 AJP1 ON1 LIBT1 SFF1 FF1 Somyurek1 | [Official CSV](https://povwebsiteresourcestore.blob.core.windows.net/lists/members.csv), [Council PDF](https://povwebsiteresourcestore.blob.core.windows.net/lists/lc_members.pdf). Old DLP row is a correction, not evidence of a post-May party switch. Rikkie-Lee Tyrrell is One Nation; Somyurek independent. |
| Moira Deeming counted within Liberal12 in old aggregate | Family First Victoria; Liberal11 | [Deeming statement, 10 September](https://www.parliament.vic.gov.au/parliamentary-activity/hansard/hansard-details/HANSARD-974425065-36940). Do not infer an exact former-party exit date. The textual Council seating page remains stale. |
| Nepean labelled “Recently held” with May working-count caveats | Historical 2 May 2026 result, separate from October membership | Retain the election and outcome; remove the implication it is a current statewide forecast. Use the linked official VEC result. |

## Election calendar checked, not reconstructed

The [current VEC election page](https://www.vec.vic.gov.au/voting/2026-state-election) gives enrolment close 3 November 8 pm; nominations 4 November 9 am–9 November noon; early voting 18–27 November; polling day 28 November 2026. All are Melbourne time. Older nomination dates (12/13 November) and older early-voting schedules are superseded source guidance following 2026 changes; those dates were not present in the archived state JSON. Candidate guidance contains a contradictory “Wednesday 17” reference; the current election calendar’s 18 November is used. No candidate announcement is presented as a formal nomination.

## Historical data retained with original periods

- 2022 results are historical election outcomes, not current party membership. The main Assembly result contains 87 districts; Narracan is linked separately to its 2023 supplementary election. Later Warrandyte (2023), Prahran/Werribee (2025), and Nepean (2026) results are linked separately.
- Census cards refer to the 2021 Census on 2022 boundaries. They have not been relabelled as 2026 statistics or transcribed here.
- Boundary edition: 2020–21 redivision, effective 1 November 2022; retrieved 2 October 2026. Raw WFS GeoJSON, source URLs and SHA-256 checksums are in `assets/maps/vic-provenance.json`. No vertex simplification or manual boundary edits.
- Member records retain each CSV row’s `LastUpdated` value separately from the retrieval/research date. Downloaded CSV checksum is recorded in `content/electorates/vic.md`.

## Numerical completion and further source checks

The initial atlas linked Mulgrave to its 2022 general-election result. This is superseded in the latest-result profile by the official 18 November 2023 by-election result; the 2022 outcome remains historical, not current membership. Numerical Census observations are now transcribed with exact cells, retaining 2021 observation year and 2022 boundary edition. Council-region medians are not supplied by the workbook and are not inferred. The 2026 Council voting rules were checked against the VEC amendments page: group voting tickets removed; at least five boxes above or below the line. No stale one-box/GVT instructions were found in the pre-update Victoria pages/source records. Early voting remains 18 November; no old venue locations are represented as current.


### Local-file, sorting and representation follow-up

Fixed direct `file://` loading through lossless classic-script geometry payloads; no browser bypass or local server is required. Grouped the map footer into four compact link groups. Added verified alphabetical/population/area/age/rent/household-income sorting, withholding volunteering/rented-tenure percentages pending denominator verification. Seven verified fields provide 616 dated district values. Region medians are not inferred.

Added geographic/current-party colour explanations, truthful five-member Council-region compositions and keyboard-accessible current Assembly/Council seat schematics. Majority markers (45/88 and 21/40) are separate from actual voting procedure; current parties are not predictions or assumed alliances. Local-government councils remain a distinct planned next layer, documented in `content/electorates/vic-implementation.md`; no council statistics are fabricated.


### Actual local-government atlas checkpoint

Added a separate local layer for 79 municipalities and eight unincorporated areas, plus 467 source ward/electoral-area features. Profiles include verified current rosters/vacancies, Moira administration, source election-history links and 1,975 annual ABS population observations (2001–2025). Statistical geography and legal boundaries remain explicitly distinct. Added many-to-many state-electorate intersections, including disclosed source slivers/topology defects. Original geometry is preserved exactly and both added layers support direct-file loading. Finance/service figures remain unavailable after the official LGPRF download returned HTTP 403 and other reuse terms remain unchecked. No navigation redesign, commit, push or publication is included.
