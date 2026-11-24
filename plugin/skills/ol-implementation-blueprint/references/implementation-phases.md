# OrangeDAM New Implementation Dependency Map & Phasing

Standard Orange Logic Onboarding Workbook tabs and companion deliverables mapped to implementation order:

## Phase 0 — Pre-Kickoff Readiness
- Admin registration on Orange Logic Link & Foundations of OrangeDAM training (`ol-onboarding-kickoff`)
- Logos (transparent PNG ~500x500px <200KB + dark-mode variant), favicon spec (16x16 `.ico` ~1KB), vanity URL, outbound notification sender email, test asset bundle, homepage template, legal copy (Terms, Privacy, optional About Us & Accessibility)
- Initial Use Case Scenarios (`Tab 8`) & User Stories (`MVP` vs `Post-MVP`)

## Phase 1 — Information Architecture (Foundational)
1. **Object Model & Metadata Fields (`Tab 3`):** Review OOTB core fields, define custom namespaced fields, object type assignments (`Image`, `Video`, `Audio`, `Other (Multimedia)`, `Folder`, `Virtual Folder`), search/filter/mandatory flags, and DataTable V2.2 API column mappings (`ol-metadata-schema`).
2. **Tags & Authority Lists (`Tab 3 - Tags`):** Define Tag Types, hierarchical tag trees (Level 0..N), and controlled vs. open vocabulary rules (`ol-taxonomy-tags`).
3. **Embedded Metadata (`Tab 10`):** Map EXIF, IPTC, XMP, and ICC import/export priority rules and identify any COR picker option-list additions (`ol-embedded-metadata`).

## Phase 2 — Container & Access Model
4. **Folder Structure (`Tab 4`):** Design top-level and child folder hierarchy keeping every folder `<= 50,000` assets; plan Virtual Folders, Stacks, and Collections (`ol-folder-structure`).
5. **Visibility Classes (`Tab 5`):** Customize OOTB classes (`Pending Process`, `Public`, `Internal Use Only`, `Hidden`) and hex colors (`ol-security-permissions`).
6. **Groups & Security Functions (`Tab 6`):** Model `Security` vs. `Generic` groups, inheritance hierarchy, group admin ownership, feature-level Security Functions, and Test Impersonation Accounts (`ol-security-permissions`).
7. **Asset Formats (`Tab 9`):** Define rendition Size Categories (`Small`, `Medium`, `Large`, `Original`), format codes (`TR7`, `TR4`, `TR1_COMP`, `TR1_WATERMARKED`, `TR1`, `WebLow`, `WebHigh`, `TRX`), and watermarking fallbacks (`ol-formats-mam`).
8. **Permissions Matrix (`Tab 7`):** Bind `Folder/Asset x Group x Visibility Class x Subtype` to the 12 permission flags + inheritance settings (`ol-security-permissions`).

## Phase 3 — Experience, Workflows & Compliance
9. **Search, Filters, Workspaces & Site Builder Portals** (`ol-search-workspaces-branding`)
10. **Cart/Download Requests, Form Builder, Approvals, Tasks & Automated Emails** (`ol-workflows-approvals`)
11. **DRM, Restrictions, Embargoes, Ingest Integrity (Virus/MD5) & Regulatory Controls** (`ol-drm-compliance`)
12. **SSO, Registration Forms, Offboarding & Reporting** (`ol-identity-sso`)

## Phase 4 — Automation, Ecosystem & Cutover
13. **AI Services (Auto-Tag, OCR, STT, Face/Logo, BYO AI, Agentic AI)** (`ol-ai-automation`)
14. **Marketplace Connectors, Desktop Apps, APIs & Cloud Storage** (`ol-integrations-api`)
15. **Asset Migration Plan, Delta Cutover, Impersonation UAT & Go-Live** (`ol-migration-cutover`)

## Critical Cross-Domain Dependencies
- Metadata fields with dropdown/tag types depend on **Tag Types** existing first.
- Permissions depend on **Folders**, **Groups**, **Visibility Classes**, and **Asset Format Size Categories** existing first.
- Watermarked vs. clean download flows depend on **Asset Formats** (`TR1_WATERMARKED` in `Small` vs. `TR1` in `Medium`) + **Permissions** + **Cart Request Workflow**.
- Migration ingest depends on finalized **Metadata Schema**, **Embedded Metadata Mapping**, **Folder Structure**, and **Allowed File Extensions**.
