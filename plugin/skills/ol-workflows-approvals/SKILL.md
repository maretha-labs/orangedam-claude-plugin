---
name: ol-workflows-approvals
description: Configure Orange Logic (OrangeDAM) download request and cart approval workflows, Form Builder intake/registration forms, creative review FlowSteps, external one-link and talent selects/kills approvals, project management views (Kanban/Calendar/Gantt), and automated email notifications. Use when designing DAM approvals, forms, tasks, or notification matrices.
---

# OrangeDAM Workflows, Forms, Approvals & Automated Notifications

Model end-to-end content operations inside OrangeDAM—from intake forms and download-request carts to multi-reviewer approvals and automated notifications.

## Workflow

### Step 1: Configure Download Request / Cart Workflows
Use `assets/workflow-blueprint-template.md` to design the asset request lifecycle:
- **Intended-Use Form:** Capture project name, channel (web/print/social), region, and duration when a user requests a restricted or unwatermarked asset.
- **Auto-Approve vs. Manual Routing:** Define conditional rules where low-risk intended uses auto-approve while sensitive/unlicensed uses route to Rights Admins.
- **Admin Review Capabilities:** Authorize, reject with reason, or **replace requested assets** with better-suited cleared alternatives; search past requests to reuse precedent; maintain full date/time/approver audit trails.
- **Requester Visibility:** Let Staff and General Users track request status (Pending / Approved / Rejected) and download authorized assets upon approval.

### Step 2: Design Custom Forms with Form Builder
Use `assets/form-builder-spec-template.md` for:
- **User Registration Forms** (capturing org, role, department, justification for new `*RegisteredUsers`).
- **Asset Usage Request Forms** and **Creative Brief / Intake Forms**.
- Define **conditional show/hide sections** (e.g., if Usage = "Print Publication", reveal Publication Name and Print Run fields) and post-submit automation (attach data to asset metadata or auto-create a workflow task).
- *(Note: `[VERIFY IN SANDBOX / OL DOCS]` exact available field types in your tenant's Form Builder beyond standard text/dropdown/date/checkbox/number/file upload.)*

### Step 3: Design Creative Review, Talent Approvals & Project Management
- **Annotations & Versioning:** Pair inline image/video/PDF/3D annotations with side-by-side version comparison so feedback stays tied to the exact iteration.
- **External One-Link Approvals:** Send external stakeholders (clients, agencies, talent reps) a secure one-time link requiring no full account (desktop + mobile + keyboard shortcuts), with an Approvals Dashboard comparing reviewers side-by-side.
- **Talent Selects / Kills Workflow:** Support `First Pick` / `Second Pick` / `Kill` ratings with optional **contractual rejection-rate caps** (e.g., max 20% kills).
- **Tasks, FlowSteps & Project Views:** Assign FlowSteps/tasks (`Assign FlowSteps to users`), set overdue escalation rules, and configure Kanban, Calendar, Gantt, Team Overview workload, and budget/resource tracking as needed.

### Step 4: Build the Automated Email Matrix
Populate `assets/email-notifications-matrix.csv` covering every event trigger, recipient group, sender address (from `ol-onboarding-kickoff`), subject/body governance, and opt-out rules.
