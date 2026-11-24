---
name: ol-folder-structure
description: Design and validate Orange Logic (OrangeDAM) folder hierarchies, virtual folders, Stacks, Asset Relationships, and Collections while enforcing the 50,000-assets-per-folder guideline and permission inheritance boundaries. Use when planning DAM folder trees, migrating legacy directory structures, or organizing creative projects in OrangeDAM.
---

# OrangeDAM Folder Hierarchy, Virtual Folders, Stacks & Collections

Architect a maintainable OrangeDAM container model that balances clean permission inheritance, metadata searchability, and performance.

## Workflow

### Step 1: Choose the Primary Folder Taxonomy Pattern
Evaluate the organization's access boundaries before drawing levels (parent folders pass settings and permissions down to child folders):
- **Department-Based Tree:** `Library -> Marketing Department -> Campaigns`, `Library -> PR Department -> Press Kits`. Best when department access isolation is the dominant rule.
- **Project / Show / Production Tree:** `Library -> Film Projects -> Show A -> Season 1`, `Library -> Photography -> Published Photography`. Best for media/entertainment and campaign production teams.
- **Lifecycle / Hybrid Tree:** Separate top-level `Library` (published/governed content) from `Draft Collateral` (department work-in-progress containers) so permissions stay simple and predictable.

### Step 2: Enforce OrangeDAM Performance & Structural Rules
Populate `assets/folder-structure-template.csv` and enforce:
1. **50,000-Asset Ceiling:** Orange Logic recommends **not exceeding 50,000 assets per individual folder** for performance reasons. Partition high-volume folders by year/quarter, season, campaign, or brand sub-folder.
2. **Shallow, Permission-Aligned Depth:** Aim for 2-5 levels; use metadata + Tags (not deep nested folders) for descriptive attributes that slice across departments.
3. **Folder Metadata & Unique Identifiers:** Every created folder has a Unique Identifier and can carry metadata (including mandatory fields required when creating a new folder).

### Step 3: Decide When to Use Non-Folder Containers
Avoid duplicating binary files across multiple folders by assigning the right OrangeDAM construct:
- **Virtual Folders:** Cross-cutting logical groupings when assets belong to multiple initiatives without duplicating storage.
- **Stacks:** Automatically link multiple assets sharing the same filename with different extensions (e.g., `shoot_001.jpg` + `shoot_001.cr3` + `shoot_001.psd`). Ensure target groups receive the `Can see deployed stacks` Security Function.
- **Asset Relationships:** Define hierarchical (parent/child master-to-derivative) and non-hierarchical (related campaign assets) links.
- **Collections:** Ad-hoc or project lightboxes (unlimited assets), re-sequencing, internal/external sharing, and PDF contact-sheet export.

### Step 4: Validate the Folder Tree CSV
Run the folder validator on the populated CSV:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_folder_tree.py" <folders.csv>
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/validate_folder_tree.py folders.csv
  ```
Fix every `ERROR` (folders exceeding 50,000 projected assets, skipped hierarchy levels, duplicate sibling names) before building the Permissions Matrix.
