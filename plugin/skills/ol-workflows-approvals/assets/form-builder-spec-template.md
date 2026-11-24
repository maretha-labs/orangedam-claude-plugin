# OrangeDAM Form Builder Specification

## Form Metadata
- **Form Name:** *(e.g., Asset Usage Request / External Account Registration / Creative Brief)*
- **Trigger Point:** *(Cart Checkout / Registration Page / Standalone Intake)*
- **Target Audience:** *(All Registered Users / External Partners / Internal Staff)*
- **Post-Submit Action:** *(Attach to Asset Metadata / Create Workflow Task / Send Notification)*

## Field Specification

| Order | Field Label | Field Type | Required? | Conditional Show/Hide Rule | Target DAM Field / Output |
| :-: | :--- | :--- | :---: | :--- | :--- |
| 1 | Project / Campaign Name | Text (< 500 chars) | Yes | Always shown | Request metadata |
| 2 | Intended Usage Channel | Single-Valued Dropdown | Yes | Always shown | Auto-approval rule input |
| 3 | Publication Name | Text (< 500 chars) | Conditional | Show only when Channel = `Print` | Request metadata |
| 4 | Target Territory | Multi-Valued Dropdown | Yes | Always shown | Rights verification |
| 5 | Usage End Date | Date | Yes | Always shown | Expiration check |
| 6 | Rights Acknowledgement | Checkbox | Yes | Always shown | Audit trail |
