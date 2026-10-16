# GitHub upload preparation

Prepared 17 October 2026 for `auraofintelligence/p4a-xyz-cinema`. The current request prepares public source for upload; no commit, push or deployment is performed by the preparation tool.

## What is ready

The current public tree contains the Redlands journey and division maps, separate council/state/federal agent rules, the existing Victoria atlas, source assets and attribution, generators and validators. `AGENTS.md` makes the level-specific rules discoverable. The existing-coverage audit and Victoria–Redlands lessons explain what to reuse and what still needs depth.

`tools/verify-place-contracts.py` discovers manifests named `*-pattern-contract.json` below `content/`. Each new place registers a properly reviewed manifest there. `.github/workflows/civic-place-checks.yml` runs those contracts and the existing Redlands and Victoria checks on a push or pull request. This is a read-only validation workflow; it does not publish Pages or alter repository settings. Its commands have been checked locally; its first GitHub execution happens after upload.

The workflow reports failures. Making those checks required before merging is a separate repository setting; it has not been changed here. A failing check must not be described as blocking an independent Pages deployment automatically.

## Repeat the local checks

Run from the repository root with Python and Node available:

```text
python tools/verify-place-contracts.py
python tools/verify-redland.py
python tools/verify-discovery.py
python tools/verify-vic-map.py
python tools/verify-vic-numbers.py
python tools/verify-vic-councils.py
node tools/check-redland-clock.mjs
node --check assets/qld-council-map.js
```

A static pass preserves the dated review evidence; it is not a fresh source, legal, editorial or browser review. Follow the acceptance guide when source data or an implementation changes.

## Make the public-source bundle

```text
python scripts/prepare-github-upload.py
```

The output goes to `../_upload-ready/`, outside this checkout. The ZIP contains the complete current public-source allowlist, including existing uncommitted public work from earlier sessions. It is a source snapshot, not a selective patch or a new repository. Preserve the destination repository's `.git` history when applying it.

The adjacent JSON manifest lists every included path, byte count and SHA-256 hash. The tool checks tracked-file completeness, public path boundaries, common credential signatures, per-file size and ZIP readback. It preserves CNAME `p4a.xyz`, licences and source maps, the public AUKUS submission and the linked backend documentation. `.gitattributes` preserves raw GeoJSON bytes, including nested Redland geometry.

The root discovery files `robots.txt`, `sitemap.xml` and `llms.txt` are included. On the custom domain the effective crawler policy belongs at `https://p4a.xyz/robots.txt`; the local files do not affect the live site until uploaded. They preserve existing rights and add no reuse permission. See [discovery maintenance](discovery-and-rights.md).

Only the reviewed `qa/redland-20261017/` folder is included from local QA. Browser profiles, sessions and caches, dependencies, bytecode, environment/key files, temporary files and upload output are excluded. The local browser profile is over 1 GB and is not site source. Existing tracked QA under `tools/` remains part of the source snapshot.

## Apply and upload

Use the existing Git checkout or apply the snapshot to a clean checkout of the same remote. Review the manifest and intended Git diff, then stage the selected public files. Do not upload the ZIP as a single repository file and do not blindly stage the original workspace's QA directories. Large official geometry files are preserved; use Git for the upload rather than the browser file uploader.

Review the staged diff, commit with a description of the final change, and push only when upload is authorised. Check the new Actions run. Keep the existing custom domain and Pages settings unless a separate hosting change is requested. `.nojekyll` keeps this buildless static tree usable with a branch-based Pages setup; no new hosting registration or account is needed.

## Source references for the workflow

The workflow uses the official [checkout](https://github.com/actions/checkout), [Python setup](https://github.com/actions/setup-python) and [Node setup](https://github.com/actions/setup-node) actions. Their documented v7 usage was checked on 17 October 2026. Recheck the official action documentation before a future version change.
