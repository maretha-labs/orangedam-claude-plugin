# OrangeDAM Default Asset Formats Reference (Onboarding Workbook Tab 9)

| Asset Type | Name | Size / Spec | Format Code | Size Category | Downloadable Default | Notes |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- |
| Image | Thumbnail - Small | 192px fixed height | `TR7` | Small | No | Displayed in Search Results |
| Image | Thumbnail - Medium | 352px fixed height | `TR4` | Small | No | Displayed in Search Results |
| Image | Low Resolution | 800px x 800px | `TR1_COMP` | Small | Yes | |
| Image | Medium Res. Watermarked | 1200px x 1200px @ 75% | `TR1_WATERMARKED` | Small | Yes | Detail tab fallback when user lacks Medium permission |
| Video | Web Low | 320x240, 192kbps H.264 / 64kbps AAC | `WebLow` | Small | Yes | |
| Audio | Web streaming | MP3 128kbps | `Web` | Small | Yes | |
| Image | Medium Resolution | 1200px x 1200px @ 75% | `TR1` | Medium | Yes | Unwatermarked; falls back to `TR1_WATERMARKED` |
| Video | Web High / Streaming (720p) | 1280x720, 1600kbps H.264 / 96kbps AAC | `WebHigh` | Medium | Yes | Displayed on MainScreen Details tab |
| Image | Large Res. Comp. | Optional custom size | *(Custom)* | Large | Yes | Optional tier |
| Video | HD | Optional custom HD preset | *(Custom)* | Large | Yes | Optional tier |
| Image | High Res | Original file | `TRX` | Original | Yes | Master binary |
| Video | High Res | Original file | `TRX` | Original | Yes | Master binary |
| Audio | Original | Original file | `TRX` | Original | Yes | Master binary |
| Multimedia | Original | Original file | `TRX` | Original | Yes | Master binary |

> **Default Fallback Rule:** If a specific Asset Type does not have a Format Code, OrangeDAM defaults its Size Category to `Large`.
