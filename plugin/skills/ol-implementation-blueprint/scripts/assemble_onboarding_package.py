#!/usr/bin/env python3
"""Assemble a Markdown OrangeDAM Onboarding Handoff summary from domain CSV/MD files.

Standard-library only. Makes zero network calls and reads no environment secrets.

Usage:
    python3 assemble_onboarding_package.py <config_dir> [--output HANDOFF.md]
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


def summarize_csv(path: Path) -> tuple[int, list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if not rows:
        return 0, []
    headers = [h.strip() for h in rows[0]]
    data_rows = [r for r in rows[1:] if any(cell.strip() for cell in r)]
    return len(data_rows), headers


def build_handoff_markdown(config_dir: Path) -> str:
    lines: list[str] = [
        "# OrangeDAM Onboarding Configuration Handoff Package",
        "",
        f"Source directory: `{config_dir.name}`",
        "",
        "## Inventory of Configuration Artifacts",
        "",
        "| File | Type | Records / Lines | Columns / Summary |",
        "| :--- | :--- | :--- | :--- |",
    ]

    files = sorted(
        p for p in config_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".csv", ".md", ".json"}
    )
    if not files:
        lines.append("| *(none found)* | - | 0 | Add domain CSV/MD exports to this folder |")
    else:
        for path in files:
            ext = path.suffix.lower()
            if ext == ".csv":
                count, headers = summarize_csv(path)
                preview = ", ".join(headers[:6]) + ("..." if len(headers) > 6 else "")
                lines.append(f"| `{path.name}` | CSV | {count} rows | {preview} |")
            else:
                text = path.read_text(encoding="utf-8", errors="replace")
                line_count = len(text.splitlines())
                first_heading = next(
                    (ln.lstrip("# ").strip() for ln in text.splitlines() if ln.startswith("#")),
                    "Document",
                )
                lines.append(f"| `{path.name}` | {ext.lstrip('.').upper()} | {line_count} lines | {first_heading} |")

    lines.extend(
        [
            "",
            "## Environment Promotion Sign-Off",
            "",
            "| Domain | Sandbox Configured | Impersonation UAT Passed | Production Promoted | Owner / Date |",
            "| :--- | :---: | :---: | :---: | :--- |",
            "| Metadata & Taxonomies | [ ] | [ ] | [ ] | |",
            "| Embedded Metadata Rules | [ ] | [ ] | [ ] | |",
            "| Folders, Groups & Visibility | [ ] | [ ] | [ ] | |",
            "| Security Functions & Permissions | [ ] | [ ] | [ ] | |",
            "| Asset Formats & Watermarks | [ ] | [ ] | [ ] | |",
            "| Search, Workspaces & Portals | [ ] | [ ] | [ ] | |",
            "| Workflows, Forms & Emails | [ ] | [ ] | [ ] | |",
            "| DRM, SSO, AI & Integrations | [ ] | [ ] | [ ] | |",
            "| Migration & Delta Cutover | [ ] | [ ] | [ ] | |",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble OrangeDAM Onboarding Handoff Markdown.")
    parser.add_argument("config_dir", type=Path, help="Directory with domain CSV/MD files.")
    parser.add_argument("--output", type=Path, default=None, help="Optional output file path.")
    args = parser.parse_args()

    if not args.config_dir.is_dir():
        print(f"Error: directory not found: {args.config_dir}", file=sys.stderr)
        return 1

    md = build_handoff_markdown(args.config_dir)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
