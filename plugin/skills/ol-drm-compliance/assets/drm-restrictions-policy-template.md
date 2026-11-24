# OrangeDAM DRM, Restrictions & Embargo Policy Template

## 1. Restriction Tiers

| Tier | Trigger / Condition | Discoverable in Search? | Preview Allowed? | Download Allowed? | External Share Allowed? | Who Can Override? |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| Embargoed | Current Date < Release Date | Internal Prod Only | Watermarked | No | No | Rights Admin |
| Rights-Managed | Licensed talent/stock asset | Yes | Watermarked (`TR1_WATERMARKED`) | Via Approved Cart Request | No | Rights Admin |
| Expired | Current Date > Expiration Date | Admin Only (`Hidden`) | Admin Only | Blocked | Revoked | Legal / Admin |
| Legal Hold | Litigation / Compliance hold | Legal & Admin Only | Legal & Admin Only | Audited Only | Blocked | Legal Admin |

## 2. Expiration & Release Automation Rules
- Advance warning schedule: `60 days`, `30 days`, `7 days` before `Expiration Date`.
- Action on expiration: Change Visibility Class to `Hidden`, revoke active external share links, remove from Site Builder portals, notify Asset Owner & Rights Admin.
- Talent release linkage: Link release PDF/contract record to all covered photo/video assets via Asset Relationships (and optional facial recognition tagging).
