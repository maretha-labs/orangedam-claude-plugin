# OrangeDAM DataTable API V2.2 & Bulk Mapping Template

> **Verification Note:** Confirm exact tenant base URL, authentication header format, and custom subtype names against your Orange Logic Developer Portal before executing requests (`[VERIFY IN SANDBOX / OL DOCS]`). Never commit live bearer tokens or passwords to this document.

## 1. Endpoint Pattern
```text
POST https://<your-tenant-domain>/API/DataTable/V2.2/Documents.<ObjectType>.<Subtype>:CreateorUpdate
```

## 2. Standard Operator Reference
| Operator | Behavior | Typical Field Type |
| :---: | :--- | :--- |
| `=` | Exact match / lookup key | `Corefield.OriginalFileName`, Unique ID |
| `:=` | Set or overwrite scalar value | Text, Long Text, Date, Number, Checkbox |
| `+=` | Append controlled tag (only if tag already exists) | Multi-Valued (Controlled Authority List) |
| `++=` | Append tag and create if missing | Multi-Valued (Open Vocabulary) |
| `+:=` | Set single-valued controlled tag / account | Single-Valued Field (e.g., `CoreField.Creator`) |

## 3. Sample Field Mapping Expression
```text
Corefield.OriginalFileName=[Original File Name]
&CoreField.title:=[Title]
&CoreField.description:=[Description]
&CoreField.Document-date:=[Asset Date]
&Geography.Country+=[Country]
&Geography.City++=[City]
&CoreField.Creator+:=[Source]
&CoreField.Keywords++=[Tags]
```
*(Multi-valued CSV cells use pipe `|` delimiting, e.g., `architecture|city`.)*
