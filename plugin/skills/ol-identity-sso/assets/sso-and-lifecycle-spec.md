# OrangeDAM Identity, SSO & User Lifecycle Specification

## 1. Authentication Matrix

| User Population | Auth Method | MFA Required? | Login Wall Behavior | Group Assignment Method |
| :--- | :--- | :---: | :--- | :--- |
| Internal Staff (`@example.com`) | Corporate SAML 2.0 / OIDC SSO (SSO-only) | Enforced by IdP | Redirect to SSO login | IdP group claims `[VERIFY IN SANDBOX / OL DOCS]` |
| External Agencies / Partners | Local OrangeDAM account (or invited) | Yes | Login required | Admin-assigned (`Basic External User` / `External Contributor`) |
| One-Time External Approvers | Secure expiring approval link | N/A | Scoped to assigned assets only | Anonymous / Link-scoped |
| Public Portal Visitors (if enabled) | Anonymous (`*UnregisteredUsers`) | N/A | Public Portal / `Public` VC only | `*UnregisteredUsers` |

## 2. IdP Group-to-OrangeDAM Group Mapping (`[VERIFY IN SANDBOX / OL DOCS]`)

| IdP Group / Claim Value | OrangeDAM Group | Notes |
| :--- | :--- | :--- |
| `DAM-Admins` | `Administrator` | Full admin + reporting |
| `DAM-Staff-Contributors` | `Staff - Contributor` | Upload & metadata edit |
| `DAM-Staff-Users` | `Staff` | Standard internal access |
| `Dept-Marketing` | `Marketing` (Generic) | Department WIP folder access |

## 3. Lifecycle & Governance Policies
- **External share-link default expiration:** `14 days` (max `30 days`; revocable anytime).
- **Employee offboarding SLA:** Immediate IdP revocation + quarterly inactive-account review; account deletion SOP verified for privacy requests.
- **Impersonation policy:** Restricted strictly to `Administrator`; UAT performed via Test Accounts.
- **Usage reporting cadence:** Monthly views/downloads + zero-result search review by DAM Admins.
