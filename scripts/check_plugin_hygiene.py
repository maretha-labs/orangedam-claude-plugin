#!/usr/bin/env python3
"""Anthropic Claude Directory pre-submission hygiene & clean-room checker.

Replicates the automated repository, manifest, file-limit, credential, and
clean-room checks documented in https://claude.com/docs/plugins/pre-submission-checklist.

Usage:
    python3 scripts/check_plugin_hygiene.py [--plugin-dir plugin]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

MAX_FILES = 512
MAX_NON_IMAGE_BYTES = 256 * 1024
MAX_ANY_FILE_BYTES = 5 * 1024 * 1024
ALLOWED_TEXT_EXTS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".csv", ".py", ".sh", ".svg",
    ".toml", ".ini", ".js", ".ts", ".css", ".html", ".xml", ".gitignore", "",
}
ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
ALLOWED_FONT_EXTS = {".ttf", ".otf", ".woff", ".woff2"}
FORBIDDEN_SYSTEM_FILES = {".ds_store", "thumbs.db", "desktop.ini", "__macosx"}
WINDOWS_RESERVED = {
    "con", "prn", "aux", "nul",
    *(f"com{i}" for i in range(1, 10)),
    *(f"lpt{i}" for i in range(1, 10)),
}
LOCKFILE_NAMES = {"package-lock.json", "npm-shrinkwrap.json", "bun.lock", "bun.lockb"}
PACKAGE_CONFIG_FILES = {".npmrc", "bunfig.toml", "uv.toml"}
RESERVED_WHOLE_NAMES = {"claude", "anthropic", "anthropics", "claude-code", "claude-mods", "official", "plugin", "mcp", "test"}
RESERVED_PREFIXES = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
ENV_SECRET_RE = re.compile(r"\$[A-Z][A-Z0-9_]*(?:TOKEN|SECRET|KEY|PASSWORD|API_KEY|AUTH)[A-Z0-9_]*")
LAUNCHER_UNPINNED_RE = re.compile(r"\b(?:npx|bunx|uvx|pipx\s+run)\s+[^\s@=]+(?:\s|$)")
# Generic confidentiality / unreleased-document guard patterns.
# Pass an external private blocklist via --blocklist-file for local pre-release checks.
CLEAN_ROOM_PATTERNS = [
    re.compile(r"confidential\s*[\u2014\-]\s*internal\s+use\s+only", re.I),
    re.compile(r"proprietary\s+and\s+confidential", re.I),
    re.compile(r"strictly\s+confidential", re.I),
]


def count_non_code_words(md_text: str) -> int:
    stripped = re.sub(r"```.*?```", " ", md_text, flags=re.S)
    stripped = re.sub(r"`[^`]+`", " ", stripped)
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", stripped))


def check_plugin(
    plugin_dir: Path,
    repo_root: Path | None = None,
    extra_patterns: list[re.Pattern[str]] | None = None,
) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    blocklist = list(CLEAN_ROOM_PATTERNS) + list(extra_patterns or [])

    if not plugin_dir.is_dir():
        return {"status": "fail", "file_count": 0, "errors": [f"Plugin directory not found: {plugin_dir}"], "warnings": []}

    # 1. Manifest checks
    manifest_dir = plugin_dir / ".claude-plugin"
    manifest_path = manifest_dir / "plugin.json"
    if not manifest_path.is_file():
        errors.append("Missing required manifest: .claude-plugin/plugin.json")
    else:
        extras = [p.name for p in manifest_dir.iterdir() if p.name != "plugin.json"]
        if extras:
            errors.append(f".claude-plugin/ must contain only plugin.json (found: {extras})")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in plugin.json: {exc}")
            manifest = {}

        name = manifest.get("name", "")
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?", name):
            errors.append(f"Manifest 'name' '{name}' must be lowercase ASCII kebab-case (1-64 chars).")
        if name in RESERVED_WHOLE_NAMES or name.startswith(RESERVED_PREFIXES):
            errors.append(f"Manifest 'name' '{name}' uses a reserved Anthropic/generic identifier.")

        for field in ("displayName", "version", "description", "author"):
            if not manifest.get(field):
                warnings.append(f"Manifest missing recommended field '{field}'.")

        has_license_file = (plugin_dir / "LICENSE").is_file() or (plugin_dir / "LICENSE.md").is_file()
        if not has_license_file and not manifest.get("license"):
            errors.append("Missing LICENSE file and 'license' field in plugin.json.")

        icon_rel = manifest.get("icon", "")
        if icon_rel:
            icon_path = (plugin_dir / icon_rel).resolve()
            if not icon_path.is_file():
                errors.append(f"Manifest icon '{icon_rel}' not found.")
            elif not str(icon_path).startswith(str(plugin_dir.resolve())):
                errors.append(f"Manifest icon '{icon_rel}' escapes plugin directory.")
            elif icon_path.suffix.lower() not in ALLOWED_IMAGE_EXTS and icon_path.suffix.lower() != ".svg":
                errors.append(f"Manifest icon '{icon_rel}' must be PNG/JPEG/GIF/WebP/SVG (never .ico).")

    # 2. Disallowed top-level items for Chat/Cowork & Claude Code hygiene
    if (plugin_dir / "bin").exists():
        errors.append("Top-level bin/ directory blocks installation on claude.ai Chat and Cowork.")
    if (plugin_dir / "CLAUDE.md").exists():
        warnings.append("CLAUDE.md at plugin root is not loaded by Claude Code and emits a validate warning.")
    for lf in LOCKFILE_NAMES:
        if (plugin_dir / lf).exists():
            warnings.append(f"Root lockfile '{lf}' triggers a directory Policy Hold.")

    # 3. README >= 40 non-code words
    readme_path = plugin_dir / "README.md"
    if not readme_path.is_file():
        errors.append("Missing required README.md in plugin folder.")
    else:
        wc = count_non_code_words(readme_path.read_text(encoding="utf-8"))
        if wc < 40:
            errors.append(f"README.md has only {wc} non-code words (minimum 40 required).")

    # 4. Walk every file in plugin_dir
    all_files: list[Path] = []
    seen_case_paths: dict[str, Path] = {}
    for root, dirs, files in os.walk(plugin_dir, followlinks=False):
        root_p = Path(root)
        for name in list(dirs) + list(files):
            p = root_p / name
            rel = p.relative_to(plugin_dir)
            if p.is_symlink():
                errors.append(f"Symbolic link forbidden in plugin folder: {rel}")
            if name.lower() in FORBIDDEN_SYSTEM_FILES:
                errors.append(f"Forbidden OS system file in plugin folder: {rel}")
            if ":" in name or name.endswith(".") or name.endswith(" "):
                errors.append(f"Cross-platform unsafe filename: {rel}")
            stem = p.stem.lower()
            if stem in WINDOWS_RESERVED:
                errors.append(f"Windows reserved filename forbidden: {rel}")
            lower_rel = str(rel).lower()
            if lower_rel in seen_case_paths:
                errors.append(f"Case-colliding path: {rel} vs {seen_case_paths[lower_rel]}")
            seen_case_paths[lower_rel] = rel

        for fname in files:
            fpath = root_p / fname
            all_files.append(fpath)
            rel = fpath.relative_to(plugin_dir)
            ext = fpath.suffix.lower()
            size = fpath.stat().st_size

            if fname.lower() in PACKAGE_CONFIG_FILES:
                errors.append(f"Disallowed package manager config file: {rel}")

            if size > MAX_ANY_FILE_BYTES:
                errors.append(f"File exceeds 5 MiB limit: {rel} ({size} bytes)")

            if ext in ALLOWED_IMAGE_EXTS or ext in ALLOWED_FONT_EXTS:
                continue
            elif ext in ALLOWED_TEXT_EXTS or fname in {"LICENSE", "README"}:
                if size > MAX_NON_IMAGE_BYTES:
                    errors.append(f"Non-image file exceeds 256 KiB hold limit: {rel} ({size} bytes)")
                text = fpath.read_text(encoding="utf-8", errors="replace")
                if text.startswith("version https://git-lfs.github.com/spec/v1"):
                    errors.append(f"Git LFS pointer file forbidden: {rel}")
                if ENV_SECRET_RE.search(text):
                    errors.append(f"Potential environment credential reference ($*_TOKEN/$*_KEY) found in {rel}")
                if LAUNCHER_UNPINNED_RE.search(text):
                    warnings.append(f"Possible unpinned package launcher reference in {rel}")
                for pat in blocklist:
                    if pat.search(text):
                        errors.append(f"Confidentiality check violation in {rel}: matched pattern '{pat.pattern}'")
            else:
                errors.append(f"Disallowed binary/non-text file extension triggers Policy Hold: {rel}")

    if len(all_files) > MAX_FILES:
        errors.append(f"Plugin contains {len(all_files)} files (limit {MAX_FILES} to avoid Policy Hold).")

    # 5. Validate every skill folder under skills/
    skills_dir = plugin_dir / "skills"
    if skills_dir.is_dir():
        for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"Skill directory missing SKILL.md: skills/{skill_dir.name}")
                continue
            content = skill_md.read_text(encoding="utf-8")
            line_count = len(content.splitlines())
            if line_count > 500:
                warnings.append(f"skills/{skill_dir.name}/SKILL.md is {line_count} lines (recommended < 500).")
            m = re.match(r"^---\n(.*?)\n---", content, flags=re.S)
            if not m:
                errors.append(f"skills/{skill_dir.name}/SKILL.md missing valid YAML frontmatter.")
            else:
                fm = m.group(1)
                name_m = re.search(r"^name:\s*(.+)$", fm, flags=re.M)
                desc_m = re.search(r"^description:\s*(.+)$", fm, flags=re.M)
                if not name_m or name_m.group(1).strip() != skill_dir.name:
                    errors.append(f"skills/{skill_dir.name}/SKILL.md frontmatter 'name' must match directory name '{skill_dir.name}'.")
                if not desc_m:
                    errors.append(f"skills/{skill_dir.name}/SKILL.md missing frontmatter 'description'.")
                elif len(desc_m.group(1).strip()) > 1024:
                    errors.append(f"skills/{skill_dir.name}/SKILL.md description exceeds 1,024 chars.")

            # Verify every referenced references/*, assets/*, scripts/* file exists
            for ref in re.findall(r"(?<![A-Za-z0-9_.-])(?:references|assets|scripts)/[A-Za-z0-9_.-]+", content):
                if not (skill_dir / ref).is_file():
                    errors.append(f"skills/{skill_dir.name}/SKILL.md references missing file '{ref}'.")

    # 6. Check .gitattributes across repo if provided
    if repo_root and repo_root.is_dir():
        for ga in repo_root.rglob(".gitattributes"):
            if ".venv" in ga.parts or ".git" in ga.parts:
                continue
            ga_text = ga.read_text(encoding="utf-8", errors="replace")
            for bad in ("export-ignore", "export-subst", "filter="):
                if bad in ga_text:
                    errors.append(f"Disallowed '{bad}' directive in {ga.relative_to(repo_root)}")

    status = "fail" if errors else ("warn" if warnings else "pass")
    return {"status": status, "file_count": len(all_files), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Anthropic Claude Plugin Directory hygiene.")
    parser.add_argument("--plugin-dir", type=Path, default=Path("plugin"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--blocklist-file", type=Path, default=None, help="Optional newline-separated regex patterns to block.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    extra: list[re.Pattern[str]] = []
    if args.blocklist_file and args.blocklist_file.is_file():
        for line in args.blocklist_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                extra.append(re.compile(line, re.I))

    res = check_plugin(args.plugin_dir, args.repo_root, extra)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Plugin Hygiene Check: {res['status'].upper()} ({res['file_count']} files in {args.plugin_dir})")
        for e in res["errors"]:
            print(f"  [ERROR] {e}")
        for w in res["warnings"]:
            print(f"  [WARN]  {w}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
