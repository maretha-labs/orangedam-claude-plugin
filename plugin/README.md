# OrangeDAM Config Assistant by Maretha

Configure new Orange Logic (OrangeDAM) Digital Asset Management implementations from pre-kickoff discovery through go-live cutover. Published independently by [Maretha](https://maretha.io), an enterprise DAM implementation consultancy.

> **Affiliation Notice:** This plugin is created and maintained by Maretha as an independent partner resource for teams configuring Orange Logic (OrangeDAM). It is not an official Anthropic or Orange Logic product, and "Orange Logic" and "OrangeDAM" are trademarks of Orange Logic, LLC.

## Install

- **claude.ai & Cowork:** Install from **Customize > Plugins > Discover**.
- **Claude Code:** Install from the directory (`/plugin directory`), or directly from GitHub:

```bash
/plugin install maretha-orangedam-config --marketplace maretha-labs/orangedam-claude-plugin
```

## What this plugin does

This plugin packages 15 focused implementation skills, plain-text configuration templates (CSV and Markdown), reference tables, and deterministic Python validation scripts that work across **claude.ai Chat, Cowork, and Claude Code** (plus two specialist subagents for Cowork and Claude Code):

1. **Master Blueprint & Cross-Domain Audit (`ol-implementation-blueprint`)** — Run discovery interviews, structure MVP vs. Post-MVP use cases and user stories, assemble a unified Onboarding Workbook package, and validate cross-file referential integrity.
2. **Pre-Kickoff Readiness (`ol-onboarding-kickoff`)** — Plan branding assets (light/dark logos, favicon specs), vanity URLs, outbound email sender setup, representative test assets, homepage templates, and legal copy.
3. **Object Model & Metadata Schema (`ol-metadata-schema`)** — Map core OrangeDAM fields and custom namespaced fields, choose field types and search/filter/mandatory flags, and draft DataTable API V2.2 mapping specs.
4. **Taxonomy, Tags & Authority Lists (`ol-taxonomy-tags`)** — Design Tag Types, multi-level hierarchical tag trees, open vs. controlled Authority Lists, and "To Be Vetted" governance.
5. **Embedded Metadata Mapping (`ol-embedded-metadata`)** — Configure prioritized EXIF, IPTC, XMP, and ICC upload/download mapping rules while avoiding native-field duplication and ExifTool type pitfalls.
6. **Folder Structure, Stacks & Collections (`ol-folder-structure`)** — Design department, project, or lifecycle folder trees enforcing OrangeDAM's 50,000-assets-per-folder guideline, plus virtual folders, Stacks, and Collections.
7. **Security, Groups, Visibility Classes & Permissions (`ol-security-permissions`)** — Architect Security vs. Generic groups, Visibility Classes, Security Functions, test impersonation accounts, and full Folder x Group x Visibility Class x Subtype permission matrices.
8. **Asset Formats, Renditions & MAM (`ol-formats-mam`)** — Map Small/Medium/Large/Original rendition codes (`TR7`, `TR4`, `TR1_COMP`, `TR1_WATERMARKED`, `TR1`, `WebLow`, `WebHigh`, `TRX`), watermarks, video transcoding pipelines, and large-file transfer.
9. **Search, Filters, Workspaces & Brand Portals (`ol-search-workspaces-branding`)** — Configure Filters Sidepanel facets, Public Page vs. Asset Management workspaces, homepage personalization, and Site Builder microsites.
10. **Workflows, Forms, Approvals & Notifications (`ol-workflows-approvals`)** — Design cart/download request flows, Form Builder forms, FlowSteps, talent selects/kills reviews, project views, and automated email matrices.
11. **DRM, Restrictions & Compliance (`ol-drm-compliance`)** — Configure embargoes, asset expirations, talent releases, virus/checksum ingest checks, C2PA provenance, and regulatory alignment.
12. **Identity, SSO & User Lifecycle (`ol-identity-sso`)** — Plan SAML/OAuth SSO vs. local login boundaries, self-registration forms, offboarding, link expiration, and usage reporting.
13. **AI Services & Automation Governance (`ol-ai-automation`)** — Configure Auto-Tagging, OCR, Speech-to-Text, facial/logo recognition, Bring Your Own AI providers, and Agentic AI Studio governance rules. (This plugin configures platform settings only and never generates AI images, video, or audio.)
14. **Integrations, APIs & Cloud Topology (`ol-integrations-api`)** — Plan Adobe CC, Figma, CMS/PIM, cloud watch-folder, CDN/IIIF, DataTable V2.2 / iAPI, desktop tool, and cloud storage topologies.
15. **Asset Migration & Go-Live Cutover (`ol-migration-cutover`)** — Build per-source migration plans, align cloud regions, plan delta cutovers and external URL redirects, and generate group-by-group UAT scripts.

## Example prompts

Try any of these requests after installing the plugin:

1. **Full Onboarding Kickoff:** "We are launching a new OrangeDAM instance for a 250-person media company with Marketing, Creative, Legal, and External Agency users. Help us design our MVP metadata schema, folder hierarchy, security groups, visibility classes, and permissions matrix, and validate everything for conflicts."
2. **Embedded Metadata Audit:** "Review this CSV of EXIF, IPTC, and XMP tags we want extracted on upload into OrangeDAM. Flag which fields are already auto-populated natively, which need COR option-list additions, and any priority or data-type traps."
3. **Permissions & Least-Privilege Review:** "Audit our OrangeDAM Groups, Security Functions, and Folder Permissions CSVs to check for circular inheritance, download buttons without View access, missing test impersonation accounts, or exposed Pending Process assets."
4. **Renditions & Watermarking Design:** "Configure our OrangeDAM asset formats and permissions so external partners see watermarked medium previews by default and must submit an intended-use cart request to unlock clean originals."
5. **Migration & Cutover Planning:** "Create an OrangeDAM Asset Migration Plan for moving 18 TB (420,000 images and ProRes videos) from AWS us-east-1 cloud storage while creative teams continue uploading until launch weekend."

## Local scripts & what this plugin runs

Six skills include human-readable, standard-library-only Python 3 validation and packaging scripts (`scripts/*.py`) that Claude can run locally (in Claude Code, Cowork, or claude.ai's code execution sandbox) on CSV or JSON files you provide:

- `ol-implementation-blueprint/scripts/validate_workbook.py` & `assemble_onboarding_package.py`
- `ol-metadata-schema/scripts/validate_metadata_schema.py`
- `ol-taxonomy-tags/scripts/validate_tag_tree.py`
- `ol-embedded-metadata/scripts/validate_embedded_mappings.py`
- `ol-folder-structure/scripts/validate_folder_tree.py`
- `ol-security-permissions/scripts/audit_permissions.py`
- `ol-migration-cutover/scripts/validate_migration_plan.py`

None of these scripts install third-party packages, read environment variables or credentials, or make outbound network requests.

## Data handling, security notes & known trade-offs

- **Data transmitted externally:** None. Version 1.0 of this plugin contains no remote MCP servers, no hooks, no telemetry, and no outbound network requests.
- **Data stored:** The plugin stores nothing outside files you explicitly ask Claude to read or generate in your conversation or local workspace.
- **Advisory scope & verification trade-off:** Version 1.0 generates and validates configuration deliverables locally; it does not connect to or mutate live OrangeDAM instances. Tenant-specific details that depend on your Orange Logic subscription or release (such as custom Form Builder types beyond the 8 core workbook types, full Security Function internal keys, SAML/SCIM claim mappings, DNS/email relay records, and API/webhook endpoints) are marked `[VERIFY IN SANDBOX / OL DOCS]` and must be confirmed in a non-production Sandbox with Test Impersonation Accounts before Production rollout.
- **Credentials:** Do not paste live OrangeDAM passwords, API keys, or private tokens into configuration CSVs. Use synthetic data and safe placeholders.
- Full privacy policy: [docs/privacy.md](https://github.com/maretha-labs/orangedam-claude-plugin/blob/main/docs/privacy.md)

## Troubleshooting

- **Skill did not trigger automatically:** Mention "OrangeDAM" or "Orange Logic" along with the domain (for example, "permissions matrix", "embedded metadata", or "migration plan"), or invoke a skill directly by name (for example, `/maretha-orangedam-config:ol-security-permissions`).
- **Python validator path errors in Chat vs. Claude Code:** In Claude Code and Cowork, Claude runs scripts via `${CLAUDE_SKILL_DIR}/scripts/<script>.py`. In claude.ai Chat, Claude runs the relative path `scripts/<script>.py` inside the sandbox.
- **Platform-specific behavior:** Skills work in claude.ai Chat, Cowork, and Claude Code. The two specialist agents (`implementation-architect` and `security-permissions-auditor`) run in Cowork and Claude Code and are safely skipped in Chat.

## Support & security

- Documentation: [docs/index.md](https://github.com/maretha-labs/orangedam-claude-plugin/blob/main/docs/index.md)
- Issues & support: [GitHub Issues](https://github.com/maretha-labs/orangedam-claude-plugin/issues) or [https://maretha.io/contact](https://maretha.io/contact)
- Security vulnerabilities: Report privately through [https://maretha.io/contact](https://maretha.io/contact) (see `SECURITY.md`).
