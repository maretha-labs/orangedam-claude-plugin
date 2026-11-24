# OrangeDAM Ingest Integrity & Compliance Checklist

| Control Area | Requirement | OrangeDAM Capability / Action | Status | Verification Notes |
| :--- | :--- | :--- | :---: | :--- |
| Ingest Security | Virus check on all uploads | Auto-scan + auto-reject failing files | [ ] | Verify with EICAR test file in Sandbox |
| File Integrity | Checksum validation on upload | MD5 validation + auto-reject corrupted uploads + periodic fixity checks | [ ] | Confirm `FileMD5` native population |
| Encryption | Data at rest & in transit | AES-256 at rest, TLS 1.2+ in transit | [ ] | Confirm in OL security package |
| Audit Logging | Tamper-proof event history | Log views, downloads, metadata edits, approvals, impersonations | [ ] | Define log retention & export schedule |
| Provenance | Content authenticity / AI tracking | Enable C2PA Content Credentials & cryptographic hashing | [ ] | Confirm C2PA retention on download |
| Watermarking | Deter leaks on pre-release media | Preview + optional forensic watermarking | [ ] | Test with external account |
| Privacy | GDPR / CCPA compliance | Publish Privacy Policy; define account deletion & DSAR SOP | [ ] | Align with Legal |
| Archival | FINRA Rule 4511 / WORM (if regulated) | Configure WORM immutable storage tier | [ ] | `[VERIFY IN SANDBOX / OL DOCS]` |
| Public Sector / Healthcare | HIPAA / TX-RAMP (if applicable) | Confirm BAA / cloud compliance tier | [ ] | `[VERIFY IN SANDBOX / OL DOCS]` |
| Accessibility | WCAG 2.2 / Section 508 | Review OL VPAT + publish optional Accessibility Policy | [ ] | Verify custom branding color contrast |
