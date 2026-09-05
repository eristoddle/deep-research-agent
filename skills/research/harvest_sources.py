#!/usr/bin/env python3
"""Tally which sources supported fields across research runs.

Read-only. Scans every result file under a research root (or a single named
run), classifies each run as `captured` (at least one result carries a
`sources` array), `no-capture` (none does — the run predates source
capture, PLAN.md D17), or `no-results` (never researched; not the same
thing, and never reported as predating capture), and tallies each distinct source URL by how many
runs it appears in and how many of those runs it actually supported a
field in. A URL that clears both counts is a promotion candidate for
`/research-harvest` to write into `CANDIDATES.md`; the judgment of which
module it belongs to, and whether to promote it at all, stays with the
skill and the human reading its output — this script only counts.

No PyYAML dependency: `outline.yaml`'s `execution.output_dir` is read with
a line-oriented scan for the single `output_dir:` key, failing soft to
`results`, per LAYOUT.md.

Exit codes: 0 ok, 2 usage/input error.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

DEFAULT_OUTPUT_DIR = "results"
NEAR_MISS_CAP = 20
FIELD_NAME_CAP = 12
SKIPPED_FILE_CAP = 20

_OUTPUT_DIR_RE = re.compile(r'^\s*output_dir:\s*(.+?)\s*(#.*)?$')


def read_output_dir(outline_path):
    """Line-oriented read of `execution.output_dir`. Fails soft to 'results'."""
    try:
        with outline_path.open(encoding="utf-8") as f:
            for line in f:
                m = _OUTPUT_DIR_RE.match(line)
                if m:
                    value = m.group(1).strip().strip("'\"")
                    if value:
                        return value
    except OSError:
        pass
    return DEFAULT_OUTPUT_DIR


def discover_runs(root_path):
    """Run folders one and two levels deep under root, per LAYOUT.md's rule."""
    found = set()
    for pattern in ("*/outline.yaml", "*/*/outline.yaml"):
        for outline in root_path.glob(pattern):
            found.add(outline.parent.resolve())
    return sorted(found)


def normalize_url(raw_url):
    """Strip a trailing '/' and lowercase scheme+host; leave the path case alone."""
    parts = urlsplit(raw_url)
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return urlunsplit((scheme, netloc, path, parts.query, parts.fragment))


def scan_run(run_dir, label):
    """Scan one run's results directory. Returns a dict of tallies plus skip info."""
    output_dir_name = read_output_dir(run_dir / "outline.yaml")
    results_dir = run_dir / output_dir_name

    captured = False
    skipped_files = []  # list of (relpath, reason)
    malformed_count = 0
    # url -> {"sources": set(names), "fields": set(names) [only from field-support entries]}
    urls = {}

    json_paths = sorted(results_dir.glob("*.json")) if results_dir.is_dir() else []
    if not json_paths:
        # Never researched, or researched somewhere this script was not pointed at.
        # Not the same as `no-capture`, and must never be reported as predating
        # source capture — that is the one distinction this script exists to make.
        return {
            "state": "no-results",
            "skipped_files": skipped_files,
            "malformed_count": malformed_count,
            "urls": urls,
        }

    for json_path in json_paths:
        rel = f"{label}/{output_dir_name}/{json_path.name}"
        try:
            text = json_path.read_text(encoding="utf-8")
            data = json.loads(text)
        except (OSError, json.JSONDecodeError):
            skipped_files.append((rel, "not valid JSON"))
            continue
        if not isinstance(data, dict):
            skipped_files.append((rel, "not a JSON object"))
            continue

        sources = data.get("sources")
        if "sources" in data:
            captured = True
        if not isinstance(sources, list):
            continue

        for entry in sources:
            if not isinstance(entry, dict) or "url" not in entry:
                malformed_count += 1
                continue
            fields = entry.get("fields", [])
            if not isinstance(fields, list):
                malformed_count += 1
                continue
            url = normalize_url(str(entry["url"]))
            source_name = entry.get("source", "")
            rec = urls.setdefault(url, {"sources": set(), "runs": set(), "field_runs": set(), "fields": set()})
            if source_name:
                rec["sources"].add(source_name)
            rec["runs"].add(label)
            if fields:
                rec["field_runs"].add(label)
                rec["fields"].update(str(f) for f in fields)

    return {
        "state": "captured" if captured else "no-capture",
        "skipped_files": skipped_files,
        "malformed_count": malformed_count,
        "urls": urls,
    }


def merge(all_urls, run_urls):
    for url, rec in run_urls.items():
        target = all_urls.setdefault(url, {"sources": set(), "runs": set(), "field_runs": set(), "fields": set()})
        target["sources"] |= rec["sources"]
        target["runs"] |= rec["runs"]
        target["field_runs"] |= rec["field_runs"]
        target["fields"] |= rec["fields"]


def format_fields(fields):
    names = sorted(fields)
    shown = names[:FIELD_NAME_CAP]
    suffix = f" (+{len(names) - FIELD_NAME_CAP} more)" if len(names) > FIELD_NAME_CAP else ""
    return f"{len(names)}: {', '.join(shown)}{suffix}" if names else "0: (none)"


def print_entry(url, rec):
    sources = ", ".join(sorted(rec["sources"])) or "(unnamed)"
    print(f"- {url}")
    print(f"    source(s): {sources}")
    print(f"    runs: {len(rec['runs'])} (field-support: {len(rec['field_runs'])})")
    print(f"    seen in: {', '.join(sorted(rec['runs']))}")
    print(f"    fields ({format_fields(rec['fields'])})")


def main():
    parser = argparse.ArgumentParser(
        description="Tally which sources supported fields across research runs (read-only)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--root", type=str, help="research root; scan every run beneath it")
    group.add_argument("--run", type=str, help="one run folder")
    parser.add_argument("--min-runs", type=int, default=3, help="minimum distinct runs a URL must appear in (default 3)")
    parser.add_argument(
        "--min-field-runs", type=int, default=2,
        help="minimum distinct runs where the URL's fields were non-empty (default 2)",
    )
    args = parser.parse_args()

    if args.min_runs <= 0 or args.min_field_runs <= 0:
        parser.error("--min-runs and --min-field-runs must be positive integers")

    if args.root:
        root_path = Path(args.root)
        if not root_path.is_dir():
            print(f"[ERROR] root not found: {root_path}", file=sys.stderr)
            sys.exit(2)
        run_dirs = discover_runs(root_path)
        labels = {d: str(d.relative_to(root_path.resolve())) for d in run_dirs}
    else:
        run_path = Path(args.run).resolve()
        if not (run_path / "outline.yaml").exists():
            print(f"[ERROR] not a run folder (no outline.yaml): {run_path}", file=sys.stderr)
            sys.exit(2)
        run_dirs = [run_path]
        labels = {run_path: run_path.name}

    if not run_dirs:
        print("No run folders found (looked for outline.yaml one and two levels deep).")
        sys.exit(0)

    captured_count = 0
    no_capture_count = 0
    no_results_count = 0
    all_skipped = []
    total_malformed = 0
    all_urls = {}

    for run_dir in run_dirs:
        label = labels[run_dir]
        result = scan_run(run_dir, label)
        if result["state"] == "captured":
            captured_count += 1
        elif result["state"] == "no-capture":
            no_capture_count += 1
        else:
            no_results_count += 1
        all_skipped.extend(result["skipped_files"])
        total_malformed += result["malformed_count"]
        merge(all_urls, result["urls"])

    total_runs = len(run_dirs)
    print(
        f"Scan: {total_runs} run(s) scanned ({captured_count} captured / {no_capture_count} no-capture / "
        f"{no_results_count} no results yet), {len(all_skipped)} file(s) skipped"
    )
    if all_skipped:
        for rel, reason in all_skipped[:SKIPPED_FILE_CAP]:
            print(f"  skipped: {rel} ({reason})")
        if len(all_skipped) > SKIPPED_FILE_CAP:
            print(f"  ... and {len(all_skipped) - SKIPPED_FILE_CAP} more")
    if total_malformed:
        print(f"{total_malformed} malformed source entries skipped")

    candidates = []
    near_misses = []
    for url, rec in all_urls.items():
        run_count = len(rec["runs"])
        field_count = len(rec["field_runs"])
        if run_count >= args.min_runs and field_count >= args.min_field_runs:
            candidates.append((url, rec))
        elif run_count > 1:
            near_misses.append((url, rec))

    candidates.sort(key=lambda kv: (-len(kv[1]["runs"]), -len(kv[1]["field_runs"]), kv[0]))
    near_misses.sort(key=lambda kv: (-len(kv[1]["runs"]), -len(kv[1]["field_runs"]), kv[0]))

    print()
    if candidates:
        print(f"## Candidates (>= {args.min_runs} runs, field-support in >= {args.min_field_runs})")
        for url, rec in candidates:
            print_entry(url, rec)
    elif no_results_count == total_runs:
        print("No candidates: no run here has been researched yet — nothing has produced results to read.")
    elif no_capture_count == total_runs:
        print("No candidates: these runs predate source capture.")
    elif captured_count == total_runs:
        print("No candidates: sources were captured and none reached the threshold.")
    else:
        parts = ["No candidates."]
        if captured_count:
            parts.append(f"{captured_count} run(s): sources were captured and none reached the threshold.")
        if no_capture_count:
            parts.append(f"{no_capture_count} run(s): these runs predate source capture.")
        if no_results_count:
            parts.append(f"{no_results_count} run(s): not researched yet, no results to read.")
        print(" ".join(parts))

    print()
    if near_misses:
        print("## Near-misses (appeared in more than one run, below threshold)")
        for url, rec in near_misses[:NEAR_MISS_CAP]:
            print_entry(url, rec)
        if len(near_misses) > NEAR_MISS_CAP:
            print(f"... and {len(near_misses) - NEAR_MISS_CAP} more")


if __name__ == "__main__":
    main()
