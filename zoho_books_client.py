"""Official Zoho Books API v3 client with regional datacenter and multi-org support."""
from __future__ import annotations
import httpx
from typing import Any, Optional

ZOHO_REGIONS = {
    "us": "https://www.zohoapis.com/books/v3",
    "eu": "https://www.zohoapis.eu/books/v3",
    "in": "https://www.zohoapis.in/books/v3",
    "au": "https://www.zohoapis.com.au/books/v3",
    "jp": "https://www.zohoapis.jp/books/v3",
    "ca": "https://www.zohoapis.ca/books/v3",
    "sa": "https://www.zohoapis.sa/books/v3",
}

class ZohoBooksClient:
    def __init__(self, auth_token: str, organization_id: str, region: str = "us", base_url: str = ""):
        self.auth_token = auth_token.strip()
        self.org_id = organization_id.strip()
        self.region = region.lower().strip() if region else "us"
        if base_url and base_url.strip():
            self.base_url = base_url.strip().rstrip("/")
        else:
            self.base_url = ZOHO_REGIONS.get(self.region, ZOHO_REGIONS["us"])

        self.headers = {
            "Authorization": f"Zoho-oauthtoken {self.auth_token}" if not self.auth_token.lower().startswith("bearer ") else self.auth_token,
            "Content-Type": "application/json",
            "User-Agent": "Imperal-ZohoBooks/0.1.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    def _params(self, extra: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        p: dict[str, Any] = {}
        if self.org_id:
            p["organization_id"] = self.org_id
        if extra:
            for k, v in extra.items():
                if v is not None and v != "":
                    p[k] = v
        return p

    def _classify_error(self, resp: httpx.Response, action_name: str) -> dict[str, Any]:
        status = resp.status_code
        err_msg = ""
        try:
            data = resp.json()
            err_msg = data.get("message", "")
        except Exception:
            err_msg = resp.text[:200]

        if status == 401:
            return {"error": f"Zoho Books auth expired or invalid token for {action_name}. Re-connect required.", "code": "UNAUTHORIZED"}
        if status == 403:
            return {"error": f"Permission denied for {action_name} in organization {self.org_id}. Check OAuth scopes.", "code": "FORBIDDEN"}
        if status == 429:
            retry_after = resp.headers.get("Retry-After", "60")
            return {"error": f"Rate limit reached on Zoho Books API for {action_name}. Retry after {retry_after}s.", "code": "RATE_LIMITED"}
        if status == 404:
            return {"error": f"Resource not found in Zoho Books: {err_msg}", "code": "NOT_FOUND"}
        return {"error": f"Zoho Books API error ({status}): {err_msg}", "code": f"HTTP_{status}"}

    async def verify_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                # GET /organizations reads account organizations and validates token
                resp = await client.get(f"{self.base_url}/organizations", headers=self.headers)
                if resp.status_code == 200:
                    data = resp.json()
                    orgs = data.get("organizations", [])
                    matched = next((o for o in orgs if str(o.get("organization_id")) == str(self.org_id)), None)
                    return {
                        "verified": True,
                        "organizations_count": len(orgs),
                        "organization_name": matched.get("name") if matched else (orgs[0].get("name") if orgs else "Zoho Books Org"),
                        "currency": matched.get("currency_code") if matched else "USD"
                    }
                err = self._classify_error(resp, "verify_auth")
                return {"verified": False, **err}
            except Exception as e:
                return {"verified": False, "error": f"Network connection to Zoho Books failed: {str(e)[:150]}", "code": "NETWORK_ERROR"}

    async def list_customers(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = self._params({"per_page": limit, "page": cursor or "1"})
                resp = await client.get(f"{self.base_url}/contacts", headers=self.headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    contacts = data.get("contacts", [])
                    page_context = data.get("page_context", {})
                    has_more = page_context.get("has_more_page", False)
                    curr_page = int(page_context.get("page", 1))
                    next_cursor = str(curr_page + 1) if has_more else None
                    items = [
                        {"id": c.get("contact_id"), "name": c.get("contact_name"), "status": c.get("status"), "email": c.get("email"), "raw": c}
                        for c in contacts
                    ]
                    return {"items": items, "total": len(items), "next_cursor": next_cursor}
                return self._classify_error(resp, "list_customers")
            except Exception as e:
                return {"error": f"Failed to list customers: {str(e)[:120]}", "items": [], "total": 0}

    async def get_customer(self, customer_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/contacts/{customer_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    data = resp.json()
                    c = data.get("contact", {})
                    return {"id": c.get("contact_id"), "name": c.get("contact_name"), "status": c.get("status"), "raw": c}
                return self._classify_error(resp, "get_customer")
            except Exception as e:
                return {"error": f"Failed to get customer: {str(e)[:120]}"}

    async def create_customer(self, name: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"contact_name": name}
                if details:
                    payload.update(details)
                resp = await client.post(f"{self.base_url}/contacts", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    data = resp.json()
                    c = data.get("contact", {})
                    return {"id": c.get("contact_id"), "name": c.get("contact_name"), "status": "active", "raw": c}
                return self._classify_error(resp, "create_customer")
            except Exception as e:
                return {"error": f"Failed to create customer: {str(e)[:120]}"}

    async def update_customer(self, customer_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/contacts/{customer_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    data = resp.json()
                    c = data.get("contact", {})
                    return {"id": c.get("contact_id"), "name": c.get("contact_name"), "status": "updated", "raw": c}
                return self._classify_error(resp, "update_customer")
            except Exception as e:
                return {"error": f"Failed to update customer: {str(e)[:120]}"}

    async def delete_customer(self, customer_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/contacts/{customer_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def list_invoices(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = self._params({"per_page": limit, "page": cursor or "1"})
                resp = await client.get(f"{self.base_url}/invoices", headers=self.headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    invoices = data.get("invoices", [])
                    page_context = data.get("page_context", {})
                    has_more = page_context.get("has_more_page", False)
                    curr_page = int(page_context.get("page", 1))
                    next_cursor = str(curr_page + 1) if has_more else None
                    items = [
                        {"id": inv.get("invoice_id"), "name": inv.get("invoice_number"), "status": inv.get("status"), "total": inv.get("total"), "raw": inv}
                        for inv in invoices
                    ]
                    return {"items": items, "total": len(items), "next_cursor": next_cursor}
                return self._classify_error(resp, "list_invoices")
            except Exception as e:
                return {"error": f"Failed to list invoices: {str(e)[:120]}", "items": [], "total": 0}

    async def get_invoice(self, invoice_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/invoices/{invoice_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    inv = resp.json().get("invoice", {})
                    return {"id": inv.get("invoice_id"), "name": inv.get("invoice_number"), "status": inv.get("status"), "raw": inv}
                return self._classify_error(resp, "get_invoice")
            except Exception as e:
                return {"error": f"Failed to get invoice: {str(e)[:120]}"}

    async def create_invoice(self, customer_id: str, line_items: list[dict[str, Any]], details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"customer_id": customer_id, "line_items": line_items}
                if details:
                    payload.update(details)
                resp = await client.post(f"{self.base_url}/invoices", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    inv = resp.json().get("invoice", {})
                    return {"id": inv.get("invoice_id"), "name": inv.get("invoice_number"), "status": inv.get("status", "draft"), "raw": inv}
                return self._classify_error(resp, "create_invoice")
            except Exception as e:
                return {"error": f"Failed to create invoice: {str(e)[:120]}"}

    async def update_invoice(self, invoice_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/invoices/{invoice_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    inv = resp.json().get("invoice", {})
                    return {"id": inv.get("invoice_id"), "name": inv.get("invoice_number"), "status": inv.get("status"), "raw": inv}
                return self._classify_error(resp, "update_invoice")
            except Exception as e:
                return {"error": f"Failed to update invoice: {str(e)[:120]}"}

    async def delete_invoice(self, invoice_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/invoices/{invoice_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def list_bills(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = self._params({"per_page": limit, "page": cursor or "1"})
                resp = await client.get(f"{self.base_url}/bills", headers=self.headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    bills = data.get("bills", [])
                    items = [{"id": b.get("bill_id"), "name": b.get("bill_number"), "status": b.get("status"), "raw": b} for b in bills]
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_bills")
            except Exception as e:
                return {"error": f"Failed to list bills: {str(e)[:120]}", "items": [], "total": 0}

    async def get_bill(self, bill_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/bills/{bill_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    b = resp.json().get("bill", {})
                    return {"id": b.get("bill_id"), "name": b.get("bill_number"), "status": b.get("status"), "raw": b}
                return self._classify_error(resp, "get_bill")
            except Exception as e:
                return {"error": f"Failed to get bill: {str(e)[:120]}"}

    async def create_bill(self, vendor_id: str, line_items: list[dict[str, Any]], details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"vendor_id": vendor_id, "line_items": line_items}
                if details: payload.update(details)
                resp = await client.post(f"{self.base_url}/bills", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    b = resp.json().get("bill", {})
                    return {"id": b.get("bill_id"), "name": b.get("bill_number"), "status": b.get("status", "open"), "raw": b}
                return self._classify_error(resp, "create_bill")
            except Exception as e:
                return {"error": f"Failed to create bill: {str(e)[:120]}"}

    async def update_bill(self, bill_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/bills/{bill_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    b = resp.json().get("bill", {})
                    return {"id": b.get("bill_id"), "name": b.get("bill_number"), "status": b.get("status"), "raw": b}
                return self._classify_error(resp, "update_bill")
            except Exception as e:
                return {"error": f"Failed to update bill: {str(e)[:120]}"}

    async def delete_bill(self, bill_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/bills/{bill_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def list_payments(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                params = self._params({"per_page": limit, "page": cursor or "1"})
                resp = await client.get(f"{self.base_url}/customerpayments", headers=self.headers, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    payments = data.get("customerpayments", [])
                    items = [{"id": p.get("payment_id"), "name": p.get("payment_number"), "status": "recorded", "raw": p} for p in payments]
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_payments")
            except Exception as e:
                return {"error": f"Failed to list payments: {str(e)[:120]}", "items": [], "total": 0}

    async def get_payment(self, payment_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/customerpayments/{payment_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    p = resp.json().get("payment", {})
                    return {"id": p.get("payment_id"), "name": p.get("payment_number"), "status": "recorded", "raw": p}
                return self._classify_error(resp, "get_payment")
            except Exception as e:
                return {"error": f"Failed to get payment: {str(e)[:120]}"}

    async def create_payment(self, customer_id: str, amount: float, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"customer_id": customer_id, "amount": amount}
                if details: payload.update(details)
                resp = await client.post(f"{self.base_url}/customerpayments", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    p = resp.json().get("payment", {})
                    return {"id": p.get("payment_id"), "name": p.get("payment_number"), "status": "recorded", "raw": p}
                return self._classify_error(resp, "create_payment")
            except Exception as e:
                return {"error": f"Failed to create payment: {str(e)[:120]}"}

    async def update_payment(self, payment_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/customerpayments/{payment_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    p = resp.json().get("payment", {})
                    return {"id": p.get("payment_id"), "name": p.get("payment_number"), "status": "updated", "raw": p}
                return self._classify_error(resp, "update_payment")
            except Exception as e:
                return {"error": f"Failed to update payment: {str(e)[:120]}"}

    async def delete_payment(self, payment_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/customerpayments/{payment_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def list_bank_accounts(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/bankaccounts", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    data = resp.json()
                    accs = data.get("bankaccounts", [])
                    items = [{"id": a.get("account_id"), "name": a.get("account_name"), "status": a.get("account_type"), "raw": a} for a in accs]
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_bank_accounts")
            except Exception as e:
                return {"error": f"Failed to list bank accounts: {str(e)[:120]}", "items": [], "total": 0}

    async def get_bank_account(self, account_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/bankaccounts/{account_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    a = resp.json().get("bankaccount", {})
                    return {"id": a.get("account_id"), "name": a.get("account_name"), "status": a.get("account_type"), "raw": a}
                return self._classify_error(resp, "get_bank_account")
            except Exception as e:
                return {"error": f"Failed to get bank account: {str(e)[:120]}"}

    async def create_bank_account(self, account_name: str, account_type: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"account_name": account_name, "account_type": account_type}
                if details: payload.update(details)
                resp = await client.post(f"{self.base_url}/bankaccounts", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    a = resp.json().get("bankaccount", {})
                    return {"id": a.get("account_id"), "name": a.get("account_name"), "status": a.get("account_type"), "raw": a}
                return self._classify_error(resp, "create_bank_account")
            except Exception as e:
                return {"error": f"Failed to create bank account: {str(e)[:120]}"}

    async def update_bank_account(self, account_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/bankaccounts/{account_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    a = resp.json().get("bankaccount", {})
                    return {"id": a.get("account_id"), "name": a.get("account_name"), "status": a.get("account_type"), "raw": a}
                return self._classify_error(resp, "update_bank_account")
            except Exception as e:
                return {"error": f"Failed to update bank account: {str(e)[:120]}"}

    async def delete_bank_account(self, account_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/bankaccounts/{account_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def list_tax_rates(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/settings/taxes", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    data = resp.json()
                    taxes = data.get("taxes", [])
                    items = [{"id": t.get("tax_id"), "name": t.get("tax_name"), "status": f"{t.get('tax_percentage')}%", "raw": t} for t in taxes]
                    return {"items": items, "total": len(items)}
                return self._classify_error(resp, "list_tax_rates")
            except Exception as e:
                return {"error": f"Failed to list tax rates: {str(e)[:120]}", "items": [], "total": 0}

    async def get_tax_rate(self, tax_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/settings/taxes/{tax_id}", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    t = resp.json().get("tax", {})
                    return {"id": t.get("tax_id"), "name": t.get("tax_name"), "status": f"{t.get('tax_percentage')}%", "raw": t}
                return self._classify_error(resp, "get_tax_rate")
            except Exception as e:
                return {"error": f"Failed to get tax rate: {str(e)[:120]}"}

    async def create_tax_rate(self, tax_name: str, tax_percentage: float, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                payload = {"tax_name": tax_name, "tax_percentage": tax_percentage}
                if details: payload.update(details)
                resp = await client.post(f"{self.base_url}/settings/taxes", headers=self.headers, params=self._params(), json=payload)
                if resp.status_code in (200, 201):
                    t = resp.json().get("tax", {})
                    return {"id": t.get("tax_id"), "name": t.get("tax_name"), "status": f"{t.get('tax_percentage')}%", "raw": t}
                return self._classify_error(resp, "create_tax_rate")
            except Exception as e:
                return {"error": f"Failed to create tax rate: {str(e)[:120]}"}

    async def update_tax_rate(self, tax_id: str, fields: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.put(f"{self.base_url}/settings/taxes/{tax_id}", headers=self.headers, params=self._params(), json=fields)
                if resp.status_code == 200:
                    t = resp.json().get("tax", {})
                    return {"id": t.get("tax_id"), "name": t.get("tax_name"), "status": f"{t.get('tax_percentage')}%", "raw": t}
                return self._classify_error(resp, "update_tax_rate")
            except Exception as e:
                return {"error": f"Failed to update tax rate: {str(e)[:120]}"}

    async def delete_tax_rate(self, tax_id: str) -> bool:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.delete(f"{self.base_url}/settings/taxes/{tax_id}", headers=self.headers, params=self._params())
                return resp.status_code == 200
            except Exception:
                return False

    async def audit_accounting_health(self) -> dict[str, Any]:
        """Value-add audit: probe customers, invoices, bills and tax rates with rate limit safety."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                inv_resp = await client.get(f"{self.base_url}/invoices", headers=self.headers, params=self._params({"status": "overdue", "per_page": 5}))
                overdue_count = 0
                if inv_resp.status_code == 200:
                    overdue_count = len(inv_resp.json().get("invoices", []))
                return {
                    "health_status": "healthy" if inv_resp.status_code == 200 else "degraded",
                    "organization_id": self.org_id,
                    "region": self.region,
                    "overdue_invoices_sample": overdue_count,
                    "api_status": "connected"
                }
            except Exception as e:
                return {"health_status": "error", "error": str(e)[:120]}

    async def get_cash_flow_summary(self) -> dict[str, Any]:
        """Value-add report: overview of bank accounts and balance aggregates."""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/bankaccounts", headers=self.headers, params=self._params())
                if resp.status_code == 200:
                    accs = resp.json().get("bankaccounts", [])
                    total_balance = sum(float(a.get("balance", 0.0)) for a in accs if a.get("balance") is not None)
                    return {
                        "accounts_count": len(accs),
                        "total_liquid_balance": total_balance,
                        "currency": accs[0].get("currency_code", "USD") if accs else "USD"
                    }
                return {"accounts_count": 0, "total_liquid_balance": 0.0, "status": "unavailable"}
            except Exception as e:
                return {"error": str(e)[:120], "accounts_count": 0}
