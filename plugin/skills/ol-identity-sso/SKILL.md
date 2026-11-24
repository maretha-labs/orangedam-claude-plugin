---
name: ol-identity-sso
description: Configure Orange Logic (OrangeDAM) authentication, SAML/OAuth SSO, MFA, staff-only SSO enforcement, external self-registration forms, user provisioning and offboarding, external share-link expiration, impersonation governance, and usage reporting. Use when designing DAM identity, login security, or user lifecycle SOPs.
---

# OrangeDAM Identity, SSO, User Lifecycle & Reporting

Define clear authentication boundaries between internal employees, external partners/agencies, and anonymous portal visitors.

## Workflow

### Step 1: Architect Authentication & SSO Boundaries
Use `assets/sso-and-lifecycle-spec.md` to document:
- **Internal Staff Login:** Enforce **SSO-only login** (SAML 2.0 / OAuth / OIDC) for corporate email domains so internal users automatically inherit employee Security Groups and immediately lose access when deprovisioned in the corporate IdP.
- **External / Agency Accounts:** Decide between local OrangeDAM credentials with **MFA**, partner SSO, or one-time external links (zero account creation) for occasional approvers/downloaders.
- **Emergency Break-Glass Admin:** Maintain a documented break-glass `*SuperAdmin` recovery procedure outside IdP outages.
- **IdP Claim & Provisioning Mapping:** Map IdP groups/claims to OrangeDAM `Security` and `Generic` groups. *(`[VERIFY IN SANDBOX / OL DOCS]`: confirm exact SAML assertion attribute names, JIT account provisioning options, and SCIM availability with Orange Logic SSO documentation.)*

### Step 2: Configure Account Registration & Lifecycle SOPs
- **Self-Registration Form:** If external users self-register, specify required fields (Name, Organization, Email, Department/Sponsor, Intended Use) and admin approval routing (`ol-workflows-approvals`).
- **Offboarding & Account Deletion:** Define who can delete/deactivate accounts upon employee departure or privacy deletion requests (`GDPR`/`CCPA`) while preserving asset ownership and historical audit logs.
- **External Share Link Governance:** Set mandatory default expiration windows (e.g., 7/14/30 days) on share links sent to external agencies, and define link-revocation SOPs when agency contracts end.

### Step 3: Impersonation & Administrative Reporting Governance
- **Impersonation Controls:** Restrict `Authorize to impersonate as another user (Gives access to all assets)` strictly to `Administrator` / `*SuperAdmin`, and use dedicated **Test Accounts to Impersonate** (one per custom Security Group) for UAT rather than impersonating real executives.
- **Reporting Catalog:** Define recurring administrative reports—most viewed and downloaded assets, top search queries, zero-result searches, expiring assets, and download approval audit history.
