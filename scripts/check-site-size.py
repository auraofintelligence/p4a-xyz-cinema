"""Check the uncompressed tracked tree against a conservative Pages size budget."""
from pathlib import Path
import argparse
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def measure(root, names, budget):
    if budget <= 0:
        raise ValueError("The byte budget must be positive")
    entries = []
    for name in names:
        path = root / name
        if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Missing or unsafe tracked file: {name}")
        entries.append({"path": name, "bytes": path.stat().st_size})
    size = sum(entry["bytes"] for entry in entries)
    maps = [entry for entry in entries if entry["path"].startswith("assets/maps/")]
    return {
        "trackedFiles": len(entries), "trackedBytes": size, "budgetBytes": budget,
        "headroomBytes": budget - size, "underBudget": size < budget,
        "mapFiles": len(maps), "mapBytes": sum(entry["bytes"] for entry in maps),
        "largestFiles": sorted(entries, key=lambda entry: entry["bytes"], reverse=True)[:10],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-bytes", type=int, default=1_000_000_000)
    args = parser.parse_args()
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").rstrip("\0").split("\0")
    result = measure(ROOT, [name for name in names if name], args.max_bytes)
    print(json.dumps(result, indent=2))
    if not result["underBudget"]:
        raise SystemExit("Tracked site is not below the deployment budget; review growth before publishing.")
    if result["trackedBytes"] > args.max_bytes * .95:
        print("WARNING: less than 5% headroom remains. Do not treat this cleanup as long-term capacity for major new assets.")


if __name__ == "__main__":
    main()
