# OrangeDAM Site Builder Brand Portal Blueprint

| Portal Name | Purpose / Use Case | Target Audience | Auth Mode (Public / SSO / Self-Reg) | Underlying DAM Folders / Collections | Rendition / Watermark Policy | Vanity URL / Path | Owner |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Brand Hub | Brand guidelines, logos, fonts, templates | All Employees & Agencies | SSO + Agency Login | `Library/Marketing/Brand Guidelines` | Unwatermarked `TR1` + `TRX` | `brand.example.com` | Brand Ops |
| Press Center | Public media kit & cleared photography | Press / Unregistered Visitors | Public (`*UnregisteredUsers`) | `Library/Photography/Published Photography` (`Public` only) | `TR1_COMP` / `TR1` (no raw originals) | `press.example.com` | PR Team |
| Partner Campaign Hub | Seasonal campaign downloads by region | Regional Distributors | Self-Registration (Admin Approved) | Regional Collections (`Public` / Partner VC) | Watermarked preview + Request for `TRX` | `partners.example.com` | Channel Mktg |

## Governance Checklist
- [ ] Every portal page pulls live DAM assets (zero duplicated static uploads)
- [ ] Portal permissions verified with a non-admin Test Account before publishing
- [ ] Expired/revoked assets automatically disappear from all portals
- [ ] Legal footer links (Terms, Privacy, Accessibility) included
