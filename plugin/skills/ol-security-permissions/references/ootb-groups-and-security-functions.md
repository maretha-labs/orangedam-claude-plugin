# OrangeDAM Out-of-the-Box Groups, Visibility Classes & Security Functions Reference

## 1. Out-of-the-Box Security Groups
| Group | Type | Default Parent | Role |
| :--- | :--- | :--- | :--- |
| `*Everyone` | Security | None | Includes both `*UnregisteredUsers` and `*RegisteredUsers` |
| `*UnregisteredUsers` | Security | `*Everyone` | Anonymous visitors / unauthenticated share-link recipients |
| `*RegisteredUsers` | Security | `*Everyone` | Automatically includes all registered accounts |
| `*SuperAdmin` | Security | None | Full platform access; needs no additional Permissions or Security Functions |
| `Administrator` | Security | None | Full access to Asset Management and Administration |

## 2. Out-of-the-Box Visibility Classes
| Visibility Class | Default Hex | Default Purpose |
| :--- | :---: | :--- |
| `Pending Process` | `f7ca18` | Default Visibility Class assigned to newly created or uploaded assets |
| `Public` | `40d650` | Assets cleared for broad / external availability |
| `Internal Use Only` | `4d6b8a` | Assets restricted to internal staff |
| `Hidden` | `a4b2bd` | Assets hidden from general groups (Admin-only visibility) |

## 3. Core Security Functions Catalog (Onboarding Workbook Tab 6)
| Category | Capability | Related OrangeDAM Security Functions / Notes |
| :--- | :--- | :--- |
| **Browse** | Public homepage vs. login wall | `Can access to the web site` (must first enable `VPage_VPage.Data.UseAccessToWebSiteSecurity`) |
| **Browse** | Browse assets | `Can access the Public Workspace in Media Management`, `Can access More on hover`, `Access to thumbnails view` |
| **Search** | Search / Blank / Recent / Saved / Advanced | `Search asset`, `Can run searches without criteria`, `Access to the recent search`, `Access to the saved search`, `Access to the advanced search` |
| **Search** | View stacked assets | `Can see deployed stacks` |
| **Download** | Direct download | Permissions-based (`Show Dwld Btn` + View tier) |
| **Download** | Request restricted download | `Request original file access` |
| **Download** | Custom crop / custom specs / watermarks | `Can download files with cropping option`, `User can download images in custom format`, `Can download assets with watermark option`, `Can modify watermark presets` |
| **Upload** | Upload / Versioning / Invite | `Can upload files in Orange Logic`, `Show action button File versioning`, `Can invite others to upload` |
| **Share & Collab** | Internal & external share | `Can Share assets`, `Send Link`, `Can Create Share Links For...` (to restrict anonymous sharing) |
| **Share & Collab** | Collections, PDF, Comments, Annotations | `Collections`, `Re-Sequence "collections" images`, `Copy collection to another user`, `Can print images from search results and collections`, `Access user comments on assets`, `Annotations on assets`, `Can view video annotations` |
| **Manage** | Asset Management Workspace | `Access to Asset management`, `Change workspace in the asset management screens` |
| **Manage** | Permissions, Metadata, Layouts, Visibility, Restrictions | `View permissions`, `View shares`, `Asset details`, `Image details`, `Tag`, `Edit detailed view layout`, `Document Visibility Class`, `Asset restrictions` |
| **Manage** | Taxonomy & Tags | `Asset Tags`, `Tags batch import / export`, `Tag Facet Categories`, `Tag restrictions`, `Tag templates`, `Tag tree`, `Tag tag types`, `Merge Tags`, suggest ("To Be Vetted") |
| **Manage** | Automated AI Services | `Can auto-tag images`, `Facial recognition for images`, `Optical character recognition Service`, `Allow to send assets to speech to text recognition` |
| **Manage** | Desktop Apps | `Can download Orange Logic applications`, `Can use the Orange LogicTools application`, `Fast download with Orange Logic Tools application` |
| **Admin** | Backend, Reports, Impersonation, Restore | `Access to the system backend menu`, `report` functions, `Authorize to impersonate as another user (Gives access to all assets)`, `Can view and restore deleted assets` |
