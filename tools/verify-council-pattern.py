"""Validate a declared civic-place journey without network calls or writes.

The historical filename is retained for councils. The manifest may describe a
council, ward/division, state district, federal electorate or another civic
place. No jurisdiction, route, council count or number of children is built in.
Run: python tools/verify-council-pattern.py --manifest PATH --json

A PASS checks the declared snapshot. It does not certify legal correctness,
source freshness, an explanation of someone's motive, visual quality or humour.
Those require the dated human/browser reviews reported separately below.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date, datetime
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import struct
import sys
from urllib.parse import unquote, urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = "content/local/council-pattern-contract.json"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def pointer(value, path=""):
    """Read a JSON Pointer; missing values are errors, never invented defaults."""
    if not path:
        return value
    if not path.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {path}")
    for key in path[1:].split("/"):
        key = key.replace("~1", "/").replace("~0", "~")
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


def text_present(value):
    return isinstance(value, str) and bool(value.strip())


def selected_values(value, selector, location=""):
    """Inventory explicit source dates, with '*' only for declared arrays/maps."""
    if not selector:
        return [(location or "/", value)]
    if not selector.startswith("/"):
        raise ValueError("Inventory selector must be a JSON Pointer")
    key, _, remaining = selector[1:].partition("/")
    tail = "/" + remaining if remaining else ""
    if key == "*":
        pairs = enumerate(value) if isinstance(value, list) else value.items()
        return [item for child_key, child in pairs for item in selected_values(child, tail, location + "/" + str(child_key))]
    key = key.replace("~1", "/").replace("~0", "~")
    return selected_values(value[int(key)] if isinstance(value, list) else value[key], tail, location + "/" + key)


def http_url(value):
    parts = urlsplit(value) if isinstance(value, str) else None
    return bool(parts and parts.scheme in {"http", "https"} and parts.netloc)


class Page(HTMLParser):
    """Small static DOM inventory; it deliberately does not execute JavaScript."""
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.elements = []
        self.stack = []
        self.ids = Counter()
        self.links = []
        self.title = ""
        self.headings = []
        self.feed(path.read_text(encoding="utf-8-sig"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        item = {"tag": tag, "attrs": attrs, "parent": self.stack[-1] if self.stack else None, "text": ""}
        index = len(self.elements)
        self.elements.append(item)
        if attrs.get("id"):
            self.ids[attrs["id"]] += 1
        for key in ("href", "src", "data"):
            if attrs.get(key) and (key != "data" or tag == "object"):
                self.links.append((tag, attrs, attrs[key]))
        if tag not in VOID:
            self.stack.append(index)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for offset in range(len(self.stack) - 1, -1, -1):
            if self.elements[self.stack[offset]]["tag"] == tag:
                del self.stack[offset:]
                break

    def handle_data(self, value):
        for index in self.stack:
            self.elements[index]["text"] += value

    def beneath(self, element, ancestor):
        index = element["parent"]
        while index is not None:
            if index == ancestor:
                return True
            index = self.elements[index]["parent"]
        return False

    def select(self, tag=None, attribute=None, value=None, css_class=None, within=None):
        result = []
        for index, element in enumerate(self.elements):
            attrs = element["attrs"]
            if tag and element["tag"] != tag:
                continue
            if attribute and (attribute not in attrs or (value is not None and attrs[attribute] != value)):
                continue
            if css_class and css_class not in attrs.get("class", "").split():
                continue
            if within is not None and index != within and not self.beneath(element, within):
                continue
            result.append((index, element))
        return result


class Validator:
    def __init__(self, manifest, root=ROOT):
        self.root = Path(root).resolve()
        self.manifest = manifest
        self.errors = []
        self.warnings = []
        self.pages = {}
        self.payloads = {}
        self.counts = Counter()

    def error(self, code, message):
        self.errors.append({"code": code, "message": message})

    def check(self, condition, code, message):
        if not condition:
            self.error(code, message)
        return bool(condition)

    def path(self, relative):
        result = (self.root / relative).resolve()
        result.relative_to(self.root)  # Never inspect a manifest path outside this repository.
        return result

    def read(self, relative):
        return json.loads(self.path(relative).read_text(encoding="utf-8-sig"))

    def page(self, path):
        if path not in self.pages:
            self.pages[path] = Page(path)
        return self.pages[path]

    def local_target(self, origin, href):
        value = urlsplit(href)
        if value.scheme or value.netloc:
            return None
        path = (self.root / unquote(value.path).lstrip("/")) if value.path.startswith("/") else (origin.parent / unquote(value.path)) if value.path else origin
        path = path.resolve()
        path.relative_to(self.root)
        return (path / "index.html" if path.is_dir() else path), unquote(value.fragment)

    def reference(self, origin, href):
        target = self.local_target(origin, href)
        if target is None:
            return
        path, fragment = target
        self.counts["localReferences"] += 1
        if not self.check(path.is_file(), "missing-local-target", f"{origin.relative_to(self.root)} -> {href}"):
            return
        if fragment and path.suffix.lower() == ".html":
            self.check(fragment in self.page(path).ids, "missing-anchor", f"{origin.relative_to(self.root)} -> {href}")

    def require_fields(self, item, fields, label):
        for field in fields:
            self.check(field in item and item[field] not in (None, "", [], {}), "missing-field", f"{label}: {field}")

    def iso_date(self, value, label):
        try:
            date.fromisoformat(value)
            return True
        except (ValueError, TypeError):
            self.error("invalid-date", f"{label}: expected an explicit ISO date, got {value!r}")
            return False

    def run_section(self, label, callback, entry):
        try:
            callback(entry)
        except (OSError, ValueError, TypeError, KeyError, IndexError, json.JSONDecodeError) as error:
            self.error("invalid-" + label, str(error))

    def verify_route(self, entry):
        entry = {**self.manifest.get("routeDefaults", {}), **entry}
        path = self.path(entry["path"])
        page = self.page(path)
        self.counts["routes"] += 1
        for identifier, count in page.ids.items():
            self.check(count == 1, "duplicate-id", f"{entry['path']}: {identifier} appears {count} times")
        for tag in ("title", "h1"):
            self.check(any(text_present(e["text"]) for _, e in page.select(tag=tag)), "unreadable-route", f"{entry['path']}: missing readable {tag}")
        if entry.get("noSvgMaps", True):
            self.check(not page.select(tag="svg"), "svg-map", f"{entry['path']}: inline SVG is forbidden in this declared journey")
            for tag, attrs, href in page.links:
                if tag in {"img", "object", "embed", "source", "image"}:
                    self.check(not urlsplit(href).path.lower().endswith(".svg") and not href.lower().startswith("data:image/svg"), "svg-map", f"{entry['path']}: SVG image/map {href}")
        for _, _, href in page.links:
            self.reference(path, href)
        targets = {self.local_target(path, element["attrs"]["href"])[0] for _, element in page.select(tag="a", attribute="href") if self.local_target(path, element["attrs"]["href"]) is not None}
        for target in entry.get("requiredNextPaths", []):
            self.check(self.path(target) in targets, "missing-next-path", f"{entry['path']}: needs a visible link to {target}")
        if entry.get("breadcrumbClass"):
            crumbs = page.select(tag="nav", css_class=entry["breadcrumbClass"])
            self.check(bool(crumbs), "missing-breadcrumbs", f"{entry['path']}: no labelled breadcrumb navigation")
            if crumbs:
                index, crumb = crumbs[0]
                self.check(text_present(crumb["attrs"].get("aria-label")), "missing-breadcrumbs", f"{entry['path']}: breadcrumb needs aria-label")
                self.check(bool(page.select(tag="a", within=index)), "missing-breadcrumbs", f"{entry['path']}: breadcrumb needs a working ancestor link")
        if entry.get("choicesClass"):
            choices = page.select(css_class=entry["choicesClass"])
            links = [element for index, _ in choices for _, element in page.select(tag="a", within=index) if text_present(element["text"])]
            self.check(len(links) >= entry.get("minimumChoices", 2), "missing-choices", f"{entry['path']}: too few readable journey choices")
        for stamp in entry.get("visibleDateValues", []):
            self.check(bool(page.select(tag="time", attribute="datetime", value=stamp)), "missing-visible-date", f"{entry['path']}: missing time datetime={stamp}")
        if entry.get("privateNoteGuard"):
            self.check(bool(page.select(tag="fieldset", attribute=entry["privateNoteGuard"])) and any("disabled" in item["attrs"] for _, item in page.select(tag="fieldset", attribute=entry["privateNoteGuard"])), "privacy-guard", f"{entry['path']}: private note must stay disabled until its JS handler is attached")

    def verify_map(self, entry):
        entry = {**self.manifest.get("mapDefaults", {}), **entry}
        page = self.page(self.path(entry["path"]))
        roots = page.select(attribute="id", value=entry["id"])
        if not self.check(len(roots) == 1, "map-root", f"{entry['path']}: map {entry['id']} must occur once"):
            return
        index, _ = roots[0]
        canvases = page.select(tag="canvas", within=index)
        self.check(len(canvases) == 1, "map-canvas", f"{entry['path']}: exactly one Canvas per declared map")
        if "totalCanvasCount" in entry:
            self.check(len(page.select(tag="canvas")) == entry["totalCanvasCount"], "duplicate-overview-map", f"{entry['path']}: wrong total Canvas count")
        if "staticImageCount" in entry:
            self.check(len(page.select(tag="img")) == entry["staticImageCount"], "duplicate-overview-map", f"{entry['path']}: unexpected static image alongside the interactive map")
        for _, canvas in canvases:
            self.check(text_present(canvas["attrs"].get("aria-label")) and canvas["attrs"].get("tabindex") == "0", "map-accessibility", f"{entry['path']}: Canvas needs a label and keyboard focus")
        for attribute in entry["requiredAttributes"]:
            self.check(bool(page.select(attribute=attribute, within=index)), "map-control", f"{entry['path']}: missing {attribute}")
        for _, search in page.select(tag="input", attribute=entry["searchAttribute"], within=index):
            self.check(bool(search["attrs"].get("id")) and bool(page.select(tag="label", attribute="for", value=search["attrs"].get("id"), within=index)), "map-search-label", f"{entry['path']}: search needs a matching visible label")
        scripts = [self.local_target(page.path, e["attrs"]["src"])[0] for _, e in page.select(tag="script", attribute="src") if self.local_target(page.path, e["attrs"]["src"]) is not None]
        layers = {layer["id"]: layer for layer in self.manifest.get("boundaryLayers", [])}
        self.check(entry["layer"] in layers, "map-layer", f"{entry['path']}: selected boundary layer is not declared")
        if entry["layer"] in layers:
            self.check(self.path(layers[entry["layer"]]["deliveryFile"]) in scripts, "map-layer", f"{entry['path']}: declared boundary layer is not loaded")
        for script in entry["scripts"]:
            self.check(scripts.count(self.path(script)) == 1, "map-script", f"{entry['path']}: include {script} exactly once")
        self.counts["interactiveMaps"] += 1

    def verify_boundary(self, entry):
        source = self.read(entry["sourceRecord"])
        self.require_fields(source, entry["sourceFields"], entry["id"] + " boundary provenance")
        geometry = pointer(source, entry.get("geometryPointer", "/geometry"))
        raw_path = self.path(geometry["file"])
        raw_bytes = raw_path.read_bytes()
        self.check(hashlib.sha256(raw_bytes).hexdigest() == geometry["sha256"], "boundary-hash", f"{entry['id']}: original response checksum changed")
        raw = json.loads(raw_bytes.decode("utf-8-sig"))
        js = self.path(entry["deliveryFile"]).read_text(encoding="utf-8-sig")
        marker = entry["assignment"] + "="
        self.check(js.count(marker) == 1, "delivery-assignment", f"{entry['id']}: expected one JSON assignment {marker}")
        delivered, consumed = json.JSONDecoder().raw_decode(js.split(marker, 1)[1].lstrip())
        self.check(js.split(marker, 1)[1].lstrip()[consumed:].strip() in {"", ";"}, "delivery-tail", f"{entry['id']}: data script must contain only the declared JSON after its assignment")
        self.payloads[entry["id"]] = delivered
        self.check(raw["type"] == delivered["type"] == "FeatureCollection", "boundary-format", f"{entry['id']}: requires a FeatureCollection")
        self.check([f["geometry"] for f in raw["features"]] == [f["geometry"] for f in delivered["features"]], "changed-boundary-coordinates", f"{entry['id']}: delivered source coordinates, rings, holes, order or parts differ")
        count = len(raw["features"])
        self.check(count == geometry["featureCount"] == entry["expectedFeatureCount"], "boundary-count", f"{entry['id']}: declared/source/delivered counts differ")
        identifiers = [str(f["properties"][entry["deliveryIdentifier"]]) for f in delivered["features"]]
        self.check(len(identifiers) == len(set(identifiers)), "boundary-identifiers", f"{entry['id']}: duplicate identifiers")
        if "expectedIdentifiers" in entry:
            self.check(set(identifiers) == set(map(str, entry["expectedIdentifiers"])), "boundary-identifiers", f"{entry['id']}: identifiers differ from this source-specific contract")
        for feature in raw["features"]:
            shape = feature["geometry"]
            self.check(shape["type"] in {"Polygon", "MultiPolygon"}, "boundary-shape", f"{entry['id']}: unsupported geometry")
            polygons = [shape["coordinates"]] if shape["type"] == "Polygon" else shape["coordinates"]
            for polygon in polygons:
                for ring in polygon:
                    self.check(len(ring) >= 4 and ring[0] == ring[-1], "boundary-ring", f"{entry['id']}: invalid or unclosed ring")
                    self.check(all(len(p) >= 2 and all(isinstance(v, (float, int)) and math.isfinite(v) for v in p[:2]) for p in ring), "boundary-coordinate", f"{entry['id']}: non-finite coordinate")
        for source_item in source.get("sources", []):
            self.require_fields(source_item, ["title", "url"], entry["id"] + " source")
            self.check(http_url(source_item["url"]), "source-url", f"{entry['id']}: source URL must link to its publisher")
        self.counts["boundaryLayers"] += 1
        self.counts["sourceFeatures"] += count

    def verify_basemap(self, entry):
        source = self.read(entry["sourceRecord"])
        image = pointer(source, entry.get("pointer", ""))
        self.require_fields(image, ["image", "sha256", "extent", "attribution", "request", "exportResponse"], entry["id"])
        self.require_fields(source, ["sourceChecked", "retrieved", "publisher", "licence", "licenceURL", "freshnessNote"], entry["id"] + " provenance")
        content = self.path(image["image"]).read_bytes()
        self.check(content.startswith(b"\x89PNG\r\n\x1a\n"), "basemap-png", f"{entry['id']}: geographic base must be an actual PNG")
        self.check(hashlib.sha256(content).hexdigest() == image["sha256"], "basemap-hash", f"{entry['id']}: raster checksum changed")
        self.check(struct.unpack(">II", content[16:24]) == (image["width"], image["height"]), "basemap-dimensions", f"{entry['id']}: PNG dimensions differ")
        response = self.read(image["exportResponse"])
        extent = image["extent"]
        for field in ("xmin", "ymin", "xmax", "ymax"):
            self.check(extent[field] == response["extent"][field], "basemap-registration", f"{entry['id']}: must use actual returned {field}, not requested bbox")
        self.check(extent["xmin"] < extent["xmax"] and extent["ymin"] < extent["ymax"], "basemap-registration", f"{entry['id']}: invalid extent")
        self.check(extent["spatialReference"]["wkid"] == entry["projection"], "basemap-projection", f"{entry['id']}: stored projection differs")
        response_sr = response["extent"]["spatialReference"]
        self.check(entry["projection"] in {response_sr.get("wkid"), response_sr.get("latestWkid")}, "basemap-projection", f"{entry['id']}: returned projection differs")
        for layer_id in entry["deliveredInLayers"]:
            delivered = pointer(self.payloads[layer_id], entry["deliveryPointer"])
            for field in ("image", "extent", "attribution"):
                self.check(delivered[field] == image[field], "basemap-delivery", f"{entry['id']}: {layer_id} changed {field}")
        self.counts["basemaps"] += 1

    def verify_records(self, entry):
        document = self.read(entry["path"])
        records = pointer(document, entry.get("recordsPointer", "/records"))
        ids = [r["id"] for r in records]
        self.check(bool(ids) and len(ids) == len(set(ids)), "record-identifiers", f"{entry['path']}: records must have distinct stable IDs")
        self.require_fields(document, entry["documentFields"], entry["path"])
        if entry.get("editorialBasisPointer"):
            basis = pointer(document, entry["editorialBasisPointer"])
            self.require_fields(basis, ["source", "credibilitySource", "reviewed", "rules", "status"], "Twinkle editorial basis")
            self.iso_date(basis["reviewed"], "Twinkle editorial review")
            for field in ("source", "credibilitySource"):
                self.reference(self.root / "index.html", basis[field])
        page = self.page(self.path(entry["renderedPath"]))
        twinkles = []
        for record in records:
            label = f"{entry['path']} {record['id']}"
            self.require_fields(record, entry["recordFields"], label)
            self.check(set(record["trinity"]) == {"cost", "free", "change"} and all(text_present(v) for v in record["trinity"].values()), "record-trinity", label + ": keep all three accounts, including explicit unknowns")
            for related in record["related"]:
                self.check(related in ids, "related-record", label + f": unresolved related ID {related}")
            for next_item in record["next"]:
                self.require_fields(next_item, ["label", "href"], label + " next path")
                self.reference(self.root / "index.html", next_item["href"])
            for source in record["sources"]:
                self.require_fields(source, entry["sourceFields"], label + " source")
                self.iso_date(source[entry["sourceDateField"]], label + " source check")
                self.reference(self.root / "index.html", source["url"])
            self.iso_date(record[entry["recordDateField"]], label + " editorial date")
            if record["type"] == entry["twinkleType"]:
                twinkles.append(record)
                self.require_fields(record, entry["twinkleFields"], label + " Twinkle")
                self.check(len(record["summary"].split()) <= entry["seedWordBudget"], "twinkle-seed-length", label + ": exceeds this manifest's editorial review budget; shorten the seed or document human review")
                self.check(record["presentation"] in entry["presentations"], "twinkle-presentation", label + ": missing comic/quiet-care choice")
                self.check(record["id"] in page.ids, "twinkle-rendering", label + ": no direct, shareable rendered record")
        self.check(len(page.select(css_class=entry["renderedTwinkleClass"])) == len(twinkles), "twinkle-rendering", "Rendered Twinkle count differs from canonical records")
        self.counts["records"] += len(records)
        self.counts["twinkles"] += len(twinkles)

    def verify_catalogue(self, entry):
        data = self.read(entry["path"])
        self.require_fields(data, entry["documentFields"], entry["path"])
        sources = {s["id"]: s for s in data["sources"]}
        self.check(len(sources) == len(data["sources"]), "source-identifiers", entry["path"] + ": duplicate source IDs")
        for source in sources.values():
            self.require_fields(source, entry["sourceFields"], source["id"])
            self.iso_date(source[entry["sourceDateField"]], source["id"])
            self.check(http_url(source["url"]), "source-url", source["id"] + ": missing publisher URL")
        for item in data.get("indicators", []):
            self.require_fields(item, ["id", "label", "unit", "period", "geography", "sourceId", entry["sourceDateField"]], "statistical indicator")
            self.check("value" in item, "indicator-value", item["id"] + ": missing value (null is an explicit unknown)")
            self.check(item["sourceId"] in sources, "indicator-source", item["id"] + ": unresolved source")
            self.iso_date(item[entry["sourceDateField"]], item["id"])
        for item in data.get("maps", []):
            self.require_fields(item, ["id", "image", "attribution", "rights", "edition", "sourceUrl"], "source map")
            self.check(self.path(item["image"]).is_file() and not item["image"].lower().endswith(".svg"), "source-map", item["id"] + ": missing raster source")
        self.counts["indicators"] += len(data.get("indicators", []))
        self.counts["sourceMapRecords"] += len(data.get("maps", []))

    def verify_representatives(self, entry):
        data = self.read(entry["path"])
        sources = {s["id"]: s for s in data["sources"]}
        for source in sources.values():
            self.require_fields(source, ["title", "url", "checked", "supports"], "representation source")
            self.iso_date(source["checked"], source["id"])
        for item in pointer(data, entry["recordsPointer"]):
            representative = pointer(item, entry["representativePointer"])
            self.require_fields(representative, entry["fields"], "public representative")
            self.iso_date(representative[entry["dateField"]], "representative listing check")
            self.check(http_url(representative["url"]) and representative["sourceId"] in sources, "representative-source", "Representative needs a dated public source and profile link")
            if entry.get("localRouteTemplate"):
                path = entry["localRouteTemplate"].format(id=item["id"])
                self.check(self.path(path).is_file(), "representative-route", f"Missing declared sub-place route {path}")
            self.counts["representativeListings"] += 1

    def verify_election(self, entry):
        data = self.read(entry["path"])
        self.require_fields(data, ["timezone", "checked", "changed", "refreshTriggers"], entry["path"])
        self.iso_date(data["checked"], "election source checked")
        self.iso_date(data["changed"], "election data changed")
        timezone = ZoneInfo(data["timezone"])
        for pointer_path in entry["eventPointers"]:
            event = pointer(data, pointer_path)
            self.require_fields(event, ["status", "source"], pointer_path)
            self.check(http_url(event["source"]), "election-source", pointer_path + ": requires official source link")
            if event.get("date"):
                self.iso_date(event["date"], pointer_path)
            if event.get("countdownTarget"):
                target = datetime.fromisoformat(event["countdownTarget"])
                self.check(target.tzinfo is not None, "election-timezone", pointer_path + ": countdown must have an explicit UTC offset")
                if target.tzinfo:
                    self.check(target.date().isoformat() == event["date"] and target.utcoffset() == target.astimezone(timezone).utcoffset(), "election-timezone", pointer_path + ": target differs from the declared local date/timezone")
                self.require_fields(event, ["dateBasis"], pointer_path)
            if not event.get("date"):
                self.check(not event.get("countdownTarget"), "invented-election-clock", pointer_path + ": unannounced date must not have an active target")
                for field in entry.get("conditionalEarlyDateFields", []):
                    self.check(not event.get(field), "invented-early-voting", pointer_path + f": {field} must stay absent until officially sourced")
        for pointer_path in entry["earlyVotingPointers"]:
            early = pointer(data, pointer_path)
            self.require_fields(early, ["status", "source"], pointer_path)
            opens, closes = early.get("opens"), early.get("closes")
            self.check(bool(opens) == bool(closes), "early-voting-window", pointer_path + ": both dates must be absent or both sourced")
            if opens and closes:
                start, finish = datetime.fromisoformat(opens), datetime.fromisoformat(closes)
                self.check(start.tzinfo is not None and finish.tzinfo is not None and start < finish, "early-voting-window", pointer_path + ": ordered timezone-aware opening/closing required")
                self.check(bool(early.get("locations")) and http_url(early["source"]), "early-voting-source", pointer_path + ": published voting locations and source required")
            else:
                self.check(not early.get("locations"), "invented-early-voting", pointer_path + ": no invented locations before timetable publication")
        self.counts["electionSnapshots"] += 1

    def verify_date_pin(self, entry):
        actual = pointer(self.read(entry["path"]), entry["pointer"])
        self.check(actual == entry["expected"], "source-date-drift", f"{entry['path']}{entry['pointer']}: changed from explicitly reviewed {entry['expected']!r}; investigate, then update the manifest deliberately")

    def verify_date_inventory(self, entry):
        data = self.read(entry["path"])
        inventory = sorted(item for selector in entry["selectors"] for item in selected_values(data, selector))
        self.check(bool(inventory), "empty-date-inventory", entry["path"])
        for location, value in inventory:
            self.iso_date(value, entry["path"] + location)
        digest = hashlib.sha256(json.dumps(inventory, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
        self.check(digest == entry["sha256"], "source-date-inventory-drift", entry["path"] + ": an inventoried source/editorial date changed; investigate and document real checks before deliberately updating the inventory")

    def verify_evidence(self, entry):
        self.iso_date(entry["reviewedOn"], "recorded evidence date")
        for path in entry["paths"]:
            self.check(self.path(path).is_file(), "missing-review-evidence", path)
        for artifact in entry["artifactFingerprints"]:
            actual = hashlib.sha256(self.path(artifact["path"]).read_bytes()).hexdigest()
            self.check(actual == artifact["sha256"], "review-evidence-stale", artifact["path"] + ": changed since this evidence binding; repeat the affected browser review and record the new evidence before updating its fingerprint")
        if entry.get("layoutEvidence"):
            results = self.read(entry["layoutEvidence"])
            for row in results:
                label = row["page"]
                self.check(row["scrollWidth"] <= row["viewport"], "recorded-horizontal-overflow", label)
                self.check(row["buttonOverlaps"] == 0, "recorded-control-overlap", label)
                if "picking" in row:
                    picks = json.loads(row["picking"]) if isinstance(row["picking"], str) else row["picking"]
                    self.check(picks["result"] == "PASS" and bool(picks["picking"]) and all(str(item["actual"]) == str(item["expected"]) for item in picks["picking"]), "recorded-map-picking", label)
        self.check(bool(entry["requiredHumanChecks"]) and bool(entry["limitations"]), "review-scope", "Manual review must declare its required checks and limits")

    def run(self):
        self.check(self.manifest.get("schemaVersion") == 1, "manifest-version", "Unsupported civic-place contract schemaVersion")
        self.run_section("place", lambda entry: self.require_fields(entry, ["id", "kind", "name", "jurisdiction"], "place"), self.manifest["place"])
        self.check(bool(self.manifest.get("routes")), "empty-scope", "Declare the civic-place routes; an empty scope cannot pass")
        for name, callback in (("routes", self.verify_route), ("maps", self.verify_map), ("boundaryLayers", self.verify_boundary), ("basemaps", self.verify_basemap), ("recordSets", self.verify_records), ("catalogues", self.verify_catalogue), ("representativeSets", self.verify_representatives), ("elections", self.verify_election), ("datePins", self.verify_date_pin), ("dateInventories", self.verify_date_inventory)):
            for entry in self.manifest.get(name, []):
                self.run_section(name, callback, entry)
        self.run_section("evidence", self.verify_evidence, self.manifest["reviewEvidence"])
        self.warnings.extend(self.manifest["reviewEvidence"]["limitations"])
        return {"result": "FAIL" if self.errors else "PASS", "scope": "Declared static civic-place snapshot; offline, read-only", "place": self.manifest["place"], "counts": dict(self.counts), "errors": self.errors, "warnings": self.warnings, "reviewEvidence": {"reviewedOn": self.manifest["reviewEvidence"]["reviewedOn"], "status": "Dated evidence exists; this run does not repeat browser/editorial/source review", "requiredHumanChecks": self.manifest["reviewEvidence"]["requiredHumanChecks"]}, "doesNotProve": ["External sources are still current or correct", "A legal interpretation or election scenario is correct", "The map looks right or works on a physical touch device", "Twinkle humour, kindness, relevance or a one-breath spoken delivery", "A recorded vote establishes motive, popularity or public support", "Undeclared pages, data or journeys meet this contract"]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=DEFAULT_MANIFEST, help="Repository-relative or absolute civic-place contract JSON")
    parser.add_argument("--json", action="store_true", help="Print machine-readable output")
    args = parser.parse_args(argv)
    try:
        candidate = Path(args.manifest)
        manifest_path = candidate if candidate.is_absolute() else ROOT / candidate
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        report = Validator(manifest).run()
    except (OSError, ValueError, TypeError, KeyError, ZoneInfoNotFoundError) as error:
        report = {"result": "FAIL", "errors": [{"code": "manifest-error", "message": str(error)}]}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Civic place acceptance: {report['result']}")
        if "counts" in report:
            print(", ".join(f"{key}: {value}" for key, value in report["counts"].items()))
        for error in report["errors"]:
            print(f"ERROR [{error['code']}] {error['message']}")
        if "reviewEvidence" in report:
            print(f"Recorded review: {report['reviewEvidence']['reviewedOn']}; machine checks do not replace the listed human reviews.")
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
