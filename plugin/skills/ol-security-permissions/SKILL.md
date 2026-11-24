---
name: ol-security-permissions
description: Design and audit Orange Logic (OrangeDAM) Security Groups, Generic Groups, Visibility Classes, Security Functions, Test Impersonation Accounts, and Folder/Asset Permissions matrices across S/M/L/Original renditions and 12 permission flags. Use when architecting or auditing DAM access control, least-privilege security, or group inheritance.
---

# OrangeDAM Security Model: Groups, Visibility Classes, Security Functions & Permissions

Architect OrangeDAM's four-layer access control model cleanly and audit it for privilege leaks or broken user workflows before configuring Sandbox.

## The Four Security Layers (Read `references/ootb-groups-and-security-functions.md`)

1. **Visibility Classes (`assets/visibility-classes-template.csv`):** Color-coded asset lifecycle labels controlling who sees an asset before and after publication.
   - OOTB defaults: `Pending Process` (`#f7ca18`, **default on newly uploaded/created assets**), `Public` (`#40d650`), `Internal Use Only` (`#4d6b8a`), `Hidden` (`#a4b2bd`).
   - Add custom classes (with hex codes) only when distinct access or lifecycle states require them (e.g., `Legal Hold`, `Expired`).
2. **Groups (`assets/groups-template.csv`):**
   - OOTB groups: `*Everyone`, `*UnregisteredUsers`, `*RegisteredUsers`, `*SuperAdmin` (full unrestricted access; needs no extra grants), `Administrator`.
   - **`Security` vs. `Generic` Account Types:** `Security` groups carry feature-level Security Functions (e.g., `Staff`, `Editor`, `Contributor`); `Generic` groups organize departments/teams for folder permissions without duplicating Security Functions (e.g., `Marketing`, `Public Relations`).
   - **Inheritance:** Child groups inherit Security Functions, Permissions, and Restrictions from Parent Groups.
   - **Delegated Admin & Test Impersonation Accounts:** Specify "Who can add/remove users for this group" AND provision a dedicated **Test Account to Impersonate** for every custom group so UAT verifies exact real-world access.
3. **Security Functions (`assets/security-functions-template.csv`):**
   - Control *what UI features/actions* a user can invoke (`Full`, `None`, `Read`, `Edit`, `Delete`, `New`, `List`) across Browse, Search, Download, Upload, Share & Collaborate, and Manage/Admin.
   - **Public Homepage Login-Wall Rule:** To push anonymous visitors directly to login instead of a public homepage, configure `Can access to the web site` **and** ensure `VPage_VPage.Data.UseAccessToWebSiteSecurity` is enabled.
   - Mark any tenant-specific Security Function internal keys beyond the standard Onboarding Workbook list as `[VERIFY IN SANDBOX / OL DOCS]`.
4. **Permissions Matrix (`assets/permissions-matrix-template.csv`):**
   - Controls *what assets* a group can see and do, scoped by `On Folder / Asset`, `Group`, `Visibility Class` (blank = all), and `On Subtypes` (blank = all).
   - **12 Permission Flags:** `View Small (S)`, `View Med (M)`, `View Large (L)`, `View Original`, `Show Dwld Btn`, `Find`, `Share Own Access`, `Edit`, `Add / Upld`, `Delete`, `Move`, `Admin` (grants all permissions + permission management).
   - Plus container propagation: `Apply to contained assets` and `Inherit permissions from parent(s)`.
   - **Download Rule:** `Show Dwld Btn` downloads the **highest-quality format** the user has View permission for — it does nothing useful without at least one View permission (`S`/`M`/`L`/`Original`).

## Workflow

1. Review OOTB defaults in `references/ootb-groups-and-security-functions.md`.
2. Populate `visibility_classes.csv`, `groups.csv`, `security_functions.csv`, and `permissions.csv` from the templates in `assets/`.
3. Write complex permissions in plain English first ("`[Group]` can `[actions]` on `[Folder]` when Visibility Class is `[Class]`"), then translate to rows.
4. Run the deterministic security auditor:
   - In Claude Code / Cowork:
     ```bash
     python3 "${CLAUDE_SKILL_DIR}/scripts/audit_permissions.py" --groups <groups.csv> --permissions <permissions.csv> --visibility <visibility_classes.csv>
     ```
   - In claude.ai Chat sandbox:
     ```bash
     python3 scripts/audit_permissions.py --groups groups.csv --permissions permissions.csv --visibility visibility_classes.csv
     ```
5. Resolve every `ERROR` (circular group inheritance, download button without View permission, write access or non-Public Visibility Class exposed to `*Everyone`/`*UnregisteredUsers`) and review all `WARN` items before Sandbox rollout.
