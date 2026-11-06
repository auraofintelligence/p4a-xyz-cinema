"""Prepare a byte-preserving Pages tree without unreferenced QA screenshots.

This is not the public-source archive and does not publish or change Pages settings.
Only tracked files are considered. All maps, fallback formats, source/licence records,
QA reports, and any screenshot named by retained text stay byte-for-byte unchanged.
Run validators in the complete checkout before packaging, not in the reduced tree.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCREENSHOT_ROOT = "tools/publication-qa/"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".mjs", ".json", ".md", ".txt", ".xml", ".svg", ".webmanifest"}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def tracked_files(root):
    result = subprocess.check_output(["git", "ls-files", "--stage", "-z"], cwd=root)
    paths = []
    for entry in result.decode("utf-8").split("\0"):
        if not entry:
            continue
        metadata, name = entry.split("\t", 1)
        mode, _, stage = metadata.split()
        path = PurePosixPath(name)
        if mode not in {"100644", "100755"} or stage != "0":
            raise ValueError(f"Unsupported or unresolved tracked entry: {name}")
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(f"Unsafe tracked path: {name}")
        local = root / name
        if local.is_symlink() or not local.is_file() or not local.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Missing or unsafe tracked file: {name}")
        paths.append(name)
    return sorted(paths)


def plan(root, paths):
    tracked = set(paths)
    candidates = {
        name for name in paths
        if (name.startswith(SCREENSHOT_ROOT) and PurePosixPath(name).suffix.lower() in IMAGE_SUFFIXES)
        or (name.startswith("assets/") and not name.startswith(("assets/maps/", "assets/media/"))
            and PurePosixPath(name).suffix.lower() in {".png", ".jpg", ".jpeg"}
            and str(PurePosixPath(name).with_suffix(".webp")) in tracked)
    }
    # Basename matching deliberately errs toward retention. It protects relative,
    # absolute, root-relative and report references, including ambiguous basenames.
    by_basename = {}
    for name in candidates:
        by_basename.setdefault(PurePosixPath(name).name, []).append(name)
    expression = re.compile("|".join(re.escape(name) for name in sorted(by_basename, key=len, reverse=True))) if by_basename else None
    referenced = {}
    if expression:
        for name in paths:
            if name in candidates or PurePosixPath(name).suffix.lower() not in TEXT_SUFFIXES:
                continue
            from urllib.parse import unquote
            text = unquote(html.unescape((root / name).read_text(encoding="utf-8-sig")))
            text = re.sub(r"\\u([0-9a-fA-F]{4})|\\x([0-9a-fA-F]{2})", lambda match: chr(int(match.group(1) or match.group(2), 16)), text)
            if PurePosixPath(name).suffix.lower() in {".json", ".webmanifest"}:
                # Decode escaped JSON strings without executing content.
                text += "\n" + json.dumps(json.loads((root / name).read_text(encoding="utf-8-sig")), ensure_ascii=False)
            # A runtime may construct a filename. If a visitor-facing script,
            # stylesheet or page mentions the QA directory at all, retain every
            # candidate rather than pretending literal-name checks are enough.
            if PurePosixPath(name).suffix.lower() in {".html", ".htm", ".css", ".js", ".mjs", ".svg"} and "publication-qa" in text:
                for target in candidates:
                    referenced.setdefault(target, set()).add(name)
            # JSON/JS may escape separators, but the actual basename is unchanged.
            for match in expression.finditer(text):
                for target in by_basename[match.group()]:
                    referenced.setdefault(target, set()).add(name)
    omitted = sorted(candidates - referenced.keys())
    included = sorted(set(paths) - set(omitted))
    assert all(name in included for name in paths if name.startswith("assets/maps/"))
    return included, omitted, {name: sorted(refs) for name, refs in sorted(referenced.items())}


def build(root, paths, output=None):
    included, omitted, referenced = plan(root, paths)
    output = output.resolve() if output else None
    if output:
        if output == root.resolve() or output.is_relative_to(root.resolve()):
            raise ValueError("Keep the artifact outside the source checkout")
        if output.exists():
            raise ValueError("Output must not exist; never overwrite a previous artifact")
        output.mkdir(parents=True)
    entries = []
    for name in included:
        source = root / name
        entry = {"path": name, "bytes": source.stat().st_size, "sha256": digest(source)}
        if output:
            destination = output / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            if digest(destination) != entry["sha256"]:
                raise ValueError(f"Artifact byte mismatch: {name}")
        entries.append(entry)
    excluded = [{"path": name, "bytes": (root / name).stat().st_size, "sha256": digest(root / name)} for name in omitted]
    maps = [entry for entry in entries if entry["path"].startswith("assets/maps/")]
    return {
        "schemaVersion": 1,
        "scope": "Only unreferenced QA rasters and unreferenced non-map, non-media originals with retained WebP counterparts omitted. All other tracked files retained unchanged.",
        "sourceBytes": sum(entry["bytes"] for entry in entries + excluded),
        "artifactBytes": sum(entry["bytes"] for entry in entries),
        "savedBytes": sum(entry["bytes"] for entry in excluded),
        "includedFileCount": len(entries), "omittedScreenshotCount": len(excluded),
        "mapFileCount": len(maps), "mapBytes": sum(entry["bytes"] for entry in maps),
        "mapBytesChanged": False, "sourceFilesDeleted": False, "published": False,
        "copiedAndHashVerified": output is not None,
        "retainedScreenshotReferences": referenced,
        "files": entries, "omittedScreenshots": excluded,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Audit without creating a deployment tree")
    mode.add_argument("--output-dir", type=Path)
    parser.add_argument("--report", required=True, type=Path, help="External JSON manifest, outside source and artifact")
    parser.add_argument("--max-bytes", type=int, default=1_000_000_000, help="Conservative deployment budget, not compressed ZIP size")
    args = parser.parse_args()
    report_path = args.report.resolve()
    if report_path.is_relative_to(ROOT) or (args.output_dir and report_path.is_relative_to(args.output_dir.resolve())):
        parser.error("Keep the manifest outside both source and artifact")
    report = build(ROOT, tracked_files(ROOT), args.output_dir)
    report["commit"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    report["workingTreeDirty"] = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True))
    report["maxBytes"] = args.max_bytes
    report["withinBudget"] = report["artifactBytes"] <= args.max_bytes
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key not in {"files", "omittedScreenshots", "retainedScreenshotReferences"}}, indent=2))
    print(f"Manifest: {report_path}")
    if report["artifactBytes"] > args.max_bytes * .9:
        print("WARNING: artifact exceeds 90% of budget; screenshot savings are not a long-term capacity plan.")
    if not report["withinBudget"]:
        raise SystemExit("Artifact exceeds deployment budget; do not publish it.")


if __name__ == "__main__":
    main()
