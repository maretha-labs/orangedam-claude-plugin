---
name: ol-onboarding-kickoff
description: Prepare pre-kickoff deliverables and baseline tenant settings for a new Orange Logic (OrangeDAM) implementation, including site logos, dark-mode logo, favicon spec, vanity URL, outbound notification email, representative test assets, homepage template, legal pages, and admin training readiness. Use before kickoff or during Week 1-2 onboarding.
---

# OrangeDAM Pre-Kickoff Readiness & Tenant Baseline

Help customer DAM administrators prepare every baseline asset and decision required during Weeks 1-2 of a new OrangeDAM implementation.

## Pre-Kickoff Deliverable Checklist

Walk the user through `assets/kickoff-checklist.md` and produce a completed readiness tracker with owners and due dates:

1. **Admin Training:** Register all Customer DAM Admins on Orange Logic **Link** and complete the free *Foundations of OrangeDAM* course prior to finalizing the Onboarding Workbook.
2. **Site Header Logo (Light & Dark Mode):**
   - Transparent PNG, approximately **500 x 500 px**, ideally **< 200 KB**.
   - Provide a dedicated **dark-mode** logo variant if the primary logo has low contrast on dark backgrounds.
3. **Favicon:** `.ico` file, recommended **16 x 16 px** at approximately **1 KB**.
4. **Vanity URL & Site Name (Optional):**
   - Must be on a domain owned by the customer (e.g., `dam.example.com`).
   - Record DNS/IT owner and target go-live date. `[VERIFY IN SANDBOX / OL DOCS]`: confirm exact CNAME target and TLS certificate provisioning steps with Orange Logic infrastructure team.
5. **Outbound Notification Sender Email:**
   - Dedicated address displayed as sender on asset expiration alerts, account registration emails, download approvals, and workflow notifications (e.g., `dam-notifications@example.com`).
   - `[VERIFY IN SANDBOX / OL DOCS]`: confirm required SPF/DKIM/DMARC DNS records with Orange Logic mail engineering before cutover.
6. **Representative Test Asset Bundle:**
   - Use `assets/test-asset-matrix-template.csv` to assemble at least one real sample of **every file extension** planned for upload (images, RAW, video codecs, audio, PDFs, Office, Adobe, 3D, ZIP), plus candidate **homepage hero images/videos**.
   - Verify embedded IPTC/XMP/EXIF test payloads are present on representative photography/video samples.
7. **Homepage Template Selection:** Pick a starting homepage template (requires Link login) and define featured collections, quick-search prompt, and branding colors.
8. **Legal & Governance Pages:**
   - **Required:** Terms & Conditions language; Privacy Policy.
   - **Optional:** About Us (text copy or hyperlink); Accessibility Policy.
9. **Onboarding Workbook & Migration Plan Head Start:** If filling out pre-kickoff, prioritize **Metadata Fields** and **Folder Structure** tabs first, plus **Asset Migration Planning Doc** source inventories.
10. **Support, Release & Training Governance:** Confirm how admins will track Orange Logic past/planned release timelines, submit support tickets/feature requests, and record training sessions.

## Output Expectations

Deliver:
1. A populated Pre-Kickoff Readiness Tracker (`assets/kickoff-checklist.md` filled in with Status, Owner, Target Date, and Blockers).
2. A Test Asset Sample Matrix (`assets/test-asset-matrix-template.csv`) covering every planned extension.
3. A short list of IT/Legal handoff actions (DNS/Vanity URL, Outbound Email Auth, Legal Copy sign-off).
