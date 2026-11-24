---
type: llm
---

PASS if the response:
1. Warns NOT to map embedded CreateDate into OrangeDAM record CreateDate (map to DocDate or a dedicated custom field).
2. Flags ExposureTime and FocalLength as Text (not Numeric) because ExifTool returns formatted values like "1/250" or "50.0 mm".
3. Notes LensModel is not in the default COR EXIF picker and must be added to EXIFFieldsOptionList.
4. Notes drop-frame timecode is MediaInfo-only (not exposed by ExifTool / COR).
FAIL if it recommends Numeric fields for ExposureTime/FocalLength or maps CreateDate directly into record CreateDate.
