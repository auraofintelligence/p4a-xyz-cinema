# Search discovery and existing rights

Added and reviewed 17 October 2026, Australia/Brisbane. Prepared locally for the existing custom domain `p4a.xyz`; these files do not change the live site until uploaded.

## What each file does

| File | Purpose |
| --- | --- |
| `pages/site-map.html` | Readable, searchable navigation grouped by what a person wants to do. |
| `content/site-page-inventory.json` | Actual public HTML routes, generated from the site tree; source mirrors and QA are not separate public pages. |
| `sitemap.xml` | The same public routes as absolute `https://p4a.xyz/` URLs. A `lastmod` appears only where an explicit reviewed implementation date supports it. |
| `robots.txt` | Origin-root crawl directions: welcome general search and OAI-SearchBot; separately request that GPTBot does not crawl for foundation-model training. |
| `llms.txt` | A voluntary proposed discovery format: a plain-language guide to the journey, page links, source dates and existing rights. It is not a grant of rights or a binding instruction for another system. |

The **Strange But True Public Source Licence** in [LICENCE.md](../LICENCE.md) remains unchanged. The original Windows CRLF copy has SHA-256 `4d41a7bdffbf8daac0ad9847d2f6a2857444b770c0d0312acea592cc9eadb009`; Git's LF checkout of the same text has SHA-256 `84027220f6bc7d69f5a3d2a091f32d0576ee24d5368beabee599399881fd80ac`. The validator accepts only these two known byte sequences, so Windows/Linux checkout line endings do not create a false licence-change failure. It never rewrites the file. Third-party maps, electoral boundaries, statistics and other material retain their own terms. Discovery does not grant additional reuse, commercial use, institutional use or AI-training permission. The licence itself remains the authority for its permissions and restrictions.

Crawl directions depend on a crawler's cooperation. They are not access controls or copyright enforcement, and no indexing or ranking is promised. The explicit GPTBot opt-out is specific to that crawler; it must not be described as blocking every AI collector.

## Recent repository examples used

- [Aura Genesis Protocol README](https://github.com/auraofintelligence/aura-genesis-geode-atlas#readme): the 16 October 2026 discovery documentation, linked guide and automated checks.
- [Aura Genesis llms.txt](https://github.com/auraofintelligence/aura-genesis-geode-atlas/blob/main/llms.txt): human entry points, source/status distinctions and explicit preservation of rights.
- [Account-root robots.txt](https://github.com/auraofintelligence/auraofintelligence.github.io/blob/main/robots.txt) and [root-policy merge snippet](https://github.com/auraofintelligence/aura-genesis-geode-atlas/blob/main/.github/robots-root-snippet.txt): separate search/training rules. A project subdirectory cannot set the shared origin's effective policy. P4A's custom domain uses its own root file directly.

The locally checked examples informed this implementation; future remote versions may change independently.

## Repeatable maintenance

1. Add, retire or revise the actual public page and its reviewed content first. Preserve source observation/check dates separately from implementation dates.
2. Record supported page update dates in the review register. Do not label every page freshly updated merely because a shared build ran.
3. Run `python tools/build-human-site-map.py`. It regenerates both human directory copies, the route inventory and the three discovery files. `python tools/build-discovery.py` can rebuild only the discovery files from the current inventory.
4. Run `python tools/verify-discovery.py`, plus applicable place and browser checks. The GitHub civic-place workflow runs the discovery check too.
5. Prepare the source bundle using `scripts/prepare-github-upload.py`. Preserve the existing licence, custom domain and third-party attributions.

Review when routes, custom domain, publication scope, supported update dates, crawler identifiers/policies, the llms proposal or licence terms change. A deliberate future licence revision requires an explicit reviewed change to the baseline check; never update the hash simply to make an unexplained modification pass. There is no automatic monitoring.

## Primary format references

- [Google: robots.txt introduction](https://developers.google.com/search/docs/crawling-indexing/robots/intro) — root location, crawl scope and limitations.
- [Google: building a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap) — absolute preferred URLs, accurate significant-update dates and no indexing guarantee.
- [OpenAI: crawler documentation](https://developers.openai.com/api/docs/bots) — independent OAI-SearchBot search and GPTBot training controls.
- [llms.txt proposal](https://llmstxt.org/) — a proposed guide format rather than an adopted universal crawler standard.

References checked 17 October 2026. The checked format documentation does not alter this repository's licence.
