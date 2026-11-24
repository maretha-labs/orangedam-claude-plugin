# OrangeDAM COR Default Embedded Metadata & Native Field Reference

## 1. Native Auto-Populated Fields (Do NOT Create COR Mapping Rules)
| Datapoint | Native OrangeDAM Field | Notes |
| :--- | :--- | :--- |
| File size | `FileSize` | Auto-populated on ingest |
| MD5 checksum | `FileMD5` | Auto-populated on ingest |
| ICC profile description | `ColorProfile` | Auto-populated on ingest |
| Duration / timecode | `Duration`, `DocDuration`, `StartTimecode` | Auto-populated on ingest |
| Bitrates (overall/video/audio) | `BitRate`, `VideoBitRate`, `AudioBitRate` | Auto-populated on ingest |
| Frame rate / Aspect ratio | `FrameRate`, `DisplayAspectRatio` | Auto-populated on ingest |
| Codecs & audio specs | `VideoFormat`, `AudioFormat`, `AudioSamplingRate`, `AudioBitDepth`, `MainAudioTrackChannels` | Auto-populated on ingest |
| GPS coordinates | `Latitude`, `Longitude` | Confirm fills natively; fallback XMP `-exif:GPSLatitude` / `-exif:GPSLongitude` |

## 2. Standard Default Import Mapping Highlights (IPTC & XMP)
| Source Type | Exact COR Source Key | Standard Destination |
| :--- | :--- | :--- |
| IPTC | `Application2_Headline` | `Title` / `Headline` |
| IPTC | `Application2_Caption` | `Description` |
| IPTC | `Application2_Keywords` | `Tags` (Tag Type: `Common`) |
| IPTC | `Application2_Copyright` | `Copyright` |
| IPTC | `Application2_Byline` | `Source` |
| IPTC | `Application2_City` | `Keyword_City` |
| IPTC | `Application2_CountryName` | `Keyword_Country` |
| IPTC | `Application2_ProvinceState` | `Keyword_State` |
| IPTC | `Application2_DateCreated` | `DocDate` (Asset Date) |
| XMP | `-dc:Creator` | `Source` |
| XMP | `-dc:Description` | `Description` |
| XMP | `-photoshop:DateCreated` | `DocDate` |
| XMP | `-photoshop:City` / `Country` / `State` | `Keyword_City` / `Keyword_Country` / `Keyword_State` |
| EXIF | `DateTimeOriginal` | `DocDate` (Priority 1) |
| EXIF | `Make`, `Model`, `FNumber`, `ExposureTime`, `ISO`, `FocalLength` | In COR default EXIF picker |

## 3. Common Tags Requiring Option-List Extension
- **Add to `EXIFFieldsOptionList`:** `LensModel`, `LensID`, `SerialNumber`, `ExposureMode`, `ExposureCompensation`, `WhiteBalance`, `SceneCaptureType`, `AudioChannelLayout`, `ColorSpaceData`, `RenderingIntent`, `ProfileCopyright`.
- **Add to `XMPFieldsOptionList_ClientSpecific`:** `-aux:Lens`, `-aux:SerialNumber`, `-GPano:ProjectionType`, `-GSpherical:ProjectionType`, `-crs:HasCrop`, `-crs:ProcessVersion`.

## 4. Non-ExifTool / Unmappable Without Custom Development
- MediaInfo-only: Drop-frame TC, PsF segmented frames, PCM byte order, audio track ID/profile/bitrate mode/compression mode/default/forced/delay.
- Binary blobs: `MakerNotes:*` (camera vendor proprietary groups).
