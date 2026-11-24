#!/usr/bin/env python3
"""Validate an OrangeDAM hierarchical Tag Tree CSV.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 validate_tag_tree.py <tags.csv> [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

LEVEL_COLS = ("Tag Term Level 0", "Tag Term Level 1", "Tag Term Level 2", "Tag Term Level 3")


def validate_tag_tree(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    seen_paths: dict[tuple[str, ...], int] = {}
    tag_types: set[str] = set()
    active_type = ""
    active_ancestors: list[str] = ["", "", "", ""]

    if not path.is_file():
        return {"status": "fail", "tag_types": [], "term_count": 0, "errors": [f"File not found: {path}"], "warnings": []}

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for idx, raw in enumerate(rows, start=2):
        row = {k.strip(): (v or "") for k, v in raw.items() if k is not None}
        tt_raw = row.get("Tag Type (Category)") or row.get("Tag Type") or ""
        tt = tt_raw.strip()
        if tt:
            if tt != active_type:
                active_type = tt
                active_ancestors = ["", "", "", ""]
            tag_types.add(tt)

        levels = [row.get(col, "") for col in LEVEL_COLS]
        populated = [i for i, val in enumerate(levels) if val.strip()]
        if not populated:
            continue

        if not active_type:
            errors.append(f"Row {idx}: tag term appears before any Tag Type (Category) is specified.")
            continue

        for i in populated:
            raw_val = levels[i]
            val = raw_val.strip()
            if raw_val != val:
                warnings.append(f"Row {idx} ({active_type}): leading/trailing whitespace in term '{raw_val}'.")
            if "|" in val:
                errors.append(f"Row {idx} ({active_type}): term '{val}' contains '|', which conflicts with OrangeDAM CSV multi-value delimiters.")

        # Support both full-path rows (L0, L1, L2 populated together) and indented tree rows (only deepest cell populated)
        deepest = max(populated)
        if len(populated) == 1:
            # Indented style: check all parent levels above deepest exist in active_ancestors
            for parent_idx in range(deepest):
                if not active_ancestors[parent_idx]:
                    errors.append(
                        f"Row {idx} ({active_type}): term '{levels[deepest].strip()}' at Level {deepest} skips missing Level {parent_idx} parent."
                    )
            active_ancestors[deepest] = levels[deepest].strip()
            for child_idx in range(deepest + 1, len(active_ancestors)):
                active_ancestors[child_idx] = ""
            full_path = tuple([active_type] + [active_ancestors[k] for k in range(deepest + 1)])
        else:
            # Full-path style: check no gaps between 0 and deepest
            for k in range(deepest + 1):
                if not levels[k].strip():
                    errors.append(
                        f"Row {idx} ({active_type}): skipped hierarchy level {k} before Level {deepest} ('{levels[deepest].strip()}')."
                    )
                else:
                    active_ancestors[k] = levels[k].strip()
            for child_idx in range(deepest + 1, len(active_ancestors)):
                active_ancestors[child_idx] = ""
            full_path = tuple([active_type] + [levels[k].strip() for k in range(deepest + 1)])

        norm_path = tuple(p.lower() for p in full_path)
        if norm_path in seen_paths:
            errors.append(
                f"Row {idx} ({active_type}): duplicate taxonomy path '{' > '.join(full_path[1:])}' (first seen on row {seen_paths[norm_path]})."
            )
        seen_paths[norm_path] = idx

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {
        "status": status,
        "tag_types": sorted(tag_types),
        "term_count": len(seen_paths),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OrangeDAM Tag Tree CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validate_tag_tree(args.csv_path)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Tag Tree Validation: {res['status'].upper()} ({len(res['tag_types'])} Tag Types, {res['term_count']} terms)")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
