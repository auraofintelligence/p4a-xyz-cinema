# Reproducible browser checks

Prepared 7 November 2026. This is a reusable test setup, not a source review or a publication receipt.

## Where the browser runs

`.github/workflows/civic-browser-checks.yml` installs a pinned Playwright release and its full Chromium build in headed mode under an Xvfb virtual display on a standard GitHub-hosted Ubuntu runner. The runner serves the exact checked-out candidate with the existing `scripts/serve.mjs`. It does not use a developer's computer, installed Codex browser, saved profile, or sign-in. The test code and setup are versioned with the project, so a desktop-app update does not replace them. Dependency and runner changes still require review; no setup can guarantee that every future external service or browser change will work unchanged.

The workflow has read-only repository permission, uses commit-pinned actions, does not persist checkout credentials, and cannot push, merge, deploy, refresh source dates, or approve its own evidence. It uses no new service account or stored secret. GitHub may require its normal repository Actions permission. It runs on relevant pushes and pull requests, and can be started manually with a repository-relative scope file after the workflow is on the default branch.

## Routine election refresh

1. Preserve pending work and start a candidate branch from the current remote revision. Perform the existing source and structural checks. Do not push unreviewed changes to the publication branch to obtain a browser preview.
2. Extend `tools/browser-qa/smoke-scope.json`, or add a dedicated scope file, with every changed rendered behavior and representative affected dependency. Use actual delivered HTML and the specific expected state. Include 390 px, 680 px and desktop viewports. The default smoke scope is a regression starting point, not all-place or whole-site certification.
3. Commit only the authorized candidate and tests to its branch. The browser job tests that branch's exact commit, not the current public site. Manual dispatch can select a reviewed scope file. Inputs are file paths, not shell commands.
4. Read the workflow conclusion and download its `civic-browser-<commit>-<attempt>` artifact. Inspect the report's checkout commit, file hashes, assertion results, blocked/request failures and limitations. An artifact upload is not a browser pass, and an automated pass is not a visual review.
5. Actually inspect the screenshots at all declared widths. Review text readability, map alignment, controls, clipping and the affected journey. Record a separate dated visual review with exact screenshots and findings. Rerun affected tests after any later candidate changes.
6. Only after the actual applicable browser, source, editorial and other acceptance checks pass, preserve the reviewed evidence and update `content/places/qa/browser-review.json` under the existing contract. Keep old reviews at their real dates. The runner deliberately does not write this file or mark visual review complete.
7. Run the normal contract builder and aggregate checks. Publication and live verification remain separate authorized steps. The current Pages process is not automatically gated by this test workflow, so the existing pre-publication review remains necessary.

The CI artifacts expire after seven days. Retain the small, relevant reviewed report and required screenshots before expiry if they will be used as durable acceptance evidence. Do not commit the entire artifact bundle or unused screenshots: preserve the site's storage limits and existing evidence conventions. Local output `browser-qa-results/` is ignored.

## Local commands on a browser-capable authorized Linux machine

```sh
python -m pip install -r tools/browser-qa/requirements.txt
python -m playwright install --with-deps --no-shell chromium
node scripts/serve.mjs
# In another terminal:
xvfb-run -a python -B tools/browser-qa/run.py --scope tools/browser-qa/smoke-scope.json --output browser-qa-results
```

The authoritative CI startup and invocation are in the workflow. Pure configuration/provenance unit tests do not require a browser:

```sh
python -B -m unittest discover -s tests -p 'test_browser_qa*.py'
```

Do not retry denied browser launches, change sandbox/network security, publish temporary previews, or reinterpret historical evidence to get around an execution restriction. Use a permitted browser-capable runner and report its actual outcome. If workflow creation, installation, launch or artifact retrieval is blocked, retain the prepared changes and identify that exact failed stage.

## Remaining acceptance scope

The browser job is not an election commission or source verifier. It cannot certify current political facts, every council/electorate journey, physical touchscreen behavior, all accessibility needs or untested layouts. The repository's [build acceptance](council-build-acceptance.md), [fractal update guide](fractal-election-updates.md) and [evidence maintenance](national-validation-maintenance.md) remain authoritative. Do not weaken their gates because a convenient automated smoke test passed.

References: [Playwright Python CI](https://playwright.dev/python/docs/ci), [GitHub Actions billing and usage](https://docs.github.com/en/actions/concepts/billing-and-usage).

The Chromium channel runs with [Playwright's documented headed Linux CI setup](https://playwright.dev/python/docs/ci#running-headed), rather than its separate reduced headless shell. Xvfb supplies an isolated virtual display on the CI runner, not access to a user's desktop. Browser-channel, display mode and version details are recorded in every result.
