---
name: ol-integrations-api
description: Architect Orange Logic (OrangeDAM) ecosystem integrations, pre-built marketplace connectors (Adobe CC, Figma, CMS, PIM, cloud watch folders, CDN/IIIF, Signiant/MASV), desktop apps, DataTable API V2.2 and iAPI bulk patterns, and SaaS/hybrid/on-prem cloud storage topologies. Use when connecting OrangeDAM to an enterprise martech stack or planning API integrations.
---

# OrangeDAM Integrations, APIs, Desktop Tools & Cloud Topology

Position OrangeDAM as the single source of truth across creative tools, CMS/PIM platforms, cloud storage, CDNs, and custom API consumers.

## Workflow

### Step 1: Inventory Ecosystem Integrations
Consult `references/marketplace-and-api-patterns.md` and populate `assets/integration-inventory-template.csv`:
- **Creative Suites:** Adobe Creative Cloud panels (Premiere Pro, Photoshop, InDesign, Illustrator — pull assets directly, save back as new versions), Figma, Sketch.
- **CMS, Headless & Delivery:** AEM, Drupal, Contentful, Contentstack, Sanity.io (`NPM` Asset Browser plugin), CDN fronting (e.g., CloudFront), and **IIIF** deep-zoom image URLs.
- **PIM, eCommerce & Marketing:** Akeneo, Salsify, Stibo, Salesforce Marketing Cloud, Slack, MailChimp, Social Media publishing (e.g., scheduled posts + engagement tracking), Shutterstock one-click licensed import.
- **Cloud Storage / Watch Folders:** Automated ingestion from Dropbox, Box, SharePoint, or Google Drive (e.g., external agency uploads to a watch folder -> OrangeDAM auto-ingests).
- **Video & Large Transfer:** Brightcove, Kaltura, Signiant, MASV.
- **Desktop Tools:** Plan rollout and Security Functions (`Can download Orange Logic applications`, `Orange LogicTools`, `Fast download`, `Clementine`) for power users.

### Step 2: Architect API & Data Synchronization Patterns
Use `assets/datatable-api-mapping-template.md` when designing programmatic integrations:
- **REST API & Discovery:** OrangeDAM exposes an API-first REST/JSON architecture for CRUD, search, Visibility Class edits/queries, workflow triggers, and **asset usage / where-used tracking** across downstream publication locations.
- **DataTable API V2.2:** Bulk record queries and CSV/JSON `CreateorUpdate` operations (`/API/DataTable/V2.2/Documents.<Type>.<Subtype>:CreateorUpdate?` with `=`, `:=`, `+=`, `++=`, `+:=`).
- **iAPI (Bulk Ingestion API):** High-volume automated ingest and spreadsheet-driven batch loads during migration or recurring feeds.
- **Webhooks / Event Callbacks & Auth:** `[VERIFY IN SANDBOX / OL DOCS]` — confirm official Orange Logic Developer Portal URL, OAuth/token auth flow, rate limits, and native webhook/event payload specifications before writing production integration code. Never embed real API keys or tokens in templates or repo files.

### Step 3: Align Cloud, Storage & Tiered Archival Topology
- **Deployment Model:** SaaS (default), Hybrid (sensitive assets on-prem + cloud scalability), or On-Premises.
- **Cloud Provider & Region:** Align OrangeDAM cloud storage backend (AWS S3, Azure Blob, or GCP Cloud Storage) with existing source storage and regional data-residency rules.
- **Tiered Archival & DR:** Define lifecycle rules moving cold archival masters automatically to low-cost storage (e.g., AWS Glacier), geo-redundancy/failover expectations, and CDN caching strategy.
