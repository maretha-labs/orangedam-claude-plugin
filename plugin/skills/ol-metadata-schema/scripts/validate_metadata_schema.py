#!/usr/bin/env python3
"""Validate an OrangeDAM Metadata Fields specification CSV.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 validate_metadata_schema.py <metadata_fields.csv> [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

VALID_FIELD_TYPES = {
    "Text - Fewer than 500 characters",
    "Long Text - No length limit",
    "Multi-Valued Field - Create Tag if it does not exist",
    "Multi-Valued Field - Apply Tag only if it exists already",
    "Single-Valued Field",
    "Date",
    "Checkbox",
    "Number",
}
VALID_OPERATORS = {"=", ":=", "+=", "++=", "+:="}
TRUTHY = {"x", "yes", "true", "1", "y"}
OBJECT_COLS = ("Image", "Video", "Audio", "Other (Multimedia)", "Folder", "Virtual Folder")


def is_truthy(val: str) -> bool:
    return val.strip().lower() in TRUTHY


def validate_metadata_csv(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    seen_names: dict[str, int] = {}
    seen_api: dict[str, int] = {}

    if not path.is_file():
        return {"status": "fail", "row_count": 0, "errors": [f"File not found: {path}"], "warnings": []}

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for idx, raw in enumerate(rows, start=2):
        row = {k.strip(): (v or "").strip() for k, v in raw.items() if k is not None}
        name = row.get("Field Name in OrangeDAM") or row.get("Field Name") or ""
        if not name:
            continue

        key = name.lower()
        if key in seen_names:
            errors.append(f"Row {idx}: duplicate Field Name '{name}' (first defined on row {seen_names[key]}).")
        seen_names[key] = idx

        ftype = row.get("Field Type", "")
        if ftype not in VALID_FIELD_TYPES:
            errors.append(f"Row {idx} ('{name}'): unrecognized Field Type '{ftype}'.")

        tag_type = row.get("Tag Type", "")
        is_tag_field = ftype in {
            "Multi-Valued Field - Create Tag if it does not exist",
            "Multi-Valued Field - Apply Tag only if it exists already",
            "Single-Valued Field",
        }
        if is_tag_field and (not tag_type or tag_type.upper() == "N/A"):
            errors.append(f"Row {idx} ('{name}'): '{ftype}' requires a Tag Type / Authority List.")
        if not is_tag_field and tag_type and tag_type.upper() != "N/A":
            warnings.append(f"Row {idx} ('{name}'): non-tag field type '{ftype}' specifies Tag Type '{tag_type}'.")

        filter_flag = row.get("Add to Filter Sidepanel", "")
        if is_truthy(filter_flag) and ftype in {"Text - Fewer than 500 characters", "Long Text - No length limit"}:
            warnings.append(
                f"Row {idx} ('{name}'): enabling Filter Sidepanel on free-text field '{ftype}' can degrade facet usability; prefer controlled Tag fields."
            )

        if not any(is_truthy(row.get(col, "")) for col in OBJECT_COLS):
            warnings.append(f"Row {idx} ('{name}'): not assigned to any Object Type ({', '.join(OBJECT_COLS)}).")

        api_name = row.get("Orange Logic API Field Name", "")
        if api_name:
            api_key = api_name.lower()
            if api_key in seen_api:
                errors.append(f"Row {idx} ('{name}'): duplicate API Field Name '{api_name}' (row {seen_api[api_key]}).")
            seen_api[api_key] = idx

        op = row.get("Operator", "")
        if op:
            if op not in VALID_OPERATORS:
                errors.append(f"Row {idx} ('{name}'): invalid DataTable V2.2 Operator '{op}'. Expected one of {sorted(VALID_OPERATORS)}.")
            elif ftype == "Multi-Valued Field - Apply Tag only if it exists already" and op == "++=":
                errors.append(f"Row {idx} ('{name}'): operator '++=' creates missing tags, contradicting 'Apply Tag only if it exists already' (use '+=').")
            elif ftype == "Multi-Valued Field - Create Tag if it does not exist" and op == "+=":
                warnings.append(f"Row {idx} ('{name}'): operator '+=' does not create new tags; consider '++=' to match field type.")

        csv_col = row.get("Column Label in the Imported CSV", "")
        if csv_col and not (csv_col.startswith("[") and csv_col.endswith("]")):
            warnings.append(f"Row {idx} ('{name}'): CSV column label '{csv_col}' should be wrapped in brackets (e.g., '[{csv_col}]').")

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "row_count": len(seen_names), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OrangeDAM Metadata Fields CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validate_metadata_csv(args.csv_path)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Metadata Schema Validation: {res['status'].upper()} ({res['row_count']} fields)")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
