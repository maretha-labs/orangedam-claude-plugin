#!/usr/bin/env python3
"""Validate OrangeDAM EXIF/IPTC/XMP embedded metadata mapping rules CSV.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 validate_embedded_mappings.py <embedded_mappings.csv> [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

NATIVE_FIELDS = {
    "audiosamplingrate",
    "colorprofile",
    "duration",
    "docduration",
    "starttimecode",
    "bitrate",
    "videobitrate",
    "audiobitrate",
    "framerate",
    "displayaspectratio",
    "videoformat",
    "audioformat",
    "audiobitdepth",
    "mainaudiotrackchannels",
    "filesize",
    "filemd5",
}
TEXT_REQUIRED_EXIF_TAGS = {
    "exposuretime",
    "focallength",
    "focallengthin35mmformat",
    "exposurecompensation",
}
COLLISION_BARE_TAGS = {"contrast", "saturation", "sharpness"}
VALID_SOURCE_TYPES = {"EXIF", "IPTC", "XMP", "System"}


def validate_embedded_csv(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    priorities_by_dest: dict[tuple[str, str], dict[str, int]] = defaultdict(dict)
    active_rules = 0

    if not path.is_file():
        return {"status": "fail", "active_rules": 0, "errors": [f"File not found: {path}"], "warnings": []}

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))

    for idx, raw in enumerate(rows, start=2):
        row = {k.strip(): (v or "").strip() for k, v in raw.items() if k is not None}
        create = (row.get("Create rule?") or "Yes").lower()
        if create.startswith("no") or create.startswith("not possible"):
            continue
        active_rules += 1

        src_type = row.get("Source Type", "")
        src_field = row.get("Source Field") or row.get("Source Field (enter exactly)") or ""
        dest = row.get("Destination Field", "")
        dest_type = row.get("Destination Field Type", "").lower()
        prio = row.get("Priority (OrderNumber)", "")
        in_cor = row.get("In COR picker?", "").lower()
        opt_action = row.get("Option-list action", "")
        direction = (row.get("Direction") or "Upload").lower()

        if src_type and src_type not in VALID_SOURCE_TYPES:
            errors.append(f"Row {idx}: unsupported Source Type '{src_type}'. Expected EXIF, IPTC, XMP, or System.")

        if src_type != "System" and not src_field:
            errors.append(f"Row {idx}: active rule targeting '{dest}' is missing Source Field.")

        if dest.lower() in NATIVE_FIELDS and src_type != "System":
            warnings.append(
                f"Row {idx}: '{dest}' is already auto-populated natively by OrangeDAM on ingest; a custom mapping rule is usually unnecessary."
            )

        if src_field.lower() in {"createdate", "-xmp:createdate"} and dest.lower() == "createdate":
            errors.append(
                f"Row {idx}: do not map embedded '{src_field}' into OrangeDAM record 'CreateDate' (record creation date). Target 'DocDate' or a custom field."
            )

        if src_field.lower() == "filesource" and dest.lower() in {"source", "corefield.creator"}:
            errors.append(
                f"Row {idx}: EXIF 'FileSource' is capture device type (camera/scanner), not Cortex 'Source' (creator)."
            )

        if src_field.lower() in TEXT_REQUIRED_EXIF_TAGS and "num" in dest_type:
            errors.append(
                f"Row {idx}: ExifTool returns formatted text for '{src_field}' (e.g., '1/250', '50.0 mm'); Destination Field Type must be Text, not Numeric."
            )

        if src_type == "EXIF" and src_field.lower() in COLLISION_BARE_TAGS:
            warnings.append(
                f"Row {idx}: bare EXIF tag '{src_field}' also exists under XMP-crs; consider '-ExifIFD:{src_field}' if strict camera-only extraction is required."
            )

        if in_cor == "no" and (not opt_action or opt_action.lower() == "none"):
            expected_list = "EXIFFieldsOptionList" if src_type == "EXIF" else "XMPFieldsOptionList_ClientSpecific"
            errors.append(
                f"Row {idx}: '{src_field}' is not in the default COR picker; set Option-list action (e.g., 'Add to {expected_list}')."
            )

        if dest and prio:
            if not prio.isdigit() or int(prio) < 1:
                errors.append(f"Row {idx}: Priority (OrderNumber) '{prio}' must be a positive integer.")
            else:
                key = (dest.lower(), direction)
                if prio in priorities_by_dest[key]:
                    errors.append(
                        f"Row {idx}: duplicate Priority '{prio}' for destination '{dest}' ({direction}); first used on row {priorities_by_dest[key][prio]}."
                    )
                priorities_by_dest[key][prio] = idx

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "active_rules": active_rules, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OrangeDAM embedded metadata mapping CSV.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validate_embedded_csv(args.csv_path)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Embedded Metadata Validation: {res['status'].upper()} ({res['active_rules']} active rules)")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
