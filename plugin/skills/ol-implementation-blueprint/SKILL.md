---
name: ol-implementation-blueprint
description: Plan a complete new Orange Logic (OrangeDAM) implementation end to end, run stakeholder discovery, prioritize MVP vs. Post-MVP use cases and user stories, sequence configuration dependencies, assemble an Onboarding Workbook handoff package, or run a cross-domain integrity audit across configuration CSVs. Use when kicking off a new OrangeDAM project or auditing a multi-tab configuration package.
---

# OrangeDAM Implementation Blueprint & Cross-Domain Audit

Guide teams from Day 0 discovery to a validated, handoff-ready Orange Logic (OrangeDAM) Onboarding Workbook package.

## Workflow

### Step 1: Discovery & Scope Intake
Collect the minimum viable context before proposing configuration tables:
1. **Organization & personas:** Internal departments, external agencies/partners, public/unregistered visitors, and admin roles.
2. **Asset mix & scale:** File types (images, video, audio, PDFs, Office, Adobe, 3D, ZIP), total volume (TB), file count, largest file size, and projected growth.
3. **Hosting & cloud alignment:** SaaS vs. Hybrid vs. On-Premises; cloud provider/region (AWS, Azure, GCP) relative to existing asset storage.
4. **Core operational needs:** Search/browse, download approval carts, watermarking, DRM/expirations, video MAM/transcoding, Brand Portals (Site Builder), SSO, AI auto-tagging, external integrations (Adobe CC, CMS, PIM, cloud storage), and legacy migration deadline.
5. **Compliance posture:** ISO 27001 / SOC 2, GDPR/CCPA, HIPAA, FINRA Rule 4511 / WORM, TX-RAMP, WCAG 2.2 / VPAT, C2PA provenance.

### Step 2: Sequence the Implementation in Dependency Order
Consult `references/implementation-phases.md` and build the implementation plan in strict dependency order so downstream tables never reference undefined objects:
1. **Kickoff & Use Cases** (`ol-onboarding-kickoff`, plus `assets/use-cases-template.csv` & `assets/user-stories-template.csv`)
2. **Information Architecture** (`ol-metadata-schema` -> `ol-taxonomy-tags` -> `ol-embedded-metadata`)
3. **Storage & Security Model** (`ol-folder-structure` -> `ol-security-permissions` -> `ol-formats-mam`)
4. **Experience & Governance** (`ol-search-workspaces-branding` -> `ol-workflows-approvals` -> `ol-drm-compliance` -> `ol-identity-sso`)
5. **Automation, Ecosystem & Launch** (`ol-ai-automation` -> `ol-integrations-api` -> `ol-migration-cutover`)

### Step 3: Capture Use Cases & User Stories
Start from `assets/use-cases-template.csv` and `assets/user-stories-template.csv`:
- Assign stable IDs (`UC-1`, `US-1`) linking each User Story (`As a... / I want... / So that...`) to its parent Use Case.
- Tag every item as `MVP` (launch blocker) or `Post-MVP`.
- Record OrangeDAM compatibility tier (`Out-of-the-box` or `Configurable (Light)` for verified standard capabilities; flag complex custom rules as `[VERIFY WITH OL PM]` before quoting effort).
- Ensure Group names referenced in Use Cases match the Groups table verbatim.

### Step 4: Validate Cross-Domain Integrity
Once configuration CSVs exist in a directory (e.g., `metadata_fields.csv`, `tags.csv`, `folders.csv`, `visibility_classes.csv`, `groups.csv`, `permissions.csv`), run the deterministic cross-domain validator:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_workbook.py" <config-dir>
  ```
- In claude.ai Chat sandbox (relative path):
  ```bash
  python3 scripts/validate_workbook.py <config-dir>
  ```
Fix every reported `ERROR` (missing Tag Types, undefined Groups/Folders/Visibility Classes in Permissions, broken download/view combinations, folders exceeding 50,000 assets) before handoff.

### Step 5: Assemble the Onboarding Handoff Package
Generate a consolidated Markdown handoff index summarizing all domain CSVs, open verification items, and Test vs. Prod promotion sign-off:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/assemble_onboarding_package.py" <config-dir> --output <config-dir>/ONBOARDING_HANDOFF.md
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/assemble_onboarding_package.py <config-dir> --output ONBOARDING_HANDOFF.md
  ```

## Guardrails

- **Never fabricate undocumented OrangeDAM UI paths or API endpoints:** Mark tenant-specific unknowns `[VERIFY IN SANDBOX / OL DOCS]` with the concrete question for Orange Logic.
- **No live credentials:** Never store passwords, bearer tokens, or private keys in CSVs or handoff documents.
- **Test vs. Prod discipline:** Track every configuration change with owner initials, date, and target environment (`Test` first, verified via Test Impersonation Accounts, then `Prod`).
