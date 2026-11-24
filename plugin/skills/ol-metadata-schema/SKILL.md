---
name: ol-metadata-schema
description: Design and validate an Orange Logic (OrangeDAM) Object Model and Metadata Fields specification, including out-of-the-box core fields, custom namespaced fields, field types, Authority Lists, object type assignments, filter/search/mandatory flags, and DataTable API V2.2 mapping operators. Use when creating or reviewing a DAM metadata schema or migrating metadata CSVs into OrangeDAM.
---

# OrangeDAM Object Model & Metadata Schema

Design a clean, searchable, DataTable-ready OrangeDAM metadata schema grounded in Orange Logic's Onboarding Workbook Tab 3 conventions.

## Workflow

### Step 1: Start from Out-of-the-Box Core Fields
Consult `references/ootb-core-fields.md` before inventing custom fields. Reuse OrangeDAM's built-in core fields whenever the business concept matches (`Original File Name`, `Title`, `Description`, `Asset Date`, `Notes`, `Usage Rights`, `Country`, `City`, `Source`, `Copyright`, `Tags`, `Orange Logic Unique Identifier`).

Key semantic distinctions:
- **Asset Date (`CoreField.Document-date`):** Date the file/content was created — **not** the upload date.
- **Notes (`CoreField.Notes` / `Admin`):** Internal administrative notes; normally hidden from Public Page workspace (`Show in Public Page = No`).
- **Usage Rights (`CoreField.Usage-rights` / `Restrictions`):** Rights/licensing summary exposed to consumers.

### Step 2: Define Custom Fields & Namespacing
Start from `assets/metadata-fields-template.csv`. For every custom field, specify:
1. **Field Name in OrangeDAM** and **Field Name in CSV** (source column header if migrating).
2. **Custom API Namespace** (for custom fields, use consistent dot-separated naming like `<org_ns>.<domain>.<FieldName>`).
3. **Field Type** (8 standard Onboarding Workbook types):
   - `Text - Fewer than 500 characters`
   - `Long Text - No length limit`
   - `Multi-Valued Field - Create Tag if it does not exist`
   - `Multi-Valued Field - Apply Tag only if it exists already`
   - `Single-Valued Field`
   - `Date`
   - `Checkbox`
   - `Number`
   *(Note: Form Builder supports additional field types beyond these 8 core workbook types — `[VERIFY IN SANDBOX / OL DOCS]` before promising specialized types like linked/paired multi-value composites.)*
4. **Tag Type (Authority List):** Required for every `Single-Valued` or `Multi-Valued` dropdown/tag field; `N/A` for free text/dates/numbers/checkboxes.
5. **UX & Search Flags:**
   - `Add to Filter Sidepanel` (`Yes`/`No` — prefer Tag/controlled fields; avoid high-cardinality free text)
   - `Show in Public Page workspace?` (`Yes`/`No`)
   - `Searchable` (free-text search index)
   - `Advanced Search` (Additional Conditions)
   - `Mandatory` (required before saving metadata / uploading / creating folders)
6. **Embedded Mapping Hints:** `Map from Embedded Metadata on Upload` and `Map to IPTC / XMP Field on Download` (hand off detailed priority rules to `ol-embedded-metadata`).
7. **Object Type Assignments:** `Image`, `Video`, `Audio`, `Other (Multimedia)`, `Folder`, `Virtual Folder` — plus indicate if metadata-only records (no binary file) are needed.
8. **Advanced Requirements:** Note multi-language metadata needs, paired/linked values (e.g., Person + Role), batch-edit workflows, and metadata copy workflows.

### Step 3: Populate DataTable API V2.2 Mapping Columns
For CSV/API bulk import readiness, verify each row's DataTable API mapping:
- **Base API:** `/API/DataTable/V2.2/Documents.<Type>.<Subtype>:CreateorUpdate?`
- **Operators:**
  - `=` — exact lookup/match key (e.g., `Corefield.OriginalFileName`)
  - `:=` — set/overwrite scalar value (`Title`, `Description`, `Asset Date`, `Notes`, `Usage Rights`, `Copyright`, `Unique Identifier`)
  - `+=` — add controlled tag only if it already exists (`Multi-Valued - Apply Tag only if it exists already`)
  - `++=` — add tag and create if missing (`Multi-Valued - Create Tag if it does not exist`)
  - `+:=` — set single-valued controlled tag/source (`Single-Valued Field`)
- **CSV Column Label:** Wrap source column header in brackets, e.g., `[Title]`.

### Step 4: Run Deterministic Validation
Validate the metadata schema CSV before moving to taxonomies or permissions:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_metadata_schema.py" <metadata_fields.csv>
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/validate_metadata_schema.py metadata_fields.csv
  ```
Resolve every `ERROR` and review all `WARN` items (such as enabling Filter Sidepanel on free-text fields).
