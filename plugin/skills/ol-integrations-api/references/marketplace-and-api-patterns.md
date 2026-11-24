# OrangeDAM Marketplace Connectors, Desktop Apps & API Patterns

## 1. Pre-Built Integration Categories (Known Ecosystem)
| Category | Representative Connectors | Typical Direction |
| :--- | :--- | :--- |
| **Creative Tools** | Adobe CC (Premiere Pro, Photoshop, InDesign, Illustrator), Figma, Sketch | Bidirectional (browse/place + versioned save-back) |
| **CMS / Headless** | Adobe Experience Manager (AEM), Drupal, Contentful, Contentstack, Sanity.io | Outbound delivery / asset picker + where-used tracking |
| **PIM / eCommerce** | Akeneo, Salsify, Stibo | Bidirectional product-asset & metadata sync |
| **Cloud Watch Folders** | Dropbox, Box, SharePoint, Google Drive | Inbound auto-ingest / sync |
| **Video & Transfer** | Brightcove, Kaltura, Signiant, MASV | Outbound streaming / accelerated >75GB transfer |
| **Marketing & Social** | Salesforce Marketing Cloud, Slack, MailChimp, Facebook/YouTube/Social, Shutterstock | Outbound publishing, notifications, stock import |
| **Standards & Delivery** | CDN (e.g., AWS CloudFront), IIIF (deep-zoom image URLs) | High-speed global delivery |

## 2. Desktop Ecosystem
- **Orange Logic Tools** (including Fast Download)
- **Clementine**
- **Adobe CC Extensions / Panels**
- Required Security Functions: `Can download Orange Logic applications`, `Can use the Orange LogicTools application`, `Fast download with Orange Logic Tools application`.

## 3. Core API Surfaces
- **DataTable API V2.2:** `/API/DataTable/V2.2/Documents.<Type>.<Subtype>:CreateorUpdate?` — bulk CRUD, search queries, and CSV column mapping (`=`, `:=`, `+=`, `++=`, `+:=`).
- **iAPI:** High-volume bulk ingestion API for migrations and automated feeds.
- **REST API:** General object CRUD, Visibility Class management, workflow triggers, and downstream usage tracking.
- **`[VERIFY IN SANDBOX / OL DOCS]`:** Obtain tenant-specific Developer Portal URL, authentication method, endpoint schemas, rate limits, and webhook support directly from Orange Logic.
