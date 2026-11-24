---
type: llm
---

PASS if the response:
1. Maps Title, Description, Asset Date, Usage Rights, Country, and City to OrangeDAM core fields (such as CoreField.title, CoreField.description, CoreField.Document-date, CoreField.Usage-rights, Geography.Country, Geography.City) and notes Asset Date is creation date, not upload date.
2. Uses "+=" for the controlled Brand field (Apply Tag only if it exists already) and "++=" for open Campaign tags (Create Tag if it does not exist), and requires a Tag Type / Authority List for controlled fields.
FAIL if it invents non-existent DataTable operators, omits Tag Type definitions for controlled dropdowns, or confuses Asset Date with upload date.
