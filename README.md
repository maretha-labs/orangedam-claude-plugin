# OrangeDAM Config Assistant by Maretha (Claude Plugin Repository)

Open-source repository for the **`maretha-orangedam-config`** Claude Directory plugin bundle (`plugin/`), published independently by [Maretha](https://maretha.io) under [Maretha Labs](https://github.com/maretha-labs).

> **Affiliation & Trade-Off Notice:** Not an official Anthropic or Orange Logic product. Version 1.0 operates strictly locally (Markdown skills, CSV/Markdown templates, and stdlib Python 3 validators) with zero remote API calls or live instance mutations. Tenant-specific settings marked `[VERIFY IN SANDBOX / OL DOCS]` must be confirmed against your Orange Logic environment before Production rollout.

## Repository Layout

- `plugin/` — **Submitted plugin bundle** (enter `plugin` as the **Plugin path** in [claude.ai/directory/manage](https://claude.ai/directory/manage)). Contains `.claude-plugin/plugin.json`, `README.md`, `LICENSE`, `SECURITY.md`, `assets/icon.png`, 15 skills under `skills/`, and 2 optional Cowork/Claude Code agents under `agents/`.
- `scripts/check_plugin_hygiene.py` — Mirrors Anthropic's automated directory validation & confidentiality checks.
- `tests/` — Pytest suite covering all bundled Python 3 stdlib validators and hygiene checks.
- `evals/` — Behavioral eval suite for `claude plugin eval`.
- `docs/` — Public documentation, privacy policy, support, and terms pages linked directly from `plugin.json`.

## Quick Local Commands

```bash
# 1. Start Claude Code with this plugin loaded directly from disk
claude --plugin-dir ./plugin

# 2. Validate manifest, components, and strict warnings
claude plugin validate --strict ./plugin

# 3. Validate all 15 skills against the Agent Skills specification
for s in plugin/skills/*/; do .venv/bin/skills-ref validate "$s"; done

# 4. Run Anthropic directory hygiene & clean-room audit
python3 scripts/check_plugin_hygiene.py --plugin-dir plugin --repo-root .

# 5. Run unit tests for all bundled Python validators
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -v tests/

# 6. Run behavioral evals (uses Claude model calls on your account)
claude plugin eval ./plugin --eval-dir ./evals --no-publish
```

## Directory Submission Notes

- Submit from **Maretha's** Claude organization at [claude.ai/directory/manage](https://claude.ai/directory/manage) -> **Submit new** -> **Plugin bundle**.
- **Repository:** `maretha-labs/orangedam-claude-plugin` | **Plugin path:** `plugin`
- See `SECURITY.md` for vulnerability reporting and safe usage guidance.
