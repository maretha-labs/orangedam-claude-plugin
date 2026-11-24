#!/usr/bin/env python3
"""Cross-domain referential integrity validator for OrangeDAM onboarding CSVs.

Standard-library only. Makes zero network calls and reads no environment secrets.

Usage:
    python3 validate_workbook.py <config_dir> [--json]

Recognized optional CSV files inside <config_dir>:
    - metadata_fields.csv
    - tags.csv
    - folders.csv
    - visibility_classes.csv
    - groups.csv
    - permissions.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

OOTB_GROUPS = {
    "*Everyone",
    "*UnregisteredUsers",
    "*RegisteredUsers",
    "*SuperAdmin",
    "Administrator",
}
OOTB_VISIBILITY_CLASSES = {
    "Pending Process",
    "Public",
    "Internal Use Only",
    "Hidden",
}
OOTB_TAG_TYPES = {"Common", "Country", "City", "Source Accounts"}
TRUTHY = {"x", "yes", "true", "1", "y"}


def is_truthy(val: str | None) -> bool:
    return (val or "").strip().lower() in TRUTHY


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [
            {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            for row in csv.DictReader(fh)
        ]


def get_ci(row: dict[str, str], *candidates: str) -> str:
    lower_map = {k.lower(): v for k, v in row.items()}
    for cand in candidates:
        if cand.lower() in lower_map:
            return lower_map[cand.lower()]
    return ""


def validate_directory(config_dir: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    loaded: list[str] = []

    if not config_dir.is_dir():
        return {
            "status": "error",
            "loaded_files": [],
            "errors": [f"Directory not found: {config_dir}"],
            "warnings": [],
        }

    tag_types: set[str] = set(OOTB_TAG_TYPES)
    folders: set[str] = set()
    vis_classes: set[str] = set(OOTB_VISIBILITY_CLASSES)
    groups: set[str] = set(OOTB_GROUPS)

    tags_path = config_dir / "tags.csv"
    if tags_path.is_file():
        loaded.append(tags_path.name)
        for row in read_csv(tags_path):
            tt = get_ci(row, "Tag Type", "Tag Type (Category)")
            if tt:
                tag_types.add(tt)

    folders_path = config_dir / "folders.csv"
    if folders_path.is_file():
        loaded.append(folders_path.name)
        for idx, row in enumerate(read_csv(folders_path), start=2):
            for col in ("Folder Name", "Folder", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6"):
                val = get_ci(row, col)
                if val:
                    folders.add(val)
            proj = get_ci(row, "Projected Asset Count", "Asset Count")
            if proj.isdigit() and int(proj) > 50000:
                errors.append(
                    f"folders.csv row {idx}: projected asset count {proj} exceeds OrangeDAM's 50,000-asset per-folder recommendation."
                )

    vc_path = config_dir / "visibility_classes.csv"
    if vc_path.is_file():
        loaded.append(vc_path.name)
        for row in read_csv(vc_path):
            vc = get_ci(row, "Visibility Class", "Name")
            if vc:
                vis_classes.add(vc)

    groups_path = config_dir / "groups.csv"
    if groups_path.is_file():
        loaded.append(groups_path.name)
        for idx, row in enumerate(read_csv(groups_path), start=2):
            grp = get_ci(row, "Group", "Group Name")
            if grp:
                groups.add(grp)
                custom = is_truthy(get_ci(row, "Custom"))
                test_acct = get_ci(row, "Test Account to Impersonate", "Test Account")
                if custom and not test_acct:
                    warnings.append(
                        f"groups.csv row {idx}: custom group '{grp}' has no Test Account to Impersonate defined for UAT."
                    )

    meta_path = config_dir / "metadata_fields.csv"
    if meta_path.is_file():
        loaded.append(meta_path.name)
        for idx, row in enumerate(read_csv(meta_path), start=2):
            fname = get_ci(row, "Field Name in OrangeDAM", "Field Name")
            ftype = get_ci(row, "Field Type")
            tt = get_ci(row, "Tag Type", "Authority List")
            if not fname:
                continue
            needs_tag_type = any(
                tok in ftype.lower() for tok in ("multi-valued", "single-valued")
            )
            if needs_tag_type:
                if not tt or tt.upper() == "N/A":
                    errors.append(
                        f"metadata_fields.csv row {idx} ('{fname}'): controlled field type '{ftype}' requires a Tag Type."
                    )
                elif tags_path.is_file() and tt not in tag_types:
                    errors.append(
                        f"metadata_fields.csv row {idx} ('{fname}'): references Tag Type '{tt}' which is not defined in tags.csv or OOTB Tag Types."
                    )

    perm_path = config_dir / "permissions.csv"
    if perm_path.is_file():
        loaded.append(perm_path.name)
        for idx, row in enumerate(read_csv(perm_path), start=2):
            folder = get_ci(row, "On Folder / Asset", "Folder")
            grp = get_ci(row, "Group")
            vc = get_ci(row, "Visibility Class")

            if folders_path.is_file() and folder and folder not in folders:
                errors.append(
                    f"permissions.csv row {idx}: folder '{folder}' not found in folders.csv."
                )
            if grp and grp not in groups:
                errors.append(
                    f"permissions.csv row {idx}: group '{grp}' not found in groups.csv or OOTB Groups."
                )
            if vc and vc not in vis_classes:
                errors.append(
                    f"permissions.csv row {idx}: Visibility Class '{vc}' not found in visibility_classes.csv or OOTB classes."
                )

            has_view = any(
                is_truthy(get_ci(row, col))
                for col in ("S", "View Small", "M", "View Med", "L", "View Large", "Original", "View Original")
            )
            has_dl = is_truthy(get_ci(row, "Dwlnd Btn", "Show Dwld Btn"))
            if has_dl and not has_view:
                errors.append(
                    f"permissions.csv row {idx} ({folder}/{grp}): Show Dwld Btn enabled without any View permission (S/M/L/Original)."
                )

    if not loaded:
        warnings.append(
            f"No recognized workbook CSV files found in {config_dir}. Expected any of: metadata_fields.csv, tags.csv, folders.csv, visibility_classes.csv, groups.csv, permissions.csv."
        )

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {
        "status": status,
        "loaded_files": loaded,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-domain integrity validator for OrangeDAM onboarding CSVs."
    )
    parser.add_argument("config_dir", type=Path, help="Directory containing configuration CSV files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report.")
    args = parser.parse_args()

    result = validate_directory(args.config_dir)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Workbook Audit Status: {result['status'].upper()}")
        print(f"Loaded files ({len(result['loaded_files'])}): {', '.join(result['loaded_files']) or 'none'}")
        for err in result["errors"]:
            print(f"  [ERROR] {err}")
        for warn in result["warnings"]:
            print(f"  [WARN]  {warn}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
