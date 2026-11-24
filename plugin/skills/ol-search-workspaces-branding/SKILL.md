---
name: ol-search-workspaces-branding
description: Configure Orange Logic (OrangeDAM) search experience, Filters Sidepanel facets, Public Page vs. Asset Management and custom department workspaces, homepage branding, and no-code Site Builder Brand Portals. Use when designing DAM search UX, role-based workspaces, brand microsites, or external partner portals.
---

# OrangeDAM Search, Workspaces, Branding & Site Builder Portals

Design intuitive discovery experiences for casual consumers, power-user librarians, and external brand-portal visitors.

## Workflow

### Step 1: Configure Search & Discovery
Use `assets/filters-and-workspaces-spec.md` to define:
- **Search Modes:** Free-text metadata search, Boolean modifiers (`AND`/`OR`/`NOT`), blank search (`Can run searches without criteria`), Recent/Saved/Shared Searches, Advanced Search additional conditions, visual & conceptual similarity, and OrangeAI NLP / semantic search.
- **Filters Sidepanel:** Group Tag-backed facets into clean **Filter Categories** (e.g., Brand, Content Type, Region, Rights Status, Visibility Class, Orientation/Format). Avoid exposing free-text fields as facets.
- **Results Display & Sorting:** Default and selectable sort orders (Relevance, Asset Date, Upload Date, Filename), quick hover preview without opening files, and zoom/media-player scrubbing controls.

### Step 2: Tailor Role-Based Workspaces
OrangeDAM supports distinct workspace experiences on the same repository:
- **Public Page Workspace:** Simplified layout with curated metadata (`Show in Public Page workspace = Yes`) for general internal/external consumers.
- **Asset Management Workspace:** Full folder tree (Browser Sidepanel), batch metadata editing, Visibility Class transitions, and asset administration for Contributors/Editors/Admins (`Access to Asset management`).
- **Department-Specific Workspaces:** Tailored dashboards and Detailed View layouts for Marketing, Creative, Legal, or IT so each team sees only relevant fields, tasks, and tools. *(Note: OrangeDAM prioritizes configuration over arbitrary frontend CSS/DOM rewrites; align expectations with built-in workspace layout controls.)*

### Step 3: Brand Homepage & Site Builder Microsites
Use `assets/portal-blueprint-template.md` to plan:
1. **Main DAM Branding:** Light/dark logos, brand color theme, vanity URL, hero banners/videos, and featured collections on the homepage.
2. **Site Builder Brand Portals (No-Code Microsites):**
   - **Common Portal Types:** Brand Guidelines Hub, Campaign/Product Launch Site, Partner/Franchisee Portal, Public Media Center / Press Archive.
   - **Live DAM Binding:** Every asset placed on a Site Builder page reflects the latest DAM version and automatically honors revocations, expirations, and underlying DAM permissions.
   - **Multi-Portal & Access Architecture:** Plan separate regional/brand/audience portals with their own branding, language, and auth mode (Public watermarked view, SSO, or self-registration).
