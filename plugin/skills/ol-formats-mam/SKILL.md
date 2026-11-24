---
name: ol-formats-mam
description: Configure Orange Logic (OrangeDAM) asset formats, Small/Medium/Large/Original rendition tiers (TR7, TR4, TR1_COMP, TR1_WATERMARKED, TR1, WebLow, WebHigh, TRX), watermarking fallbacks, custom video transcoding presets, proxy video editing, file extension waivers, and >75GB large-file transfer. Use when designing DAM derivatives, watermarks, or video/MAM pipelines.
---

# OrangeDAM Asset Formats, Watermarking & MAM / Video Pipelines

Map every rendition tier cleanly to OrangeDAM's four permission size categories (`Small`, `Medium`, `Large`, `Original`) and configure scalable video/MAM processing.

## Workflow

### Step 1: Map Standard Rendition Codes to Permission Tiers
Consult `references/default-asset-formats.md` and customize `assets/asset-formats-template.csv`:
- **How Permissions bind to Formats:** Permissions (`View Small`, `View Med`, `View Large`, `View Original`) govern access by **Size Category**, and `Show Dwld Btn` delivers the highest-quality downloadable format in the user's granted tier.
- **Fallback Rule:** If an Asset Type has **no** Format Code assigned, OrangeDAM uses **Large** as its Size Category.
- **Watermarking Pattern (`TR1` vs. `TR1_WATERMARKED`):**
  - `TR1_WATERMARKED` (1200x1200 @ 75%, watermarked) lives in **Small**.
  - `TR1` (1200x1200 @ 75%, unwatermarked) lives in **Medium** and automatically falls back to `TR1_WATERMARKED` for users lacking `View Med`.
  - Pair this with `Request original file access` so general/external users preview and download watermarked Small renditions while submitting cart requests for clean `TRX` originals.

### Step 2: Configure Video & MAM Workflows
Use `assets/transcode-presets-template.md` to specify:
1. **Streaming Proxies:** Baseline `WebLow` (320x240, H.264/AAC) and `WebHigh` (1280x720, H.264/AAC) for in-browser playback and Asset Management Details tab preview.
2. **Custom Transcoding Presets:** Channel-specific bitrates, codecs, resolutions, and containers triggered on upload or publish (e.g., social 1080p MP4, web HLS, broadcast mezzanine).
3. **Proxy Video Editing & Collaboration:** Lightweight browser proxy trims synced back to high-res masters, frame-accurate scrubbing, time-coded video annotations, and subclip sharing (sharing specific start/end ranges of audio/video).
4. **Auto-Cropping & Custom Download Specs:** Decide which groups receive `Can download files with cropping option`, `User can download images in custom format`, and `Can modify watermark presets`.
5. **Forensic & Dynamic Watermarking:** Define visible preview watermarks vs. forensic tracking watermarks for pre-release or embargoed media.

### Step 3: Govern File Extensions, 3D/ZIP & Large File Transfer
- Audit every file extension against Orange Logic's supported/prohibited extension list and flag any requiring a **waiver or special config** (`[VERIFY IN SANDBOX / OL DOCS]`: verify current supported/prohibited extensions in Orange Logic Help Center).
- Document special handling for **3D models** (in-browser 3D preview & annotation) and **ZIP archives**.
- For files **> 75 GB** (upload or download), configure UDP-accelerated transfer connectors (**Signiant**, **MASV**) and/or Orange Logic desktop apps (**Orange Logic Tools**, **Fast Download**, **Clementine**).
