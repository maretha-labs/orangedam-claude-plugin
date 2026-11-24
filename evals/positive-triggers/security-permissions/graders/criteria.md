---
type: llm
---

PASS if the response:
1. Uses OrangeDAM's OOTB Visibility Classes (Pending Process as upload default, Public, Internal Use Only, Hidden) and OOTB Groups (*Everyone, *UnregisteredUsers, *RegisteredUsers, Administrator).
2. Distinguishes Security groups from Generic department groups, includes Test Impersonation Accounts for UAT, and ensures Show Dwld Btn is paired with appropriate View tiers (S/M/L/Original).
3. Scopes External Agencies strictly to Public with watermarked Small/Medium previews + Request original file access.
FAIL if it grants Pending Process or write access to *UnregisteredUsers or omits Visibility Classes and Security Functions.
