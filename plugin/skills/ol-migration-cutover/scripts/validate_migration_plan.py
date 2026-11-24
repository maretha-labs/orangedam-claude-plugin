#!/usr/bin/env python3
"""Validate an OrangeDAM Asset Migration Plan JSON specification.

Standard-library only. Zero network calls, zero credential reads.

Usage:
    python3 validate_migration_plan.py <migration_plan.json> [--json]

Expected JSON shape:
{
  "target_cloud": "AWS",
  "target_region": "us-east-1",
  "sources": [
    {
      "name": "Legacy Box",
      "volume_tb": 12.5,
      "file_count": 250000,
      "source_cloud": "AWS",
      "source_region": "us-east-1",
      "max_assets_in_single_folder": 35000,
      "extensions": [".jpg", ".png", ".mov", ".pdf"],
      "has_3d_files": false,
      "has_zip_files": false,
      "extension_waivers_reviewed": true,
      "cutoff_date": "2026-12-31",
      "mvp_launch_subset": "2025-2026 Published Marketing (45,000 files)",
      "active_edits_during_migration": true,
      "delta_cutover_plan": "Nightly incremental sync + 48h freeze window",
      "has_published_links": true,
      "published_links_plan": "CMS URL update script before cutover"
    }
  ]
}
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MAX_FOLDER_ASSETS = 50000
SUSPICIOUS_EXTENSIONS = {".exe", ".bat", ".sh", ".dll", ".dmg", ".msi", ".app", ".jar"}


def validate_migration_plan(path: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return {"status": "fail", "source_count": 0, "errors": [f"File not found: {path}"], "warnings": []}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {"status": "fail", "source_count": 0, "errors": [f"Invalid JSON: {exc}"], "warnings": []}

    target_cloud = (data.get("target_cloud") or "").strip().lower()
    target_region = (data.get("target_region") or "").strip().lower()
    sources = data.get("sources") or []
    if not sources:
        errors.append("Migration plan must declare at least one source under 'sources'.")

    for idx, src in enumerate(sources, start=1):
        name = src.get("name") or f"Source #{idx}"
        if not src.get("file_count") or int(src.get("file_count", 0)) <= 0:
            errors.append(f"[{name}]: missing or non-positive 'file_count'.")
        if src.get("volume_tb") is None or float(src.get("volume_tb", 0)) <= 0:
            errors.append(f"[{name}]: missing or non-positive 'volume_tb'.")

        max_folder = int(src.get("max_assets_in_single_folder", 0) or 0)
        if max_folder > MAX_FOLDER_ASSETS:
            errors.append(
                f"[{name}]: max_assets_in_single_folder ({max_folder:,}) exceeds OrangeDAM's 50,000-asset per-folder limit; partition before ingest."
            )

        exts = [e.lower().strip() for e in (src.get("extensions") or []) if str(e).strip()]
        if not exts:
            errors.append(f"[{name}]: 'extensions' inventory is empty; enumerate all source file extensions.")
        flagged = sorted(set(exts) & SUSPICIOUS_EXTENSIONS)
        if flagged and not src.get("extension_waivers_reviewed"):
            errors.append(
                f"[{name}]: potentially prohibited/executable extensions {flagged} found without 'extension_waivers_reviewed: true'."
            )

        if (src.get("has_3d_files") or src.get("has_zip_files")) and not src.get("extension_waivers_reviewed"):
            warnings.append(
                f"[{name}]: includes 3D or ZIP files; confirm OrangeDAM ingestion/extraction handling and extension waivers with Orange Logic."
            )

        if not (src.get("cutoff_date") or "").strip():
            warnings.append(f"[{name}]: no source system 'cutoff_date' recorded.")

        if not (src.get("mvp_launch_subset") or "").strip():
            warnings.append(f"[{name}]: 'mvp_launch_subset' not defined; identify Day-1 searchable subset to de-risk launch.")

        if src.get("active_edits_during_migration") and not (src.get("delta_cutover_plan") or "").strip():
            errors.append(
                f"[{name}]: source remains live during migration ('active_edits_during_migration: true') but 'delta_cutover_plan' is missing."
            )

        if src.get("has_published_links") and not (src.get("published_links_plan") or "").strip():
            errors.append(
                f"[{name}]: source has published external links ('has_published_links: true') but 'published_links_plan' is missing."
            )

        src_cloud = (src.get("source_cloud") or "").strip().lower()
        src_region = (src.get("source_region") or "").strip().lower()
        if target_cloud and src_cloud and src_cloud != target_cloud:
            warnings.append(
                f"[{name}]: cross-cloud transfer ({src.get('source_cloud')} -> {data.get('target_cloud')}); budget egress fees and transfer acceleration."
            )
        elif target_cloud and src_cloud == target_cloud and target_region and src_region and src_region != target_region:
            warnings.append(
                f"[{name}]: cross-region transfer ({src.get('source_region')} -> {data.get('target_region')}); verify cross-region egress and ingest throughput."
            )

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "source_count": len(sources), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OrangeDAM Asset Migration Plan JSON.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    res = validate_migration_plan(args.json_path)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Migration Plan Validation: {res['status'].upper()} ({res['source_count']} source(s))")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
