# Federal, state supplements and ward handoff

**Resume update, 17 October 2026:** The user's subsequent explicit resume instruction authorised continued work. The NT/WA/SA ward integration has now been merged locally; see [the scoped integration report](ward-integration-2026-10-17.md) and `sources/council-ward-integration-verification.json`. The stopped-state evidence below remains historical. New national page/build/browser acceptance remains with the root workflow; this update is not a publication or blanket completion claim.

**NT detail continuation:** The separate official current-roster and historical-event supplement is now built and coordinated with the council merge owner. See [the exact scope, source gaps and verification](nt-council-details-2026-10-17.md). It supplies 16 independently sourced roster snapshots and 80 historical parent contest contexts with all 336 official nominee names. Six exact-date gaps remain explicit, including two failed nomination rounds; all earlier missing candidate pages were resolved through the ordinary browser.

Saved 17 October 2026, Australia/Brisbane. Work stopped at the user's explicit request because repeated network approvals were disrupting the session. No further acquisition, generation, publication or research is authorised by this handoff alone. No Twinkles were added.

## Saved federal adapter

`tools/acquire-federal-places.py` builds `content/places/federal.json`. The saved canonical file contains **159 places, 226 independently current representatives and 1,468 historical contestants**:

- 150 serving House divisions, one distinct future O'Donoghue division and eight Senate areas.
- Current 150 MPs and 76 Senators from the public official Parliamentary Handbook API. Historical election winners were not used as a current-office roster.
- Complete 2025 AEC House and Senate candidate records, plus the 2026 Farrer by-election. Senate candidate vote measures are explicitly below-the-line first preferences; these must not be relabelled as each candidate's share of all Senate votes.
- Eleven exact AEC boundary layers under `assets/maps/national/federal*`, including serving 2025 and next-election SA/TAS/ACT 2026 editions. Same-name next-edition features retain `mapRefs`. Grey and future O'Donoghue remain distinct records; no current MP or previous poll is invented for the new name.
- Future federal election dates remain null/unannounced where no date was established.

Saved checks: `content/places/sources/federal-verification.json`, `federal-geometry-audit.json` and `federal-link-check.json`. The completed geometry check compared 2,880,317 coordinate pairs across 7,649 rings; original native GDA94 coordinates are retained with the datum-alignment limitation. The completed HTTP check covered 311 distinct official AEC place/event URLs. APH profile URLs did not receive a successful HTTP status check where the main APH host denied direct access; that is not hidden by the AEC check.

Original federal sources are retained under `content/places/raw/federal/`, excluded from public packaging. Public federal source manifests and verification reports remain under `content/places/sources/`. The Handbook JSON/client and official HTML have separate rights/privacy review requirements. Do not publish a full original biography/contact-data dump merely because it was retrievable. Preserve public factual name/role/profile links and provenance hashes.

## Saved Queensland and NSW state supplements

The state agent owns merging these supplements into `content/places/state.json`; this agent did not edit that shared file.

| Supplement | Districts | Independently current MPs | Historical contestants |
| --- | ---: | ---: | ---: |
| `content/places/state-qld-details.json` | 93 | 93 | 541 |
| `content/places/state-nsw-details.json` | 93 | 93 | 603 |

Reproducible local adapters are `tools/acquire-qld-state-details.py` and `tools/acquire-nsw-state-details.py`. Their minimal public-profile factual extracts are `content/places/raw/state-qld-supp-member-profiles.json` and `content/places/raw/state-nsw-supp-member-profiles.json`. No contact addresses, phone numbers or biographies are included in the NSW factual extract.

Queensland includes 525 contestants from all 93 districts in 2024, seven from Hinchinbrook on 29 November 2025 and nine from Stafford on 16 May 2026. The next normal general-election clock is rule-derived 28 October 2028, with statutory qualifications preserved. The 2026 redistribution applies to the 2028 general election; earlier by-elections continue using the serving boundary edition. The official member PDF says 23 September 2026; the retrieval/check date is separate. ECQ archive XML source event IDs and count stages were retained, including its `final="NO"` flags rather than silently upgrading the original stage.

NSW includes all 93 district ballots in 2023 and the six subsequent Northern Tablelands, Epping, Hornsby, Pittwater, Port Macquarie and Kiama by-elections. All 603 normalized first-preference totals reconcile to their respective official formal-vote totals. The published next election is **13 March 2027**, with its clock targeting **18:00 Australia/Sydney (+11:00)**. Do not substitute the ordinary fourth-Saturday assumption. Current MPs were taken from each official profile's **Current positions** table, excluding **Prior positions**. Current parties are omitted where a separate current-affiliation source was not retained.

Saved reports are `content/places/sources/state-qld-supp-verification.json` and `state-nsw-supp-verification.json`. These are transformation/source-join checks, not full per-place browser reviews. At stop time, a local read of `state.json` showed 93 populated Queensland and 93 populated NSW current-member records, indicating the state merge had progressed. The state agent must confirm the full event/source merge and rebuild dependent pages before calling it complete. NSW statewide Legislative Council coverage remains a separate task; the public current directory showed 41 listings, so do not invent a 42nd member or infer the vacancy reason.

Original source files under `content/places/raw/state-qld-supp-*` and `state-nsw-supp-*` must stay local unless their separate reuse/privacy basis is reviewed. Full parliamentary PDF/text, profile HTML and application code are not automatically public release assets. Transfer logs preserve direct 403/404 failures without bypass. The Queensland transfer log also records an expired ECQ TLS-certificate limitation from its earlier public read; the later ward acquisition uses fully verified TLS and has no such fallback.

## Saved NT and WA ward supplement

Ready for the council agent to merge: `content/places/council-ward-supplement.json`, built by `tools/acquire-council-ward-supplement.py`. It follows the shared `{sources, layers, places}` schema.

| Jurisdiction | True wards | Parent councils | Original polygon features | Exact coordinate pairs |
| --- | ---: | ---: | ---: | ---: |
| NT | 51 | 13 | 830 | 70,495 |
| WA | 113 | 28 | 202 | 177,095 |
| Total | 164 | 41 | 1,032 | 247,590 |

The openly licensed source is the official Digital Atlas of Australia/Geoscape Wards service. Its live item metadata states August 2026; the service description still states November 2025. Both are recorded, with retrieval kept separate. The retained licence explicitly states Commonwealth CC BY 4.0, independently of the more restrictive Landgate source previously considered.

Delivered files are `assets/maps/national/council-ward-supp-nt.geojson`, `council-ward-supp-wa.geojson` and their `.gz` equivalents. Native GDA94/EPSG:4283 longitude/latitude coordinates are retained as exact source bytes, including original feature boundaries and holes. There is no simplification, dissolve, guessed division or claimed datum transformation. `wd_ply_pid` is the unique feature ID; one place per stable `ward_pid` uses additional `mapRefs` for every other source polygon part. Every source object ID and polygon part has a corresponding place reference.

The parent join uses the official Geoscape `lga_pid` and distinct LGA names; each abbreviated name matched exactly after punctuation/spacing normalization to one existing canonical council. Source ward/LGA IDs and names remain in each place. Current ward representatives and election histories are deliberately empty in this geometry supplement and require the council agent's separate sourced merge; do not overwrite populated canonical people/events with empty arrays.

`content/places/sources/council-ward-supp-verification.json` reports PASS for source object-ID completeness, exact delivery/source SHA256 equality, gzip round trips and all-part place joins. Transfer metadata, live licence/item metadata, source geometry and distinct parent identities are retained under `content/places/{raw,sources}/council-ward-supp-*`. All ward transfers used the bundled Python runtime with certificate and hostname verification enabled. No TLS or access-denial bypass exists in this adapter.

At the stop-time read, **zero of the supplement's 164 IDs were present in `councils.json`**. The council agent had just said it was beginning this merge; verify the final shared file before regenerating or claiming integration.

## NSW ward discovery saved, not implemented

No NSW ward geometry is included in the delivered supplement. Geoscape Wards explicitly has no NSW coverage.

- Western Parkland Councils publishes 18 polygons under CC BY 4.0, retained as `content/places/raw/council-ward-supp-nsw-wpc-wards.geojson` with its metadata. The metadata is dated November 2021. Some features are whole undivided councils, not wards (Campbelltown and Hawkesbury), so they must not become fictional ward pages. Current structures and boundaries require reconciliation.
- The public North Sydney item expressly prohibits reproducing its map without permission. Only its metadata was retained; its geometry was not downloaded or delivered.
- The NSW Spatial Portal's three ward proxy services failed with `Error generating token`. No token/authentication workaround was attempted.
- A useful last public lead was found in the NSW Electoral Commission's Ballina page: its own map loads the public KML URL `https://kml.elections.nsw.gov.au/kmlservice.asmx/getKMLRedist?colortweak=1&servertype=prod&location=LG2023/Ballina_boundary.kml`. The previously started request completed before the stop and retained **306,171 bytes** as `content/places/raw/council-ward-supp-nsw-ec-ballina.kml`, SHA256 `c88b9a62237062c34c0147bb88b7aa9f86fbe92dec6bfa6b81777b5b3de6e066`. It is **unparsed and unreviewed**, not a completed NSW map. The first incomplete URL failed; the corrected URL came directly from the public client's documented suffix, without bypassing an access restriction.
- Ballina's page labels this map data “2023 Redistribution of Local Government Areas for LG2401, D2023-10-30”. A retained NSWEC copyright page states CC BY 4.0 with exceptions for third-party material, personal information, trademarks, media and source code. Confirm the KML's attribution/rights before any future delivery. The client JS is for local inspection only and is expressly outside that licence.
- Suggested further SA/WA/NT legal council-wide LGA acquisition was **not started**. Existing ABS approximations cannot be relabelled as legal council boundaries.

## National verification and contracts

Owned tooling saved: `tools/verify-national-places.py`, `tools/build-national-contracts.py`, and the in-process/cached `tools/verify-place-contracts.py` runner. The existing Redlands manifest passed the optimized runner previously. The national checker distinguishes missing research coverage from structural failure and makes no browser or live-link claims.

At stop time, `content/places/qa/national-validation.json` was **FAIL**, mode `generated-pages-and-data`, and stale relative to subsequent dataset merges. No final default national PASS has been obtained for the latest generated site. `content/places/qa/browser-review.json` does not exist. Accordingly **no new national per-place contract manifests have been generated**. The contract builder correctly requires actual passing default national validation and real passing browser evidence, binds the entire canonical place record, and keeps source/browser limitations explicit.

Do not claim national completion, final browser/accessibility acceptance, complete council member/contestant coverage, or successful source-rights publication review from the supplemental PASS reports. Further generation, map/browser review, discovery/sitemap checks and manifest binding remain for a future explicitly resumed session.

## Running work and stop state

No unified-exec session ID remains outstanding from this agent. The last interrupted fetch had already completed and wrote the successful Ballina transfer record. A local `Get-Process python` check returned no Python processes. CIM process enumeration was denied by the sandbox and was not escalated; no unrelated process was terminated. No new network requests were made after the stop instruction. All completed normalized supplements and local provenance are saved in the shared working tree; no commit, push or publication was performed by this agent.
