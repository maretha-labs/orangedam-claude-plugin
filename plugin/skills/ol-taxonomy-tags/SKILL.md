---
name: ol-taxonomy-tags
description: Design and validate Orange Logic (OrangeDAM) Tag Types, Authority Lists, hierarchical taxonomy trees, controlled vs. open vocabulary rules, and "To Be Vetted" tag governance workflows. Use when structuring dropdown lists, keyword hierarchies, or taxonomy maintenance policies for OrangeDAM.
---

# OrangeDAM Taxonomy, Tags & Authority Lists

Structure controlled vocabularies and hierarchical tag trees cleanly so OrangeDAM filters, dropdowns, and metadata governance scale without tag sprawl.

## Core Concepts (OrangeDAM Terminology)

- **Tags:** Reusable terms applied either as generic keywords (on the asset Tags tab) or as dropdown options bound to metadata fields.
- **Tag Type:** Category organizing a set of Tags (OOTB defaults include `Common`, `Country`, `City`, `Source Accounts`).
- **Authority List:** One or more Tag Types linked in a metadata field's settings to populate its dropdown values.

## Workflow

### Step 1: Partition Vocabularies into Tag Types
For every controlled or multi-valued field from `ol-metadata-schema`, assign a dedicated **Tag Type**:
- Keep broad descriptive keywords in `Common`.
- Isolate structured facets (e.g., `Regional Offices`, `Brand`, `Content Type`, `Campaign`, `Language`, `Department`) into distinct Tag Types so Filter Sidepanel facets remain clean and unambiguous.

### Step 2: Build Hierarchical Tag Trees
Populate `assets/tag-tree-template.csv` using `Tag Type (Category)` plus `Tag Term Level 0` .. `Tag Term Level 3`:
- Ensure every child term has a non-empty parent level above it (no skipped levels like Level 0 -> Level 2).
- Keep naming consistent (singular vs. plural, casing, no trailing spaces, avoid pipe `|` inside term names because `|` is the standard CSV multi-value delimiter in OrangeDAM imports).

### Step 3: Choose Vocabulary Enforcement & Governance Rules
For each Tag Type, document:
1. **Enforcement Mode:**
   - **Controlled (`Apply Tag only if it exists already`, DataTable `+=`):** Best for Brand, Country, Legal Status, Department, Rights Tier.
   - **Open (`Create Tag if it does not exist`, DataTable `++=`):** Best for freeform `Common` tags or fast-moving `City` / event lists.
2. **Governance & Security Functions:**
   - **Suggest terms ("To Be Vetted"):** Grant contributors suggest permission while restricting final creation/editing/merging to Taxonomy Admins / Librarians.
   - **Cascading edits:** Editing a taxonomy term automatically updates applied assets across the DAM.
   - **Admin operations to scope via Security Functions:** `Asset Tags`, `Tags batch import / export`, `Tag Facet Categories`, `Tag restrictions`, `Tag templates`, `Tag tree`, `Tag tag types`, `Merge Tags`.
3. **External Taxonomy Integration (Optional):** If syncing with external taxonomy managers (e.g., PoolParty / SKOS), mark exact import format `[VERIFY IN SANDBOX / OL DOCS]`.

### Step 4: Validate the Tag Tree CSV
Run the validator on the populated tag tree CSV:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_tag_tree.py" <tags.csv>
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/validate_tag_tree.py tags.csv
  ```
Fix all `ERROR` findings (orphaned hierarchy levels, duplicate sibling paths, illegal delimiters) before import.
