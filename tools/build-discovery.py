"""Build voluntary crawl/discovery guides from reviewed public routes and dates.

This does not change the project's licence, refresh source facts, or publish files.
Call build() after rebuilding content/site-page-inventory.json.
"""
from collections import OrderedDict
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote
import xml.etree.ElementTree as ET
from page_review_register import reviewed_page_entries


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://p4a.xyz"
INVENTORY = "content/site-page-inventory.json"
REGISTER = "content/history/civic-page-review-register-2026-10-17.json"
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
EXCLUSIONS = ("/qa/", "/content/", "/tools/", "/scripts/", "/backend/")
GROUPS = OrderedDict([
    ("start", ("Start and find your bearings", "Introductions and readable ways into the workbench.")),
    ("places", ("Maps and places", "Find a state, council or electorate; keep their responsibilities distinct.")),
    ("councils-national", ("Councils and local electoral areas", "Sourced local-government places, actual subdivisions, public representation and election records.")),
    ("state-electorates", ("State and territory electorates", "Actual districts, upper-house regions and statewide chambers with their dated source editions.")),
    ("federal-electorates", ("Federal divisions and Senate representation", "House divisions and Senate state/territory context; current office and previous contestants remain distinct.")),
    ("redland", ("Redlands: the local journey", "Follow a place or question through evidence, systems, public records, participation and outcomes.")),
    ("divisions", ("Redlands: ten divisions", "Local orientation, exact division boundaries and connected questions.")),
    ("policies", ("Everyday questions and policy ideas", "Inspect public concerns, evidence and proposed responses.")),
    ("twinkles", ("Twinkles", "One scene, one gripe, one spoken breath, followed by deeper context.")),
    ("systems", ("Systems and shared possibilities", "Connect local questions to wider civic, economic and information systems.")),
    ("tools", ("Build, contribute and take part", "Guides and browser-local drafting tools; check each tool's own scope.")),
    ("culture", ("Origins, music and imagination", "Stories, lyric meanings and ideas behind the project.")),
    ("support", ("Support and design", "Support options, gear and visual experiments.")),
    ("state-rooms", ("State and territory rooms", "Portals, histories and rulebooks, including Victoria's existing atlas and election guide.")),
])


def canonical(path):
    """Use one explicit public URL for each inventory route."""
    return ORIGIN + ("/" if path == "index.html" else "/" + quote(path, safe="/.-_~"))


def public_inventory(root=ROOT):
    data = json.loads((root / INVENTORY).read_text(encoding="utf-8"))
    pages = data["pages"]
    paths = [row["path"] for row in pages]
    if len(paths) != len(set(paths)) or data["pageCount"] != len(paths):
        raise ValueError("The public route inventory has a duplicate or incorrect count")
    for row in pages:
        path = row["path"]
        parts = PurePosixPath(path).parts
        if (path.startswith("/") or ".." in parts or "\\" in path
                or "?" in path or "#" in path or not path.endswith(".html")
                or not (path == "index.html" or parts[0] in ("pages", "states"))):
            raise ValueError("Not an explicit public HTML route: " + path)
        if not (root / path).is_file():
            raise ValueError("Public route does not exist: " + path)
        if row["navigationGroup"] not in GROUPS:
            raise ValueError("Review the new navigation group: " + row["navigationGroup"])
    return data


def reviewed_dates(root=ROOT):
    """Implementation lastmod dates, never inferred from mtime or a build clock."""
    rows = reviewed_page_entries(root)
    dates = {}
    for row in rows:
        value = row["lastUpdated"]
        if date.fromisoformat(value).isoformat() != value:
            raise ValueError("Expected an explicit ISO date: " + value)
        if row["path"] in dates:
            raise ValueError("Repeated page in the review register: " + row["path"])
        dates[row["path"]] = value
    return dates


class Description(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.value = ""

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag.lower() == "meta" and attrs.get("name", "").lower() == "description":
            self.value = attrs.get("content", "")


def concise_description(root, row):
    parser = Description()
    parser.feed((root / row["path"]).read_text(encoding="utf-8"))
    value = re.sub(r"\s+", " ", parser.value).strip()
    if len(value) > 240:
        value = value[:237].rsplit(" ", 1)[0] + "…"
    return value or GROUPS[row["navigationGroup"]][1]


def markdown_label(value):
    return re.sub(r"\s+", " ", value).strip().replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def render_robots():
    lines = [
        "# P4A discovery directions - reviewed 17 October 2026.",
        "# Existing Strange But True Public Source Licence and third-party rights remain unchanged:",
        "# https://p4a.xyz/LICENCE.md",
        "# Cooperative crawl directions do not enforce copyright or guarantee indexing.",
        "# Search discovery grants no additional reuse or AI-training permission.",
        "",
    ]
    for agent in ("*", "OAI-SearchBot"):
        lines.append("User-agent: " + agent)
        # Named groups do not inherit the wildcard group's exclusions.
        lines.extend("Disallow: " + path for path in EXCLUSIONS)
        lines += ["Allow: /", ""]
    lines += [
        "# Separate request for this identified foundation-model training crawler.",
        "User-agent: GPTBot", "Disallow: /", "",
        "Sitemap: https://p4a.xyz/sitemap.xml", "",
    ]
    return "\n".join(lines)


def render_sitemap(pages, dates):
    ET.register_namespace("", SITEMAP_NS)
    tree = ET.Element("{" + SITEMAP_NS + "}urlset")
    for row in pages:
        node = ET.SubElement(tree, "{" + SITEMAP_NS + "}url")
        ET.SubElement(node, "{" + SITEMAP_NS + "}loc").text = canonical(row["path"])
        if row["path"] in dates:
            ET.SubElement(node, "{" + SITEMAP_NS + "}lastmod").text = dates[row["path"]]
    ET.indent(tree, space="  ")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(tree, encoding="unicode") + "\n"


def render_llms(root, inventory):
    lines = [
        "# P4A civic workbench",
        "",
        "> A roots-up public journey from places and everyday questions to evidence, public decisions, shared possibilities and meaningful participation.",
        "",
        "Canonical website: https://p4a.xyz/",
        "Repository: https://github.com/auraofintelligence/p4a-xyz-cinema",
        "Discovery guide reviewed: 17 October 2026, Australia/Brisbane. Page and source dates remain separate.",
        "",
        "Copyright (c) 2026 Luke Nathan Hayes / Strange But True / Aura of Intelligence. Original material remains governed by the existing Strange But True Public Source Licence. Third-party maps, data, libraries and other material retain their own rights and attribution. This voluntary guide grants no additional reuse or AI-training permission and does not guarantee crawling or indexing.",
        "",
        "This is a static public workbench and proposal archive. P4A is a proposed movement and drafting project, not a registered political party. An example, countdown, reflection or profile is not evidence of an announced candidacy, accepted nomination, operating civic database or official authority. Follow each page's status, sources and uncertainty; do not infer private intentions.",
        "",
        "## Ownership, status and source dates",
        "",
        "- [Strange But True Public Source Licence](https://p4a.xyz/LICENCE.md): Existing permissions, restrictions and required attribution; this guide does not amend them.",
        "- [Human-readable site map](https://p4a.xyz/pages/site-map.html): Search the public pages by purpose.",
        "- [XML sitemap](https://p4a.xyz/sitemap.xml): One canonical URL for every inventoried public HTML page.",
        "- [Sources and page review register](https://p4a.xyz/states/qld/councils/redland/sources/index.html#review-register): Separate implementation updates, source observations and review triggers.",
        "- [Agent entry rules](https://p4a.xyz/AGENTS.md): Read the separate council, state or federal guide before extending the pattern.",
        "",
        "## Follow a thread",
        "",
        "Start with the national place directory, choose a state or territory, then councils, state electorates or federal representation. Search or select an actual area, inspect it and Open its dedicated page. Redlands retains the fuller local journey with divisions, questions, systems, people, participation and outcomes. Keep three accounts together: what it cost, what was given freely, and what changed. Verified freely given hours are counted once, with no fixed dollar conversion.",
        "",
        "The national place pages supply sourced maps, dated public representation, election events and available historical contestants. Individual source coverage remains explicit on each page and in the canonical records; do not infer completeness from a route count. Victoria retains its deeper atlas, Census comparisons and 2026 election guide. Current and next-election boundary editions remain distinct. New local Twinkles are left to grassroots implementation. Do not assume that Queensland's rules, boundaries, dates or division structures apply elsewhere.",
        "",
        "Twinkles begin with one ordinary scene, one everyday gripe and one self-contained spoken breath. Read the serious context and evidence beneath the seed. Public voting records need the exact motion; a stated reason needs an attributable source, and an inferred explanation must remain labelled.",
        "",
        "## Complete public page directory",
        "",
        f"{len(inventory['pages'])} public HTML routes, grouped by purpose. Canonical content mirrors, scripts, QA and backend source are not separate public pages. Links describe the existing archive; they do not certify every proposal or refresh its facts.",
    ]
    for key, (title, purpose) in GROUPS.items():
        rows = [row for row in inventory["pages"] if row["navigationGroup"] == key]
        if key == "divisions":
            rows.sort(key=lambda row: int(row["path"].split("/")[-2]))
        if key == "redland":
            flow = ["index.html", "divisions/index.html", "explore/index.html", "possibilities/index.html", "candidates/index.html", "elections/index.html", "action/index.html", "outcomes/index.html", "sources/index.html"]
            rows.sort(key=lambda row: flow.index(row["path"].split("states/qld/councils/redland/")[1]) if row["path"].split("states/qld/councils/redland/")[1] in flow else len(flow))
        lines += ["", "### " + title, "", purpose, ""]
        for row in rows:
            lines.append(f"- [{markdown_label(row['title'])}]({canonical(row['path'])}): {concise_description(root, row)}")
    return "\n".join(lines) + "\n"


def build(root=ROOT):
    """Write only the three root discovery files, with no clock-derived dates."""
    root = Path(root)
    inventory = public_inventory(root)
    dates = reviewed_dates(root)
    known = {row["path"] for row in inventory["pages"]}
    if set(dates) - known:
        raise ValueError("Review register includes a route missing from the public inventory")
    files = {
        "robots.txt": render_robots(),
        "sitemap.xml": render_sitemap(inventory["pages"], dates),
        "llms.txt": render_llms(root, inventory),
    }
    for name, body in files.items():
        with (root / name).open("w", encoding="utf-8", newline="\n") as output:
            output.write(body)
    return {"publicPages": len(inventory["pages"]), "evidencedLastmodDates": len(dates), "files": list(files)}


if __name__ == "__main__":
    print("Built discovery guides: " + json.dumps(build(), ensure_ascii=False))
