---
name: ol-drm-compliance
description: Configure Orange Logic (OrangeDAM) Digital Rights Management (DRM), asset restrictions and embargoes, expiration automation, talent/model releases, ingest virus scanning and MD5 checksum/fixity controls, forensic watermarking, C2PA provenance, and regulatory compliance (ISO 27001, SOC 2, GDPR/CCPA, HIPAA, FINRA 4511/WORM, TX-RAMP, WCAG 2.2). Use when designing DAM rights enforcement or security/compliance governance.
---

# OrangeDAM Digital Rights Management (DRM), Restrictions & Compliance

Protect licensed, embargoed, and regulated assets through automated enforcement rather than manual spreadsheets.

## Workflow

### Step 1: Define Restrictions, Embargoes & Expiration Automation
Use `assets/drm-restrictions-policy-template.md` to specify:
- **Restriction Types:** Independent controls over asset **access**, **discoverability (search)**, **downloading**, and **sharing**. Ensure restricted assets are completely invisible/inaccessible to unauthorized groups.
- **Embargoes & Release Dates:** Pre-release assets stay restricted/hidden until scheduled release date, then transition automatically.
- **Expiration Dates:** Define expiration date fields + automated expiry rules (advance owner notifications at e.g. 30/7 days, automatic Visibility Class change to `Hidden` or restriction lock on expiry, blocking downloads/portal display).
- **Security Function Gate:** Restrict `Asset restrictions` management strictly to authorized Rights/Legal/Admin groups.

### Step 2: Model Talent Releases & Usage Rights Metadata
- Store signed model/talent releases, photographer agreements, and stock license contracts directly in OrangeDAM and link them to covered photo/video assets.
- Capture structured rights metadata: License Type (`Royalty-Free`, `Rights-Managed`, `Owned`), Permitted Channels (`Web`, `Print`, `Social`, `Broadcast`, `Internal`), Permitted Regions, Exclusivity, and Validity Window.
- Optional AI linkage: Use facial recognition to detect talent in photos/videos, tag talent records, and associate corresponding release contracts and expiration dates (`ol-ai-automation`).

### Step 3: Enforce Ingest Integrity & Content Authenticity
- **Virus Scanning on Ingest:** Require automated antivirus scan on every uploaded file with automatic rejection of infected files.
- **MD5 Checksum & Fixity:** Require checksum validation on upload (auto-rejecting corrupted transfers) plus ongoing fixity verification against bit rot.
- **Tamper-Proof Audit Trails & C2PA:** Enable cryptographic hashing and full audit logging (views, downloads, metadata edits, permission changes), forensic watermarking where leak deterrence is required, and **C2PA Content Credentials** tracking for media provenance and AI-manipulation detection.

### Step 4: Align with Regulatory Standards
Walk through `assets/compliance-checklist.md` to map organizational requirements to OrangeDAM capabilities:
- Security baseline: AES-256 at rest, TLS 1.2+ in transit, ISO/IEC 27001, SOC 2 Type II.
- Privacy: GDPR / CCPA (account deletion / data-subject handling + Privacy Policy page).
- Regulated verticals: HIPAA, **FINRA Rule 4511 / WORM** (Write Once Read Many archival storage), **TX-RAMP**, and **WCAG 2.2 / Section 508 (VPAT)** accessibility.
- Mark tenant-specific contract addenda, regional data-residency hosting, or WORM bucket provisioning as `[VERIFY IN SANDBOX / OL DOCS]`.
