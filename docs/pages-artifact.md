# Lossless deployment packaging

Prepared 6 November 2026. This is a deploy-artifact preparation change, not a new
source-data review, a hosting migration or a claim that the live site is smaller.

The public-source repository retains QA evidence and all original map formats.
The Pages artifact may omit only raster screenshots under `tools/publication-qa/`
which are not named in retained HTML, CSS, JavaScript, JSON, Markdown or discovery
text (including SVG and escaped names). Referenced screenshots stay included, even
when a basename is ambiguous. A runtime reference to the QA directory retains every
candidate. These are conservative static checks, not proof against every possible
dynamically constructed URL; inspect the omission manifest before any deployment.
Maps, raw GeoJSON fallbacks, compressed deliveries, attribution, reports, contracts
and source dates remain byte-for-byte unchanged. Nothing is deleted from Git.

Run the existing Civic place checks in the complete checkout first. Then run:

```text
python -B -m unittest discover -s tests -p test_pages_artifact.py
python -B scripts/prepare-pages-artifact.py --check --report ../pages-package-plan.json
python -B scripts/prepare-pages-artifact.py --output-dir ../pages-artifact --report ../pages-artifact.json
```

The output directory must be new and outside the source checkout. Every copied
file is hashed and compared. The external manifest records all included and omitted
files, exact sizes and hashes. The default conservative budget is 1,000,000,000 bytes;
going over it fails preparation. More than 90% emits a capacity warning. Download
compression does not count as published-site storage savings.

## Deployment remains a separate step

The existing branch-based Pages deployment uses `.nojekyll` and publishes source
directly. Running this script alone does not change that deployment. Do not remove
`.nojekyll` or enable Jekyll merely to exclude screenshots. An authenticated hosting
change is required to publish the prepared artifact through GitHub Actions. Preserve
the custom domain, access level and HTTPS settings. Before switching, wire the
complete existing validators and this byte-preserving packager ahead of deploy,
verify the exact commit and successful Pages result, and review representative
national, Victoria and Redlands map loading, selection, text routes and fallbacks.
Until then this is preparation only. Keep the current live deployment untouched.

## Capacity and growth

At base commit `3bf2aac97eecf20377ce9cacde3a28627705eda5`, tracked files total
1,104,798,054 bytes. The QA raster candidates total 114,929,603 bytes before linked
screenshots are retained. Even removing every candidate would leave 989,868,451
bytes. This is useful housekeeping, not durable headroom for a large expansion.

Do not delete the plain GeoJSON duplicates: current loaders really use them as
fallbacks. A later lossless delivery change needs browser compatibility and failure
tests, exact decoded-coordinate/hash equality, preserved licence and source records,
and corresponding contract evidence. Geometry simplification is not required.
Dedicated static-asset hosting can separate large immutable geometry and videos
from the page build, but it needs an explicit hosting decision and cache/CORS checks.

Public committee and inquiry directories can remain lightweight incremental static
records with source links, dates and status history. A real members area needs a
separate authenticated application and private data store: hiding public Pages
files behind JavaScript is not access control. Constitution collaboration may use
public read-only versions with a separate permissioned editing service. No such
features, services, accounts or payments are implemented by this packaging change.
