# Zoho Books Connector — Authentication & Credentials Standard (B1–B10)

## Compliance Audit
- **B1 (Explicit Credentials):** Requires explicit `auth_token` and `organization_id`.
- **B2 (Encrypted Storage):** Credentials saved exclusively in Imperal Secrets vault (`zoho_books_connections`).
- **B3 (Masked Exposure):** Secrets masked in UI/logs (`zoho…1234`).
- **B4 (One-Click Revocation):** `disconnect_zoho_books` clears stored credentials immediately.
- **B5 (Least Privilege):** Scopes documented for user clarity (`ZohoBooks.fullaccess.all`).
- **B6 (Proactive Validation):** `verify_auth()` executes harmless `GET /organizations` verification call before saving.
- **B7 (Multi-Datacenter / Region):** Full support for US, EU, IN, AU, JP, CA, SA datacenters.
- **B8 (Secret Sanitization):** Error classifier catches and redacts tokens/auth headers from all error strings.
- **B9 (Multi-Account Scoping):** Explicit `connection_id` on every tool allows switching between accounts/organizations.
- **B10 (Scope Degradation):** Informative error messaging when permissions are missing.
