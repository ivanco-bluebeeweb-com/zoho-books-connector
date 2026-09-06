# Zoho Books Connector — Connector Discovery

## Official API Landscape
Zoho Books exposes a RESTful API v3 structured around standard double-entry bookkeeping entities:
- **Organizations:** Top-level tenancy container (`GET /organizations`).
- **Contacts / Customers:** Customer and vendor profiles (`GET/POST/PUT/DELETE /contacts`).
- **Invoices:** Accounts receivable sales invoices (`GET/POST/PUT/DELETE /invoices`).
- **Bills:** Accounts payable vendor bills (`GET/POST/PUT/DELETE /bills`).
- **Customer Payments:** Payments received against invoices (`GET/POST/PUT/DELETE /customerpayments`).
- **Bank Accounts:** Chart of accounts banking & cash accounts (`GET/POST/PUT/DELETE /bankaccounts`).
- **Tax Rates:** Tax authorities and tax percentages (`GET/POST/PUT/DELETE /settings/taxes`).

## Authentication & Authorization Architecture
- **Protocol:** OAuth 2.0 (Authorization Code Grant / Self-Client Tokens)
- **Header:** `Authorization: Zoho-oauthtoken <access_token>`
- **Scope required:** `ZohoBooks.fullaccess.all` (or granular `ZohoBooks.contacts.all`, `ZohoBooks.invoices.all`, etc.)
- **Organization Scoping:** All operations scoped to `organization_id`.

## Error Handling & Rate Limiting
- HTTP 401: Invalid or expired OAuth token; classified as `UNAUTHORIZED` with guidance to regenerate token.
- HTTP 403: Insufficient organizational permissions; classified as `FORBIDDEN`.
- HTTP 429: Zoho API daily/minute rate limit exceeded; extracts `Retry-After` and yields `RATE_LIMITED`.
- Secret Redaction: Tokens and sensitive payload headers are sanitized from all logged errors (Standard B8).
