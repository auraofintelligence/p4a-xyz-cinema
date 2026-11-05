# National validation and shared contract evidence

Version 1.1, 5 November 2026. Inherit [the fractal update guide](fractal-election-updates.md) and [acceptance gates](council-build-acceptance.md). These are maintenance instructions, not a fresh source, editorial, geometry or browser approval.

## What remains checked

The national validator still checks all canonical records, registered routes, map joins, polygon feature types/counts, exact decoded geometry delivery, available retained-source hashes, local links/assets/fragments and rendered people/event parity. It takes complete artifact fingerprints before and after validation. No check is selected away for a small election change.

Geometry is compared and hashed in decoded byte chunks, then parsed one feature at a time. Coordinates are not simplified or sampled. Memory depends on the largest feature or other top-level JSON value, canonical tables, feature-ID sets and at most 96 parsed pages plus 96 anchor inventories. This does not promise constant memory for arbitrarily large individual features. Malformed or truncated input fails. Separate geometry/picking, clock, source, browser and editorial gates still apply.

Evidence completeness uses artifact discovery without hashing the same files a second time. The saved SHA-256 of every present artifact is still verified, including browser fixtures; retained local-only originals still have to match their canonical source hashes when present. Missing local-only originals remain an explicit limit, never a new source pass. Validation itself continues to hash before and after the run to detect changing inputs.

## Stable per-place declarations

Newly generated national contracts retain the full canonical place pin, authored route implementation date, route checks and human-review limits. Their `reviewEvidence.sharedEvidence` refers to `content/places/qa/shared-contract-evidence.json`.

That shared document holds the actual validation review date, report paths and shared renderer/report fingerprints once. The reference is intentionally stable across later reviewed evidence updates. Both `verify-council-pattern.py` and `verify-place-contracts.py` resolve it and enforce complete current national and browser evidence. Missing, malformed, chained or overriding shared bindings fail. The aggregate runner reuses identical shared checks within the run; it still checks every place declaration. Legacy inline evidence remains supported and enforced.

The shared binding also fingerprints `content/places/qa/contract-set.json`. That index names and hashes every generated national contract. It remains `in-progress` while a multi-file migration writes outputs; completion is replaced last. Missing/extra/changed contracts or an incomplete marker fail standalone and aggregate acceptance. An interrupted build can be resumed, but generation success is not post-migration acceptance: run the full aggregate and all applicable gates before publishing. A report-only refresh replaces the shared binding atomically without rewriting the unchanged index or place contracts.

All acceptance runs use content snapshots, not modification-time/size freshness. A final hash pass covers all read documents/pages, declared evidence and transitive national/browser dependencies, including previously absent local originals. Added/removed dependency or contract membership also fails. Builder guards run before writes, after output assembly and after completion replacement; interruption or a failed final guard leaves an incomplete multi-file set. Supported use requires an exclusively controlled, stable workspace through final validation and commit. These guards detect persistent injected changes, including equal-size changes with restored timestamps. They do not make arbitrary external change-and-restore attacks or edits after the final check impossible. Do not run generators concurrently with acceptance or migration.

## One-time migration, then routine updates

Do not mass-rebind the checked-in legacy contracts merely to demonstrate a draft. Changed validator/helper bytes invalidate the old national evidence. Keep existing report/source dates and browser fixture hashes intact until their required checks have actually been completed.

For an intentional migration:

1. Reconcile the local fix with the then-current main and any separately pending election/publication work. Preserve that work's canonical records and history.
2. Run the new regressions, applicable checks and default national validation with source hashes against stable final inputs. `--no-write` verifies without replacing a reviewed report; omit it only when intentionally saving that completed structural run.
3. Check whether the recorded browser code, tested pages and fixtures are byte-for-byte unchanged and whether their declared scope still covers the affected work. Repeat affected real browser review where needed. Never refresh an old fixture's hash or review date to make it pass.
4. After current structural and genuine browser evidence pass, run `python -B tools/build-national-contracts.py --dry-run`, then intentionally run the builder without `--dry-run`. This first migration rewrites the legacy national contracts once and creates one shared binding. Review the complete diff and run standalone representative contracts plus `python -B tools/verify-place-contracts.py`.
5. For subsequent reviewed updates, the builder writes a place contract only when its own declaration changes; a report/date-only refresh writes the shared binding alone. A scoped canonical edit changes that place's full-record pin and any genuinely affected route-date declarations. Neighbours retain identical bytes. National validation still covers the complete national inputs.

The builder never fetches sources, changes a source check date, generates browser evidence, or upgrades a structural check into per-place civic completeness. Browser, source, editorial and geometry limits remain separately declared.

## Before publication

Run the required checks before publication. Civic CI is independent of Pages deployment, and unprotected main does not provide a deployment gate. This document and a local PASS do not authorise pushing, publishing, merging or deploying.

Regression command: `python -B -m unittest discover -s tests -p test_national_validation_scope.py`. This includes late transitive mutations, preserved metadata, builder assembly/write/completion races, malformed evidence and interrupted/partial migration. Existing date provenance tests and `python -B tools/check-contract-cache.py` remain applicable. See [the repair report](../releases/2026-11-05-national-validation-repair.md) for its exact base, actual checks, measurements and delivery state.
