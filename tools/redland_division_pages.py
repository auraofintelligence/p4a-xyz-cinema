"""Build ten small, sourced division journeys using the existing Redlands shell.

No network calls, automatic redating, invented statistics or new services.
The caller may pass build-redland.py's ``shell`` function to build_pages();
standalone use loads that helper without invoking its main() build.
"""
from pathlib import Path
import html
import importlib.util
import json
import os


ROOT = Path(__file__).resolve().parents[1]
BASE = "states/qld/councils/redland/"


def _read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def _escape(value):
    return html.escape(str(value), quote=True)


def _href(page, target):
    if target.startswith(("https://", "http://", "#")):
        return _escape(target)
    path, fragment_marker, fragment = target.lstrip("/").partition("#")
    clean, query_marker, query = path.partition("?")
    result = os.path.relpath(ROOT / clean, (ROOT / page).parent).replace("\\", "/")
    if query_marker:
        result += "?" + query
    if fragment_marker:
        result += "#" + fragment
    return _escape(result)


def _link(page, target, label, css=""):
    external = target.startswith(("https://", "http://"))
    attrs = f' class="{_escape(css)}"' if css else ""
    if external:
        attrs += ' target="_blank" rel="noopener noreferrer"'
    return f'<a href="{_href(page, target)}"{attrs}>{_escape(label)}</a>'


def _card(page, number, title, description, target, label):
    return (
        '<article class="local-card">'
        f'<span class="local-number">{_escape(number)}</span>'
        f'<h3>{_escape(title)}</h3><p>{_escape(description)}</p>'
        + _link(page, target, label, "local-card-link") + '</article>'
    )


def _default_shell():
    """Reuse the established shell, without duplicating branding or building it."""
    spec = importlib.util.spec_from_file_location("redland_shell_helper", ROOT / "tools/build-redland.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.shell


def build_pages(shell_fn=None):
    """Write and return ten {relative_path: HTML} division overview pages.

    ``shell_fn`` has the existing build-redland.py shell signature. Returning
    the outputs also lets the main generator include them in its own checks.
    """
    shell_fn = shell_fn or _default_shell()
    data = _read("content/local/redland-divisions.json")
    records = {record["id"]: record for record in _read("content/local/redland-connections.json")["records"]}
    divisions = data["divisions"]
    if sorted(item["id"] for item in divisions) != list(range(1, 11)):
        raise ValueError("The reviewed Redland division directory must contain exactly divisions 1–10.")
    outputs = {}

    for division in divisions:
        number = division["id"]
        label = division["label"]
        page = BASE + f"divisions/{number}/index.html"
        selected_map = BASE + f"divisions/index.html?division={number}#redland-division-map"
        representative = division["representative"]
        councillor = representative["role"] + " " + representative["name"]
        twinkle_cards = []
        for record_id in division["twinkles"]:
            if record_id not in records:
                raise ValueError(f"Unknown Twinkle {record_id} in {label}")
            record = records[record_id]
            twinkle_cards.append(_card(
                page, "A question to explore", record["title"], record["summary"],
                BASE + "explore/index.html#" + record_id, "Follow this question"
            ))

        body = f'''<section class="local-panel accent" aria-labelledby="selected-place">
<p class="local-kicker">Your selected division</p>
<h2 id="selected-place">{_escape(division['localities'])}</h2>
<p>Use the same map, select and open pattern to keep your bearings. A suburb can cross a division boundary; a locality label is a starting point.</p>
<p>{_link(page, selected_map, 'View ' + label + ' on the interactive map', 'local-button primary')}</p>
<p class="local-source">For an address-specific check, use {_link(page, 'https://www.redland.qld.gov.au/About-Council/Mayor-and-Councillors/Mayor-and-councillor-profiles', "Council’s official division finder")}. The links and public representative listing were checked on <time datetime="2026-10-17">17 October 2026</time>.</p>
</section>
<section class="local-section" aria-labelledby="division-paths">
<p class="local-kicker">A few useful paths</p><h2 id="division-paths">What would you like to follow?</h2>
<div class="local-grid two">
{_card(page, '01', 'An everyday question', 'A broken path, a caring role, a journey or an idea. Bring the place and lived experience together, then follow the evidence.', '#local-questions', 'Explore some starting questions')}
{_card(page, '02', 'People and decisions', 'Find the listed divisional councillor, official records and the decision behind a claim.', '#public-records', 'Inspect the public trail')}
{_card(page, '03', 'A connected system', 'Link a local observation to civic twins, legal sources, chosen contribution and broader possibilities.', BASE + 'possibilities/index.html', 'Connect the local and the wider system')}
{_card(page, '04', 'Maps and statistics', 'Keep the boundary, source period and measure together. See what is known and what still needs a matched division-level source.', '#division-data', 'Check the data and its limits')}
</div></section>
<section class="local-section" id="local-questions"><h2>A question can start here.</h2>
<p>These are suggested entry points into the existing Redlands Twinkles. They are prompts for exploration; the number of residents affected and the priority within this division have not been measured.</p>
<div class="local-grid">{''.join(twinkle_cards)}</div>
<p>{_link(page, BASE + 'explore/index.html', 'Search all local questions and systems')} · {_link(page, BASE + 'action/index.html', 'Prepare your own observation, correction or offer')}</p>
</section>
<section class="local-section" id="public-records"><p class="local-kicker">Public representative and evidence</p>
<h2>{_escape(councillor)}</h2>
<p>Council lists this representative for {_escape(label)}. Read the official profile for contact routes, published background, interests and newsletters where provided. A representative profile is one source; a particular decision still needs its own record.</p>
<p>{_link(page, representative['url'], 'Open the official councillor profile', 'local-button')} {_link(page, data['sources'][0]['url'], 'Check the full current directory', 'local-button')}</p>
<p class="local-source">Source: {_link(page, data['sources'][0]['url'], data['sources'][0]['title'])}. Published listing checked <time datetime="2026-10-17">17 October 2026</time>. Roles and links need another check when conditions change.</p>
<div class="local-grid two">
{_card(page, 'The decision', 'What happened, and who voted?', 'Follow the agenda item, minute, motion and recorded vote where available. A speech or newsletter can add context; it cannot replace the formal decision record.', data['sources'][2]['url'], 'Open official council meeting records')}
{_card(page, 'The explanation', 'What is the evidence for why?', 'Link an explicit public explanation when one exists. Label a plausible interpretation as an interpretation, preserve other explanations and leave motive unknown where evidence is missing.', BASE + 'candidates/index.html', 'Follow the people and evidence pathway')}
</div>
<p>A divisional councillor and the citywide mayor have different electoral constituencies. {_link(page, data['sources'][1]['url'], 'Council’s election guide')} explains the structure. {_link(page, BASE + 'candidates/index.html', 'Election dates and any officially announced by-election')} stay in the shared Redlands election section.</p>
</section>
<section class="local-section" id="division-data"><h2>Keep the number beside its geography.</h2>
<p><strong>{_escape(data['divisionStatistics']['status'])}</strong></p>
<p>A council total is not a division count. An old electoral map’s enrolment figures describe its stated period, rather than the current population. Compare council divisions, state electorates and Bowman as separate geographies before joining their data.</p>
<div class="local-related">{_link(page, selected_map, 'Return to the selected boundary')}{_link(page, BASE + 'sources/index.html#statistics', 'Dated council statistics and ABS links')}{_link(page, BASE + 'sources/index.html#boundaries', 'State and federal boundary sources')}{_link(page, 'content/local/redland-divisions.json', 'Division directory, source dates and update rules')}</div>
</section>
<section class="local-section"><h2>From this place to meaningful change.</h2>
<p>Carry the original question into a civic twin or a legal source trail, compare possible changes, and identify who can agree to the work. The local example connects these proposals; it does not claim they are operating council services.</p>
<div class="local-trinity">
<div><strong>What it cost</strong><p>No division-level project cost is measured here. Keep estimates, actual spending, paid work and future obligations visible when a proposal develops.</p></div>
<div><strong>What was given freely</strong><p>No contributions are claimed by this page. Record chosen time, care, knowledge and resources with consent; count a verified human hour once.</p></div>
<div><strong>What changed</strong><p>No local result is claimed. Choose a baseline, record benefit and harm, and bring observed change back to the people who raised the question.</p></div>
</div>
<div class="local-related">{_link(page, BASE + 'action/index.html', 'Prepare a useful next step')}{_link(page, BASE + 'outcomes/index.html', 'Track delivery, change and learning')}{_link(page, BASE + 'possibilities/index.html', 'Explore wider possibilities')}</div>
</section>
<p class="local-source">Division page added <time datetime="2026-10-17">17 October 2026</time>. {_link(page, 'content/history/redland.md', 'Dated change record')} · {_link(page, 'docs/agents/local-place-pattern.md', 'Carry this pattern to another place')}</p>'''

        title = "Redlands · " + label
        intro = "Your place, local questions, public records and connected possibilities. Follow the same journey one division closer."
        rendered = shell_fn(page, title, intro, body, active='Divisions')
        # Extend the existing breadcrumb instead of introducing a second UI.
        crumb_end = _link(page, BASE + 'index.html', 'Redlands') + '</nav>'
        expanded = (
            _link(page, BASE + 'index.html', 'Redlands') + '<span>/</span>'
            + _link(page, BASE + 'divisions/index.html', 'Divisions')
            + '<span>/</span><span aria-current="page">' + _escape(label) + '</span></nav>'
        )
        if crumb_end not in rendered:
            raise ValueError("Existing Redlands breadcrumb changed; review division integration.")
        rendered = rendered.replace(crumb_end, expanded, 1)
        # These pages were first created today; do not inherit the earlier
        # council page's first-build date as their own creation date.
        rendered = rendered.replace('Started 16 October · Updated ', 'Added 17 October · Reviewed ')
        output = ROOT / page
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered + '\n', encoding='utf-8')
        outputs[page] = rendered

    print(f"Generated {len(outputs)} Redland division pages. Representative listings checked 2026-10-17; division statistics remain unfilled.")
    return outputs


if __name__ == '__main__':
    build_pages()
