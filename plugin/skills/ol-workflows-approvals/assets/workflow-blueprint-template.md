# OrangeDAM Workflow & Approval Blueprint

## 1. Download Request / Cart Workflow
- **Trigger:** User clicks "Request Access" on view-only or watermarked asset (`Request original file access`).
- **Intake Form:** Intended Use, Channel (Web/Print/Broadcast/Social), Territory, Campaign Dates.
- **Auto-Approval Rules:** *(e.g., Internal presentation + `Public` Visibility Class -> Auto-Approve)*
- **Manual Approval Queue:** Routes to `Rights Administrators` group; supports Approve, Reject, or Replace Asset.
- **SLA & Escalation:** Reminder at 48 hours; escalate to Backup Admin at 72 hours.
- **Audit Retention:** Retain requester, approver, timestamp, intended use, and decision permanently.

## 2. Asset Ingestion & Publication Approval (FlowSteps)
1. **Upload:** Asset enters `Pending Process` Visibility Class (`#f7ca18`).
2. **Metadata & QC Task:** Auto-assigned to `Staff - Contributor` / `Metadata Librarian` (mandatory fields enforced).
3. **Creative / Legal Review:** Inline annotations + side-by-side version comparison.
4. **Publish:** Approved asset transitions to `Internal Use Only` or `Public`; rejected asset returns with comments.

## 3. External / Talent Selects Workflow (If Applicable)
- Delivery method: Secure one-time external approval link (no login required, desktop/mobile).
- Rating scheme: `1st Pick` / `2nd Pick` / `Kill`.
- Contractual Kill Limit: *(e.g., 20% max rejects per shoot, or N/A)*.
- Multi-reviewer reconciliation: Compare unanimous approvals vs. conflicts in Approvals Dashboard.
