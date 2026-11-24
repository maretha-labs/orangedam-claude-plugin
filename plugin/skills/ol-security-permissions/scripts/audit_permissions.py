#!/usr/bin/env python3
"""Audit OrangeDAM Groups, Visibility Classes, and Permissions CSVs.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 audit_permissions.py --groups groups.csv --permissions permissions.csv [--visibility visibility_classes.csv] [--json]
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

OOTB_GROUPS = {
    "*Everyone",
    "*UnregisteredUsers",
    "*RegisteredUsers",
    "*SuperAdmin",
    "Administrator",
}
OOTB_VISIBILITY = {"Pending Process", "Public", "Internal Use Only", "Hidden"}
PUBLIC_ANONYMOUS_GROUPS = {"*Everyone", "*UnregisteredUsers"}
TRUTHY = {"x", "yes", "true", "1", "y"}
HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")


def is_truthy(val: str) -> bool:
    return val.strip().lower() in TRUTHY


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return [
            {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            for row in csv.DictReader(fh)
        ]


def detect_cycles(parents_map: dict[str, list[str]]) -> list[str]:
    cycles: list[str] = []
    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(node: str, trail: list[str]) -> None:
        visiting.add(node)
        for parent in parents_map.get(node, []):
            if parent in visiting:
                cycle_start = trail.index(parent) if parent in trail else 0
                cycles.append(" -> ".join(trail[cycle_start:] + [parent]))
            elif parent not in visited and parent in parents_map:
                dfs(parent, trail + [parent])
        visiting.remove(node)
        visited.add(node)

    for grp in parents_map:
        if grp not in visited:
            dfs(grp, [grp])
    return cycles


def audit(groups_path: Path | None, perms_path: Path | None, vis_path: Path | None) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    known_groups: set[str] = set(OOTB_GROUPS)
    known_vis: set[str] = set(OOTB_VISIBILITY)
    parents_map: dict[str, list[str]] = {}

    if vis_path:
        if not vis_path.is_file():
            errors.append(f"Visibility classes file not found: {vis_path}")
        else:
            for idx, row in enumerate(read_rows(vis_path), start=2):
                vc = row.get("Visibility Class") or row.get("Name") or ""
                if not vc:
                    continue
                known_vis.add(vc)
                hx = row.get("Hex Color", "")
                if hx and not HEX_RE.match(hx):
                    warnings.append(f"visibility_classes.csv row {idx} ('{vc}'): Hex Color '{hx}' is not a valid 6-digit hex code.")

    if groups_path:
        if not groups_path.is_file():
            errors.append(f"Groups file not found: {groups_path}")
        else:
            rows = read_rows(groups_path)
            for idx, row in enumerate(rows, start=2):
                grp = row.get("Group") or row.get("Group Name") or ""
                if not grp:
                    continue
                known_groups.add(grp)
                acct_type = row.get("Account Type", "")
                if acct_type and acct_type not in {"Security", "Generic"}:
                    errors.append(f"groups.csv row {idx} ('{grp}'): Account Type '{acct_type}' must be 'Security' or 'Generic'.")
                raw_parents = row.get("Parent Groups", "")
                parents = [p.strip() for p in re.split(r"[|,;]", raw_parents) if p.strip() and p.strip().upper() != "N/A"]
                parents_map[grp] = parents

                if is_truthy(row.get("Custom", "")):
                    if not row.get("Test Account to Impersonate", ""):
                        warnings.append(f"groups.csv row {idx} ('{grp}'): missing Test Account to Impersonate for UAT.")
                    if not row.get("Who can add and remove users for this group?", ""):
                        warnings.append(f"groups.csv row {idx} ('{grp}'): missing delegated group manager ('Who can add and remove users').")

            for grp, parents in parents_map.items():
                for parent in parents:
                    if parent not in known_groups:
                        errors.append(f"groups.csv: group '{grp}' references unknown Parent Group '{parent}'.")

            for cycle in detect_cycles(parents_map):
                errors.append(f"groups.csv: circular group inheritance detected: {cycle}")

    if perms_path:
        if not perms_path.is_file():
            errors.append(f"Permissions file not found: {perms_path}")
        else:
            for idx, row in enumerate(read_rows(perms_path), start=2):
                folder = row.get("On Folder / Asset") or row.get("Folder") or ""
                grp = row.get("Group", "")
                vc = row.get("Visibility Class", "")
                if not folder and not grp:
                    continue

                if grp and grp not in known_groups:
                    errors.append(f"permissions.csv row {idx}: unknown Group '{grp}'.")
                if vc and vc not in known_vis:
                    errors.append(f"permissions.csv row {idx}: unknown Visibility Class '{vc}'.")

                has_s = is_truthy(row.get("S", "") or row.get("View Small", ""))
                has_m = is_truthy(row.get("M", "") or row.get("View Med", ""))
                has_l = is_truthy(row.get("L", "") or row.get("View Large", ""))
                has_orig = is_truthy(row.get("Original", "") or row.get("View Original", ""))
                has_view = has_s or has_m or has_l or has_orig
                has_dl = is_truthy(row.get("Dwlnd Btn", "") or row.get("Show Dwld Btn", ""))
                has_find = is_truthy(row.get("Find", ""))
                has_edit = is_truthy(row.get("Edit", ""))
                has_upload = is_truthy(row.get("Add / Upld", "") or row.get("Add/Upld", ""))
                has_delete = is_truthy(row.get("Delete", ""))
                has_move = is_truthy(row.get("Move", ""))
                has_admin = is_truthy(row.get("Admin", ""))

                if has_dl and not has_view and not has_admin:
                    errors.append(
                        f"permissions.csv row {idx} ({folder} / {grp}): Show Dwld Btn is enabled without any View permission (S/M/L/Original)."
                    )

                if (has_edit or has_delete or has_move) and not has_find and not has_admin:
                    warnings.append(
                        f"permissions.csv row {idx} ({folder} / {grp}): Edit/Delete/Move granted without Find permission."
                    )

                if grp in PUBLIC_ANONYMOUS_GROUPS:
                    if has_edit or has_upload or has_delete or has_move or has_admin:
                        errors.append(
                            f"permissions.csv row {idx} ({folder} / {grp}): write/admin permission granted to anonymous/public group '{grp}'."
                        )
                    if vc in {"Pending Process", "Internal Use Only", "Hidden"} or not vc:
                        errors.append(
                            f"permissions.csv row {idx} ({folder} / {grp}): anonymous/public group '{grp}' must be scoped strictly to 'Public' Visibility Class (found '{vc or 'ALL'}')."
                        )

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit OrangeDAM Groups, Visibility Classes, and Permissions.")
    parser.add_argument("--groups", type=Path, default=None)
    parser.add_argument("--permissions", type=Path, default=None)
    parser.add_argument("--visibility", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = audit(args.groups, args.permissions, args.visibility)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Security & Permissions Audit: {res['status'].upper()}")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
