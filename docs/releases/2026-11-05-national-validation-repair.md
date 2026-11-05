# National validation maintenance repair - local draft

Prepared 5 November 2026. Base: `00e4f9b56dbcddbd69830a34a8f959a24fe7eba7` on `auraofintelligence/p4a-xyz-cinema` remote main, verified before cloning and again before handover. Work used an isolated task clone. No push, publication, merge or deployment was performed. The separate pending election/publication task and its event update were not modified.

## Finding and scope

The national contract builder duplicated four shared implementation fingerprints, two report fingerprints and the national validation date into each of 2,080 place contracts. A changed report or shared fingerprint therefore rewrote every contract even when almost all canonical place declarations were unchanged. The aggregate runner already cached shared evidence and bounded its page cache; those optimisations did not remove this write coupling.

Two separate validation costs remained. `require_current_evidence` verified every fingerprint and then hashed the discovered artifacts again only to compare their path set. The national validator retained all parsed pages and loaded entire decoded geometry layers, with additional full decoded delivery buffers. The largest retained compressed layer expands to 179,302,110 bytes before JSON object allocation. The earlier external low-memory workaround did not change that stock implementation.

This draft changes validation tooling, CI regression coverage and maintenance instructions. It changes no election facts, source check dates, canonical place records, geometry, public routes, browser fixture hashes or delivered pages/assets. None of the 2,080 checked-in national contracts or saved QA reports was regenerated.

## Implementation

- Newly generated contracts reference one `content/places/qa/shared-contract-evidence.json` document for mutable shared hashes/report dates. Each place retains its full canonical-record pin, authored implementation date and declared human-review limits. Unchanged manifests are not rewritten.
- Standalone and aggregate validators resolve the same shared declaration and require complete current national/browser evidence. Corrupt, absent, chained, escaping or overriding references fail; a date cannot advance independently of its actual validation report. Legacy inline national evidence and local journey manifests remain supported.
- Artifact discovery is separate from hashing. Every present recorded dependency is still hashed and checked, the required artifact set still has to match, and available local-only originals still have to match their canonical source hashes. The national validator retains its complete before/after snapshots.
- Geometry delivery is hashed and compared in decoded chunks, then every feature is parsed separately. No geometry is sampled, rounded, transformed or simplified. Feature identity, joins, type/count and exact decoded delivery checks remain. Page and anchor caches each retain at most 96 entries; available retained-source hashes also use chunked reads.
- The new helper and standalone validator are included in national evidence dependencies. Exact-byte Git attributes protect them and the existing retained Redlands profile archive. The regression suite runs before national checks in Civic CI.

Memory remains proportional to the largest feature or other top-level JSON value, identity/canonical tables and bounded page inventories. An arbitrarily large individual feature is still a limit; this is not a claim of constant memory for arbitrary input.

## Actual validation

| Check | Result and limit |
| --- | --- |
| New shared-evidence/bounded-reader suite | PASS, 18 tests in the configured Python 3.12.14 runtime. Covers one-record scope, unchanged neighbour bytes/mtime, report-only updates, legacy manifests, corrupt bindings, shared-code/geometry changes, new required artifacts, stale browser fixtures, retained-source hashes, parser/truncation cases, byte comparison, cache eviction and original archive bytes. |
| Existing contract-date and page-review-date suites | PASS, nine tests. Canonical authored page dates remain unchanged. |
| Existing contract-cache check | PASS, 96-entry LRU semantics preserved. |
| Changed Python syntax and Git whitespace checks | PASS. |
| Full national structural validation with source hashes and `--no-write` | PASS, 169.295 seconds; 999,177 assertions, 2,080 canonical places/routes, 49 geometry layers and gzip round trips, 18 canonical delivery comparisons, 3,270 features across editions, 273 available original hashes, 2,113 pages, 176,159 local references and 14,658 fragment checks. 3,066 artifacts bound in the transient run; saved QA evidence was not replaced. |
| Initial observed full run | FAIL, only the retained `council-redland-profiles` hash. Windows had converted its original archive from LF to CRLF. The Git blob's SHA-256 already matched the canonical hash. Restored those exact blob bytes in the isolated clone and added the narrow byte-preservation attribute; no source content or recorded hash was refreshed. The repeat passed. |
| Initial test invocation | Environment error: the sandbox's virtual default temporary directory rejected writes. Repeated the suite with its temporary directory inside the writable task workspace; all 18 final tests passed. |
| Production contracts and evidence migration | NOT RUN. Existing saved evidence is stale against the intentionally changed validator dependencies. No contract-builder write or manufactured browser pass was used. Synthetic standalone/aggregate compatibility and rejection tests passed. |
| Browser, physical touch, screen-reader, live sources, separate Node picking/delivery/clock suites, remote CI and live deployment | NOT RUN for this tooling-only draft. Their separate acceptance requirements remain. No UI, map delivery, clock or source-fact change is claimed. |

The complete national assertion count matches the saved baseline's 999,177. The artifact count increases by two because the new geometry helper and standalone contract validator are now explicit dependencies. Declared coverage gaps and 1,062 absent local-only source snapshots remain explicit; hash checks do not establish fresh political/source truth.

## Measured effect

The [measurement record](2026-11-05-national-validation-repair.json) contains the synthetic comparison and full-run counts.

| Dimension | Before | Draft behaviour |
| --- | --- | --- |
| Report/date-only contract refresh after migration | 2,080 place manifests rewritten | Shared binding alone changes; synthetic regression confirms unchanged place bytes and mtimes. |
| One canonical-record edit after migration | Shared report fingerprints also forced unrelated contract churn | Affected place declaration plus shared binding changes; neighbour stays byte-identical. Actual generated-page dependants remain the existing generator's responsibility. |
| Hash work per unique shared evidence check | `2N + B` content hashes for present national artifacts `N` and browser artifacts `B` | `N + B`; regression counts actual digest calls. Completeness discovery and all hash verification remain. National before/after validation snapshots are unchanged. |
| Synthetic 3,000-feature geometry, 256 coordinate pairs each | 157,018,748 peak Python allocated bytes; 2.112 seconds | 4,649,005 peak Python allocated bytes; 1.931 seconds; identical decoded hash, all 3,000 identities and exact byte comparison. |
| National check scope | All national records/routes | Same complete scope; no incremental acceptance shortcut. |

The synthetic memory figures use `tracemalloc`, include its overhead and are not operating-system RSS or a national before/after benchmark. No old full memory-heavy run was launched for comparison.

## Remaining migration and publication work

The reviewed-evidence migration is intentionally pending. Use [national validation maintenance](../agents/national-validation-maintenance.md): reconcile against then-current main and the separate election work; save a genuinely completed final structural run; repeat affected real browser review wherever its code/page/fixture bytes or scope require it; then dry-run and intentionally regenerate the contracts. That first migration rewrites the 2,080 legacy national manifests once and creates one shared binding. Deploy compatible validators with those declarations. Later reviewed evidence updates stay scoped as described above. Never rehash an old browser fixture or advance a source date simply to satisfy a build.

Before any authorised publication, run the applicable independent gates. Civic CI does not gate Pages deployment and main is unprotected, so a post-push CI result cannot protect a Pages release. This preparation authorises no publication.

## Separate bounded recovery result

The requested November 4 commit `780fc0e641156b48ffa6b2d3fe62c9f9e43de462` was not found in the identified retained local P4A repository objects. The retained publication checkout exists, clean and detached at `9978928f49c4e01cc26b2b1058a92614fa38022e`. Its main checkout is at `6e924cc26a3c2e1fa50ec51e4b6a9874a2f6ab59`, with 51 modified tracked entries and 212 untracked entries. No retained workspace was changed. The cloud checkout name `p4a-election-20261104` has no verified local path; this bounded check does not establish recovery of that cloud commit. The separate local recovery record contains locations and read-only command evidence without private file contents.
