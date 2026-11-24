# OrangeDAM Search, Filters & Workspaces Specification

## 1. Filters Sidepanel Configuration

| Display Order | Filter Category | Facet Field / Tag Type | Visible in Public Page? | Visible in Asset Mgmt? | Notes |
| :-: | :--- | :--- | :---: | :---: | :--- |
| 1 | Asset Basics | Asset Type (Image/Video/Audio/Doc) | Yes | Yes | Built-in |
| 2 | Classification | Content Type (Tag Type) | Yes | Yes | |
| 3 | Geography | Country / City | Yes | Yes | |
| 4 | Governance | Visibility Class | No | Yes | Staff/Admin only |
| 5 | Rights | Rights Status / Expiration | Yes | Yes | |

## 2. Search Settings
- Default sort order: `Relevance` (alternatives: `Asset Date`, `Upload Date`, `Filename`)
- Blank search enabled for: `Staff`, `Basic External User`, `Administrator`
- Saved & shared searches enabled for: `Staff`, `Administrator`
- NLP / semantic search & visual similarity enabled: `Yes` / `No`

## 3. Workspace Layout Matrix

| Workspace Name | Target Groups | Visible Metadata Fields | Primary Actions Exposed |
| :--- | :--- | :--- | :--- |
| Public Page | Basic External User, General Staff | Title, Description, Asset Date, Usage Rights, Copyright, Country, Tags | Search, Filter, Preview, Request/Download, Collections |
| Asset Management | Contributors, Advanced Users, Admins | All Core + Custom Fields + Admin Notes + Visibility Class | Upload, Batch Edit, Folder Nav, Stacks, Versioning, Permissions |
| Legal / Rights View | Legal Reviewers | Title, Usage Rights, Restrictions, Expiration, Talent Releases | Approve Requests, Set Restrictions, Audit Logs |
