# OrangeDAM Video Transcoding & Large-File Delivery Specification

## 1. Custom Transcode Presets

| Preset Name | Target Channel | Container / Codec | Resolution / FPS | Video Bitrate | Audio Spec | Trigger (On Upload / On Publish / Manual) | Size Category |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Social 1080p | Web / Social | MP4 (H.264) | 1920x1080 (source FPS) | 8 Mbps | AAC 192 kbps | On Publish | Large |
| Internal Review 720p | Browser Review | MP4 (H.264) | 1280x720 | 1.6 Mbps | AAC 96 kbps | On Upload | Medium |
| Archival Proxy | Long-Term Review | MP4 (H.264) | 1280x720 | 3 Mbps | AAC 128 kbps | On Upload | Medium |

## 2. MAM Feature Toggles
- [ ] Proxy video editing synced back to high-res masters
- [ ] Frame-accurate video scrubbing & time-coded annotations
- [ ] Audio/video subclip sharing (start/end range selection)
- [ ] Watermark preset applied on external video streams
- [ ] Large file (> 75 GB) transfer method: `Signiant` / `MASV` / `Orange Logic Tools` / `Clementine`

## 3. File Extension Waivers & Special Formats
- Extensions requiring waiver verification (`[VERIFY IN SANDBOX / OL DOCS]`): *(list extensions)*
- 3D model preview formats required: *(e.g., `.glb`, `.gltf`, `.obj`, `.fbx`)*
- ZIP archive policy: *(preserve as single asset vs. auto-extract)*
