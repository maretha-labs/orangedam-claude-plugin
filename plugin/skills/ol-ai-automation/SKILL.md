---
name: ol-ai-automation
description: Configure Orange Logic (OrangeDAM) AI services and automation governance, including image auto-tagging layered with controlled taxonomies, OCR, speech-to-text transcription and speaker ID, facial and brand-logo recognition, NLP/visual search, Bring Your Own AI providers, and Agentic AI Studio workflows. Use when scoping DAM AI features, cost controls, or AI permission gating.
---

# OrangeDAM AI Services & Automation Governance

Design practical, cost-controlled, rights-compliant AI configurations for OrangeDAM.

> **Scope Note:** This skill configures OrangeDAM platform settings and governance policies only. It never invokes AI image, video, or audio generation models.

## Workflow

### Step 1: Select & Scope Automated AI Services
Populate `assets/ai-services-governance-matrix.csv` across OrangeDAM's core AI capabilities:
1. **Image Auto-Tagging + Taxonomy Layering:** Enable AI object/scene/color tagging on upload, then chain automation rules that map broad AI keywords onto controlled taxonomy terms or target collections (preventing uncontrolled tag clutter).
2. **OCR (Optical Character Recognition):** Extract searchable text from scanned PDFs, slides, and images.
3. **Video Speech-to-Text & Captions:** Auto-generate searchable transcripts/captions and optional speaker Voice ID tagging.
4. **Facial Recognition & Brand Logo Detection:** Detect people or logos frame-by-frame in photos/videos to enable person search and automate talent release / DRM linkage (`ol-drm-compliance`). *Verify privacy/biometric consent laws (e.g., GDPR/BIPA) with Legal before enabling facial recognition.*
5. **NLP Semantic & Visual Similarity Search:** Enable plain-language search and "visually/conceptually similar" asset discovery.
6. **Intelligent Automation:** Auto-cropping into channel aspect ratios, auto-transcoding, auto-watermarking unlicensed assets, and auto-routing based on AI classification.

### Step 2: Evaluate Built-In vs. Bring Your Own AI (BYO AI)
- Decide whether to use OrangeDAM's built-in AI connectors or plug in **Bring Your Own AI** (AWS Rekognition, Google Vision, Azure Cognitive Services, or custom enterprise vision/NLP APIs).
- Specify which asset subtypes and folders trigger AI automatically on ingest vs. **manual on-demand execution** (critical for controlling per-minute video STT and per-image vision API costs during bulk migrations!).

### Step 3: Configure Agentic AI Studio & GenAI Governance
- **Agentic AI Studio:** Document candidate repeatable multi-step workflows (e.g., product photo upload -> auto-tag -> create creative brief task -> route for review) with explicit human-in-the-loop approval checkpoints.
- **GenAI Governance (If Enabled in Tenant):** Define which approved input assets may be used, require **C2PA Content Credentials** tagging on derived media, and clarify legal sign-off rules. *(`[VERIFY IN SANDBOX / OL DOCS]`: confirm exact Agentic AI Studio and GenAI feature availability and licensing tier on the customer's tenant.)*

### Step 4: Gate Access via Security Functions
Assign AI execution Security Functions intentionally (`Can auto-tag images`, `Facial recognition for images`, `Optical character recognition Service`, `Allow to send assets to speech to text recognition`) so only authorized groups trigger metered AI processing.
