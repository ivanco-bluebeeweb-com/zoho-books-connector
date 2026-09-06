# Zoho Books Connector — Preparation

## Product Scope
Build a comprehensive Imperal connector for **Zoho Books** (C27. Accounting & Bookkeeping). The integration connects directly to the official **Zoho Books API v3** across all global regional datacenters, empowering users to manage customers, invoices, bills, vendor payments, bank accounts, tax rates, and cash flow operations.

## Official API Specifications
- **API Version:** Zoho Books API v3
- **Base URLs by Regional Datacenter:**
  - US: `https://www.zohoapis.com/books/v3`
  - EU: `https://www.zohoapis.eu/books/v3`
  - IN: `https://www.zohoapis.in/books/v3`
  - AU: `https://www.zohoapis.com.au/books/v3`
  - JP: `https://www.zohoapis.jp/books/v3`
  - CA: `https://www.zohoapis.ca/books/v3`
  - SA: `https://www.zohoapis.sa/books/v3`
- **Mandatory Requirements:**
  - Every API request MUST supply `organization_id` as a query parameter.
  - Multi-datacenter routing support (Standard B7).
  - Explicit rate limit detection (HTTP 429) and auth classification (HTTP 401/403).
  - Multi-tenant connection tracking via `connection_id` (Standard B9).

## Delivery Gates
1. [x] Official API discovery completed with Zoho API v3 specifications.
2. [x] Regional datacenter matrix mapped and implemented.
3. [x] Five mandatory specification documents authored.
4. [x] Client implemented with B7-B10 compliance, secret redaction, and 429/401 classification.
5. [x] Panel sidebar implemented conforming to UI_INTERFACE_STANDARD.md.
6. [x] Action prices calibrated per PRICING_POLICY.md.
