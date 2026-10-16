"""Check public discovery coverage, crawl requests and unchanged licence rights."""
from datetime import date
import hashlib
import importlib.util
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlparse
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
# Git's LF checkout and the original Windows CRLF copy have identical text.
# Accept only these two reviewed byte sequences; never rewrite the licence here.
LICENCE_SHA256 = {
    "4d41a7bdffbf8daac0ad9847d2f6a2857444b770c0d0312acea592cc9eadb009",
    "84027220f6bc7d69f5a3d2a091f32d0576ee24d5368beabee599399881fd80ac",
}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def verify(root=ROOT):
    inventory = json.loads((root / "content/site-page-inventory.json").read_text(encoding="utf-8"))
    paths = [row["path"] for row in inventory["pages"]]
    expected = {"https://p4a.xyz/" if path == "index.html" else "https://p4a.xyz/" + quote(path, safe="/.-_~") for path in paths}
    check(len(paths) == len(set(paths)) == inventory["pageCount"], "Inventory count or uniqueness differs")
    actual = {"index.html"} | {path.relative_to(root).as_posix() for folder in ("pages", "states") for path in (root/folder).rglob("*.html")}
    check(set(paths) == actual, "Public HTML routes changed; rebuild the human sitemap and discovery files")
    check((root/"pages/site-map.html").read_bytes() == (root/"content/rooms/site-map.html").read_bytes(), "Human sitemap source and public copy differ")

    register = json.loads((root / "content/history/civic-page-review-register-2026-10-17.json").read_text(encoding="utf-8"))
    dates = {row["path"]: row["lastUpdated"] for group in register["pageGroups"] for row in group["pages"]}
    dates.update({row["path"]: row["lastUpdated"] for row in register["updatedExistingPages"]})
    check(set(dates) <= set(paths), "A review-register path is missing from the inventory")

    tree = ET.fromstring((root / "sitemap.xml").read_text(encoding="utf-8"))
    check(tree.tag == "{" + NS["sm"] + "}urlset", "Sitemap namespace/root is incorrect")
    nodes = tree.findall("sm:url", NS)
    urls = [node.findtext("sm:loc", namespaces=NS) for node in nodes]
    check(len(urls) == len(set(urls)) and set(urls) == expected, "Sitemap must cover exactly the public inventory once")
    check(len(nodes) == len(tree), "Sitemap contains unexpected root elements")
    timestamp_count = 0
    for node, url in zip(nodes, urls):
        parsed = urlparse(url)
        check(parsed.scheme == "https" and parsed.netloc == "p4a.xyz" and not parsed.query and not parsed.fragment, "Sitemap URL is not a canonical public URL: " + url)
        path = "index.html" if parsed.path == "/" else unquote(parsed.path.lstrip("/"))
        check(path in paths and (root / path).is_file(), "Sitemap URL has no existing inventoried page: " + url)
        check(not path.startswith(("content/", "qa/", "tools/", "scripts/", "backend/")), "Nonpublic mirror/source in sitemap")
        lastmods = node.findall("sm:lastmod", NS)
        check(len(lastmods) <= 1, "Repeated lastmod")
        if lastmods:
            value = lastmods[0].text
            check(path in dates and dates[path] == value, "Lastmod lacks exact review-register evidence: " + path)
            check(date.fromisoformat(value).isoformat() == value, "Lastmod is not an ISO date")
            timestamp_count += 1
        else:
            check(path not in dates, "An explicitly reviewed page has lost its lastmod: " + path)
        check(all(child.tag in ("{" + NS["sm"] + "}loc", "{" + NS["sm"] + "}lastmod") for child in node), "Unexpected sitemap fields")

    robots_text = (root / "robots.txt").read_text(encoding="utf-8")
    robots = RobotFileParser()
    robots.parse(robots_text.splitlines())
    check(robots.site_maps() == ["https://p4a.xyz/sitemap.xml"], "robots.txt does not declare the canonical sitemap")
    for agent in ("Googlebot", "bingbot", "OAI-SearchBot"):
        for url in expected:
            check(robots.can_fetch(agent, url), agent + " cannot discover public page: " + url)
        for prefix in ("qa", "content", "tools", "scripts", "backend"):
            check(not robots.can_fetch(agent, "https://p4a.xyz/" + prefix + "/example"), agent + " lost a source/QA exclusion")
        check(robots.can_fetch(agent, "https://p4a.xyz/LICENCE.md"), "Licence must remain discoverable")
        check(robots.can_fetch(agent, "https://p4a.xyz/docs/agents/council-journey-rules.md"), "Public agent documentation must remain discoverable")
    for path in ("/", "/pages/site-map.html", "/states/qld/councils/redland/index.html", "/LICENCE.md"):
        check(not robots.can_fetch("GPTBot", "https://p4a.xyz" + path), "GPTBot training crawl request must be disallowed")
    check("User-agent: OAI-SearchBot" in robots_text and "User-agent: GPTBot" in robots_text, "Search and training requests are not separate")

    llms = (root / "llms.txt").read_text(encoding="utf-8")
    check("voluntary guide grants no additional reuse or AI-training permission" in llms, "llms.txt needs its no-additional-permission statement")
    check("does not guarantee crawling or indexing" in llms, "llms.txt must not promise indexing")
    check("Third-party maps, data, libraries and other material retain their own rights and attribution" in llms, "Third-party rights statement missing")
    check("https://p4a.xyz/LICENCE.md" in llms, "Existing licence link missing")
    check("static public workbench" in llms and "not a registered political party" in llms, "Public prototype status missing")
    check("is not evidence of an announced candidacy" in llms, "Candidacy status must not be inferred")
    directory = llms.split("## Complete public page directory\n", 1)[1]
    directory_urls = re.findall(r"^- \[[^\n]*\]\((https://p4a\.xyz/[^)\s]*)\):", directory, re.M)
    check(len(directory_urls) == len(set(directory_urls)) and set(directory_urls) == expected, "llms.txt directory must cover each public route exactly once")
    check(hashlib.sha256((root / "LICENCE.md").read_bytes()).hexdigest() in LICENCE_SHA256, "LICENCE.md changed; stop and review rights before preparing an upload")

    spec = importlib.util.spec_from_file_location("p4a_discovery_build", root / "tools/build-discovery.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    check(robots_text == module.render_robots(), "robots.txt differs from its repeatable generator")
    check((root / "sitemap.xml").read_text(encoding="utf-8") == module.render_sitemap(inventory["pages"], dates), "sitemap.xml differs from its repeatable generator")
    check(llms == module.render_llms(root, inventory), "llms.txt is stale against the inventoried pages")
    return {"publicPages": len(urls), "evidencedLastmodDates": timestamp_count, "searchAndTrainingRequests": "separate", "licence": "unchanged"}


if __name__ == "__main__":
    print("Discovery checks passed: " + json.dumps(verify(), ensure_ascii=False))
