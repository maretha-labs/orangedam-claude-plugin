---
name: ol-migration-cutover
description: Plan and validate an Orange Logic (OrangeDAM) asset migration from legacy DAMs or cloud storage (Box, SharePoint, Dropbox, Google Drive, Nuxeo, or custom repositories), covering per-source volume and extension inventories, cloud-region alignment, embedded vs. external metadata mapping, 50K/folder constraints, delta cutover, published link updates, and impersonation UAT. Use when planning DAM migration or go-live cutover.
---

# OrangeDAM Asset Migration, Ingest & Go-Live Cutover

Build a complete, risk-checked Orange Logic Asset Migration Plan and Group-by-Group UAT Cutover Plan aligned with Orange Logic's standard Asset Migration Planning Document.

## Workflow

### Step 1: Complete Per-Source Asset & Metadata Inventory
Populate `assets/migration-planning-template.md` **separately for every source system** being migrated:
1. **Volume & Counts:** Total storage (TB) and total file count, plus breakdown by asset type (images, videos, audio, PDFs, Office, Adobe, 3D, ZIP — exact counts or percentages).
2. **Metadata Sources:**
   - **Embedded metadata** (IPTC/XMP/EXIF inside files -> cross-check `ol-embedded-metadata`).
   - **External metadata** (CSV/database fields stored outside files -> cross-check `ol-metadata-schema` & DataTable V2.2 / `iAPI`).
3. **File Extensions Audit:** Full list of all file extensions present in the source; check against Orange Logic's supported/prohibited list and flag any requiring a **waiver or special config**; explicitly call out **3D files** and **ZIP archives**.
4. **Cloud Storage Alignment:** Record whether source files live in AWS, Azure, or GCP and the **exact region**. Same-cloud / same-region placement dramatically lowers egress cost and speeds ingest.
5. **Folder Structure & Deduplication:** Decide whether to preserve or refactor the existing folder tree while strictly respecting OrangeDAM's **50,000 assets per individual folder** recommendation; plan duplicate-file detection on upload and ingest queue monitoring.

### Step 2: Plan Timing, Ingest Phasing & Delta Cutover
Document every operational constraint:
- **Source Cutoff Date:** Exact date access to the legacy system expires, plus internal campaign/launch deadlines.
- **MVP Launch Subset:** Minimum subset of assets that **must** be searchable on Day 1 vs. archival history eligible for post-launch backfill.
- **Ingest Servers & Acceleration:** Primary vs. secondary ingest server allocation and whether accelerated migration cost options are required.
- **Live-Source Delta Cutover:** If users continue creating/editing content in source systems after bulk migration begins, define the delta sync cadence, final content-freeze window, and cutover verification checksum/count reconciliation.
- **Published External Links:** Inventory all external websites, CMS pages, or partner links pointing to legacy asset URLs and define the URL-update or redirect plan.

### Step 3: Validate the Migration Plan
Create a structured JSON summary of the migration plan (or pass `--json` spec generated from the interview) and run the deterministic validator:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_migration_plan.py" <migration_plan.json>
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/validate_migration_plan.py migration_plan.json
  ```
Fix every `ERROR` (missing cutoff date, folder exceeding 50,000 files, live source without delta cutover strategy, published links without redirect plan, unreviewed 3D/ZIP/prohibited extensions).

### Step 4: Build Group-by-Group Impersonation UAT & Go-Live Checklist
Populate `assets/uat-impersonation-test-plan.csv` so every custom Security Group from `ol-security-permissions` is exercised in Sandbox via its dedicated **Test Account to Impersonate** before Production cutover.
