---
name: ol-embedded-metadata
description: Configure and audit Orange Logic (OrangeDAM) embedded metadata import/export mapping rules for EXIF, IPTC, XMP, and ICC tags, including fallback priority chains (OrderNumber), COR default picker coverage, EXIFFieldsOptionList and XMPFieldsOptionList_ClientSpecific additions, and ExifTool vs. MediaInfo pitfalls. Use when mapping embedded file metadata on upload or download.
---

# OrangeDAM Embedded Metadata Mapping (EXIF, IPTC, XMP, ICC)

Configure accurate bidirectional embedded metadata mapping rules in OrangeDAM without duplicating native system fields or breaking ExifTool extraction.

## Workflow

### Step 1: Filter Out Native & Unmappable Datapoints First
Consult `references/cor-default-iptc-xmp-exif.md` before creating rules:
1. **Already native in OrangeDAM (create NO import template row):**
   - Audio/Video tech specs: `AudioSamplingRate`, `Duration`, `DocDuration`/`StartTimecode`, `BitRate`/`VideoBitRate`, `AudioBitRate`, `FrameRate`, `DisplayAspectRatio`, `VideoFormat`, `AudioFormat`, `AudioBitDepth`, `MainAudioTrackChannels`.
   - File & color basics: `ColorProfile` (profile description), `FileSize`, `FileMD5`, `Latitude`/`Longitude` *(confirm GPS populates on instance; add `-exif:GPSLatitude` / `-exif:GPSLongitude` fallback rows only if missing)*.
2. **Not mappable via ExifTool / COR (needs dev or leave in raw metadata):**
   - MediaInfo-only video/audio flags: drop-frame timecode, PsF segmented frames, PCM endianness, audio track ID/format profile/bitrate mode (CBR/VBR)/compression mode/default/forced/delay.
   - `MakerNotes:*` vendor binary blobs (Canon, Nikon, Sony, etc.) — no single scalar tag.

### Step 2: Build Prioritized Fallback Chains (`OrderNumber`)
Start from `assets/embedded-mapping-template.csv` and assign explicit integer `Priority (OrderNumber)` per destination field when multiple standards can supply the same value:
- Example (`DocDate` / Asset Date):
  - Priority `1`: `EXIF` -> `DateTimeOriginal`
  - Priority `2`: `XMP` -> `-photoshop:DateCreated`
  - Priority `3`: `IPTC` -> `Application2_DateCreated`
- Example (`Keyword_City` / `Keyword_Country` / `Keyword_State`):
  - Priority `1`: `IPTC` (`Application2_City`, `Application2_CountryName`, `Application2_ProvinceState` — COR defaults)
  - Priority `2`: `XMP` (`-photoshop:City`, `-photoshop:Country`, `-photoshop:State`)

### Step 3: Identify Option-List Extensions
Flag every rule whose source tag is **not** in the default COR picker:
- **Missing EXIF / Composite / ICC tag:** Action = `Add to EXIFFieldsOptionList` (e.g., `LensModel`, `SerialNumber`, `ExposureMode`, `WhiteBalance`, `FOV`, `ColorSpaceData`, `AudioChannelLayout`).
- **Missing XMP tag:** Action = `Add to XMPFieldsOptionList_ClientSpecific` (e.g., `-aux:Lens`, `-aux:SerialNumber`, `-GPano:ProjectionType`, `-GSpherical:ProjectionType`, `-crs:*`).
- **IPTC:** Fixed `Application2_*` list; verify exact `Application2_` key name.

### Step 4: Enforce Technical Mapping Guardrails
1. **Never map embedded `CreateDate` to OrangeDAM's record `CreateDate`** (record creation timestamp). Map to `DocDate` or a dedicated custom field like `<ns>.capture.CreateDateEmbedded`.
2. **Use `Text`, not `Numeric`, for formatted ExifTool tags:** `ExposureTime` (`1/250`), `FocalLength` (`50.0 mm`), `FocalLengthIn35mmFormat`, and `ExposureCompensation` (`+1/3`) return formatted strings.
3. **Disambiguate EXIF vs. Lightroom XMP bare names:** `Contrast`, `Saturation`, and `Sharpness` exist in both ExifIFD and `XMP-crs`; use `-ExifIFD:Contrast` (etc.) when explicit camera-only extraction is required.
4. **Never map `FileSource` (camera/scanner device type) to Cortex `Source` (`CoreField.Creator`).**
5. **VR / 360° projection:** Map both Priority 1 `-GPano:ProjectionType` (images) and Priority 2 `-GSpherical:ProjectionType` (video).

### Step 5: Validate Mapping Rules
Run the deterministic mapping validator on the CSV:
- In Claude Code / Cowork:
  ```bash
  python3 "${CLAUDE_SKILL_DIR}/scripts/validate_embedded_mappings.py" <embedded_mappings.csv>
  ```
- In claude.ai Chat sandbox:
  ```bash
  python3 scripts/validate_embedded_mappings.py embedded_mappings.csv
  ```
Fix every `ERROR` and verify sample files from `ol-onboarding-kickoff` in Sandbox after loading rules.
