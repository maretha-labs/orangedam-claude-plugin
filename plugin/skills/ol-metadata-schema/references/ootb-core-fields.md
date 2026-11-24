# OrangeDAM Out-of-the-Box Core Metadata Fields Reference

Verified from Orange Logic's standard Onboarding Workbook (`3. Object Model & Metadata Fields`):

| Field Name in OrangeDAM | Core Field Type | Tag Type | Public Page Default | Embedded Upload / Download Default | Orange Logic API Field Name | DataTable V2.2 Operator | Internal DB Note |
| :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| Original File Name | Text - Fewer than 500 characters | N/A | No | Filename / Filename | `Corefield.OriginalFileName` | `=` | Match/lookup key |
| Title | Text - Fewer than 500 characters | N/A | Yes | Headline / Headline | `CoreField.title` | `:=` | |
| Description | Long Text - No length limit | N/A | Yes | Caption (IPTC) / Caption (IPTC) | `CoreField.description` | `:=` | `CaptionLong` (`DO_DOCUMENTS_DbBO.FieldList.CaptionLong`) |
| Asset Date | Date | N/A | Yes | DateCreated (IPTC) / DateCreated (IPTC) | `CoreField.Document-date` | `:=` | File creation date, NOT upload date |
| Notes | Long Text - No length limit | N/A | No | N/A / N/A | `CoreField.Notes` | `:=` | `Admin` (`DO_DOCUMENTS_DbBO.FieldList.Admin`) |
| Usage Rights | Long Text - No length limit | N/A | Yes | N/A / N/A | `CoreField.Usage-rights` | `:=` | `Restrictions` (`DO_DOCUMENTS_DbBO.FieldList.Restrictions`) |
| Country | Multi-Valued Field - Apply Tag only if it exists already | Country | Yes | N/A (or IPTC/XMP rule) | `Geography.Country` | `+=` | Controlled vocabulary |
| City | Multi-Valued Field - Create Tag if it does not exist | City | Yes | N/A (or IPTC/XMP rule) | `Geography.City` | `++=` | Open vocabulary |
| Source | Single-Valued Field | Source Accounts | Yes | Byline (IPTC) / Byline (IPTC) | `CoreField.Creator` | `+:=` | Single-valued creator/source |
| Copyright | Text - Fewer than 500 characters | N/A | Yes | Copyright (IPTC) / Copyright (IPTC) | `CoreField.copyright` | `:=` | |
| Tags | Multi-Valued Field - Create Tag if it does not exist | Common | Yes | Keywords (IPTC) / Keywords (IPTC) | `CoreField.Keywords` | `++=` | Pipe-delimited in CSV (e.g., `architecture\|city`) |
| Orange Logic Unique Identifier | Text - Fewer than 500 characters | N/A | Yes | N/A / SpecialInstructions (IPTC) | `CoreField.unique-identifier` | `:=` | System unique ID (e.g., `CTL90568`) |

## Allowed Workbook Field Types (`DataValidation`)
1. `Text - Fewer than 500 characters`
2. `Long Text - No length limit`
3. `Multi-Valued Field - Create Tag if it does not exist`
4. `Multi-Valued Field - Apply Tag only if it exists already`
5. `Single-Valued Field`
6. `Date`
7. `Checkbox`
8. `Number`

## Object Types
`Image`, `Video`, `Audio`, `Other (Multimedia)`, `Folder`, `Virtual Folder`.
