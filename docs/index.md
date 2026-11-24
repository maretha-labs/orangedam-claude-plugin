# OrangeDAM Config Assistant by Maretha — Documentation

Documentation for the `maretha-orangedam-config` Claude Directory plugin ([github.com/maretha-labs/orangedam-claude-plugin](https://github.com/maretha-labs/orangedam-claude-plugin)).

## Overview

`OrangeDAM Config Assistant by Maretha` guides DAM administrators, solution architects, and implementation teams through configuring a new Orange Logic (OrangeDAM) deployment across 15 domain skills, plain-text templates, and local Python validation scripts.

> Independent open-source partner plugin by [Maretha](https://maretha.io). Not an official Anthropic or Orange Logic product.

## Supported Claude Surfaces

| Component | claude.ai Chat | Cowork | Claude Code |
| :--- | :--- | :--- | :--- |
| 15 Domain Skills (`skills/`) | Yes | Yes | Yes |
| Local Python 3 Validators (`scripts/`) | Yes (code sandbox) | Yes | Yes |
| 2 Specialist Agents (`agents/`) | Skipped | Yes | Yes |

## Installation

- **claude.ai & Cowork:** Open **Customize > Plugins > Discover**, search for **OrangeDAM Config Assistant by Maretha**, and install.
- **Claude Code:** Run `/plugin directory`, or install from GitHub: `/plugin install maretha-orangedam-config --marketplace maretha-labs/orangedam-claude-plugin`. For local testing: `claude --plugin-dir ./plugin`.

## Recommended Implementation Sequence

1. `ol-implementation-blueprint` — Discovery, MVP scoping, Use Case Scenarios, User Stories
2. `ol-onboarding-kickoff` — Branding assets, vanity URL, outbound email, legal copy, test assets
3. `ol-metadata-schema` -> `ol-taxonomy-tags` -> `ol-embedded-metadata` — Information architecture & EXIF/IPTC/XMP mapping
4. `ol-folder-structure` -> `ol-security-permissions` -> `ol-formats-mam` — Folders, Groups, Visibility Classes, Security Functions, Permissions, Renditions
5. `ol-search-workspaces-branding` -> `ol-workflows-approvals` -> `ol-drm-compliance` -> `ol-identity-sso` — UX, Approvals, DRM, SSO
6. `ol-ai-automation` -> `ol-integrations-api` -> `ol-migration-cutover` — AI governance, integrations, migration, UAT, cutover
7. Re-run `ol-implementation-blueprint` cross-domain audit (`validate_workbook.py`) before configuring Sandbox.
