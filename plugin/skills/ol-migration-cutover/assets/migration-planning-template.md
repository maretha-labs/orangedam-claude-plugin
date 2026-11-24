# OrangeDAM Asset Migration Planning Document

Complete one copy of Parts 1 and 2 for **each** source system being migrated.

## Source System: `[Insert Source System Name]`

### Part 1: Assets & Metadata
- **Total Volume (TB) & File Count:** *(e.g., 14.5 TB / 380,000 files)*
- **Breakdown by Asset Type:**
  - Images: *(count / %)*
  - Videos: *(count / %)*
  - Audio: *(count / %)*
  - PDFs / Documents: *(count / %)*
  - Design (PSD/AI/INDD): *(count / %)*
  - 3D Files: *(Yes/No — list extensions & count)*
  - ZIP Archives: *(Yes/No — list count & extraction policy)*
- **Embedded Metadata to Map (IPTC / XMP / EXIF):** *(Yes/No — link to `embedded_mappings.csv`)*
- **External Metadata to Map (Sidecar CSV / DB):** *(Yes/No — link to `metadata_fields.csv`)*
- **Complete List of File Extensions:** *(enumerate every extension; flag any requiring waiver `[VERIFY IN SANDBOX / OL DOCS]`)*
- **Source Cloud Hosting:** Cloud provider (`AWS` / `Azure` / `GCP` / `On-Prem`) + Region (`us-east-1`, etc.)
- **Target OrangeDAM Cloud & Region:** *(verify same-cloud / same-region alignment)*
- **Folder Structure Strategy:** Maintain vs. Refactor; **max assets in any single folder = `<= 50,000`**
- **Duplicate Detection Policy:** MD5 checksum / filename dedup rules on ingest

### Part 2: Timing & Cutover
- **Source System Access Loss / Decommission Date:** `YYYY-MM-DD`
- **Internal Deadlines & Dependencies:** *(e.g., campaign launches, agency cutoffs)*
- **MVP Launch Subset (Must be searchable Day 1):** *(define folders/date range/file count)*
- **Post-Launch Backfill Subset:** *(define archive scope)*
- **Will users continue creating/editing in source during migration?** `Yes` / `No`
  - *If Yes — Delta Cutover Strategy & Freeze Window:* *(specify incremental sync schedule + freeze start/end)*
- **Published External Links Requiring Updates/Redirects:** `Yes` / `No`
  - *If Yes — Remediation Plan:* *(CMS URL rewrite, redirect map, owner)*

### Part 3: Execution Plan (Implementation Lead & Orange Logic PM)
- **Ingest Method & Servers:** *(DataTable V2.2 / iAPI / S3 sync; primary vs. secondary ingest servers)*
- **Priority Queue Order:** *(MVP launch folders first)*
- **Responsibility Split (Customer vs. Implementation Partner vs. Orange Logic):** *(table)*
- **Risks & Mitigations:** *(extension waivers, accelerated migration cost options, >75 GB files, external link cutover)*
