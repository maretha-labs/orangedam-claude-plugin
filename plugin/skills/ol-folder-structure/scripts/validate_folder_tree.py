#!/usr/bin/env python3
"""Validate an OrangeDAM Folder Structure CSV.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 validate_folder_tree.py <folders.csv> [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

LEVEL_COLS = ("Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6")
MAX_ASSETS_PER_FOLDER = 50000
WARN_ASSETS_PER_FOLDER = 40000


def validate_folder_tree(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    seen_paths: dict[tuple[str, ...], int] = {}
    ancestors: list[str] = [""] * len(LEVEL_COLS)

    if not path.is_file():
        return {"status": "fail", "folder_count": 0, "errors": [f"File not found: {path}"], "warnings": []}

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for idx, raw in enumerate(rows, start=2):
        row = {k.strip(): (v or "").strip() for k, v in raw.items() if k is not None}
        levels = [row.get(col, "") for col in LEVEL_COLS]
        populated = [i for i, val in enumerate(levels) if val]
        if not populated:
            continue

        deepest = max(populated)
        if len(populated) == 1:
            for p_idx in range(deepest):
                if not ancestors[p_idx]:
                    errors.append(
                        f"Row {idx}: folder '{levels[deepest]}' at Level {deepest + 1} skips missing Level {p_idx + 1} parent."
                    )
            ancestors[deepest] = levels[deepest]
            for c_idx in range(deepest + 1, len(ancestors)):
                ancestors[c_idx] = ""
            full_path = tuple(ancestors[: deepest + 1])
        else:
            for k in range(deepest + 1):
                if not levels[k]:
                    errors.append(
                        f"Row {idx}: folder '{levels[deepest]}' skips empty Level {k + 1}."
                    )
                else:
                    ancestors[k] = levels[k]
            for c_idx in range(deepest + 1, len(ancestors)):
                ancestors[c_idx] = ""
            full_path = tuple(levels[: deepest + 1])

        norm_path = tuple(p.lower() for p in full_path)
        if norm_path in seen_paths:
            errors.append(
                f"Row {idx}: duplicate folder path '{' / '.join(full_path)}' (first seen on row {seen_paths[norm_path]})."
            )
        seen_paths[norm_path] = idx

        if deepest >= 5:
            warnings.append(
                f"Row {idx} ('{' / '.join(full_path)}'): folder depth {deepest + 1} is deep; consider using metadata/Tags instead of deep nesting."
            )

        proj_raw = row.get("Projected Asset Count") or row.get("Asset Count") or ""
        if proj_raw:
            cleaned = proj_raw.replace(",", "")
            if not cleaned.isdigit():
                warnings.append(f"Row {idx} ('{' / '.join(full_path)}'): non-numeric Projected Asset Count '{proj_raw}'.")
            else:
                count = int(cleaned)
                if count > MAX_ASSETS_PER_FOLDER:
                    errors.append(
                        f"Row {idx} ('{' / '.join(full_path)}'): projected {count:,} assets exceeds OrangeDAM's 50,000-asset per-folder limit; partition into child folders."
                    )
                elif count >= WARN_ASSETS_PER_FOLDER:
                    warnings.append(
                        f"Row {idx} ('{' / '.join(full_path)}'): projected {count:,} assets approaches the 50,000-asset per-folder ceiling; plan sub-folder partitioning."
                    )

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "folder_count": len(seen_paths), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OrangeDAM Folder Structure CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validate_folder_tree(args.csv_path)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Folder Tree Validation: {res['status'].upper()} ({res['folder_count']} folders)")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
