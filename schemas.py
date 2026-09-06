"""Pydantic schemas for Zoho Books Connector (C27. Accounting & Bookkeeping)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme Zoho Books.")
    auth_token: str = Field(description="Zoho Books OAuth Access Token or Self-Client token.")
    organization_id: str = Field(description="Zoho Books Organization ID (found in Zoho Books under Settings > Organization Profile).")
    region: str = Field(default="us", description="Zoho regional datacenter: 'us' (com), 'eu' (eu), 'in' (in), 'au' (com.au), 'jp' (jp), 'ca' (ca), 'sa' (sa).")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain (overrides regional default).")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    organization_id: str
    region: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class DeleteResult(BaseModel):
    id: str
    deleted: bool
    message: str

class ListCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination page number (1, 2, ...).")

class GetCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer (contact_id in Zoho).")

class CreateCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    contact_name: str = Field(description="Display name or primary contact name.")
    company_name: str = Field(default="", description="Company name if B2B customer.")
    email: str = Field(default="", description="Primary billing email address.")
    phone: str = Field(default="", description="Primary contact phone number.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Optional extra Zoho contact fields.")

class UpdateCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer (contact_id).")
    fields: dict[str, Any] = Field(description="Attributes to update (contact_name, email, phone, etc.).")

class DeleteCustomerParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Unique identifier of the customer to delete.")

class CustomerRecord(BaseModel):
    id: str
    name: str
    email: str = ""
    phone: str = ""
    status: str = "active"
    raw: dict[str, Any] = {}

class CustomerList(BaseModel):
    items: list[CustomerRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class ListInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination page number.")

class GetInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class CreateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Customer ID the invoice is issued to.")
    invoice_number: str = Field(default="", description="Optional explicit invoice number.")
    date: str = Field(default="", description="Invoice issue date (YYYY-MM-DD).")
    due_date: str = Field(default="", description="Invoice due date (YYYY-MM-DD).")
    line_items: list[dict[str, Any]] = Field(default=[], description="List of invoice line items with item_id or name, rate, quantity.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteInvoiceParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    invoice_id: str = Field(description="Unique identifier of the invoice.")

class InvoiceRecord(BaseModel):
    id: str
    name: str
    invoice_number: str = ""
    customer_name: str = ""
    total: float = 0.0
    balance: float = 0.0
    status: str = "active"
    raw: dict[str, Any] = {}

class InvoiceList(BaseModel):
    items: list[InvoiceRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class ListBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page number.")

class GetBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class CreateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    vendor_id: str = Field(description="Vendor ID the bill is from.")
    bill_number: str = Field(default="", description="Vendor reference bill number.")
    line_items: list[dict[str, Any]] = Field(default=[], description="Bill line items.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBillParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    bill_id: str = Field(description="Unique identifier of the bill.")

class BillRecord(BaseModel):
    id: str
    name: str
    bill_number: str = ""
    vendor_name: str = ""
    total: float = 0.0
    balance: float = 0.0
    status: str = "open"
    raw: dict[str, Any] = {}

class BillList(BaseModel):
    items: list[BillRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class ListPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page number.")

class GetPaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class CreatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    customer_id: str = Field(description="Customer who made the payment.")
    amount: float = Field(description="Payment amount received.")
    date: str = Field(default="", description="Payment date (YYYY-MM-DD).")
    payment_mode: str = Field(default="cash", description="Payment mode (cash, bank, check, etc.).")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdatePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeletePaymentParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    payment_id: str = Field(description="Unique identifier of the payment.")

class PaymentRecord(BaseModel):
    id: str
    name: str
    payment_number: str = ""
    customer_name: str = ""
    amount: float = 0.0
    date: str = ""
    status: str = "received"
    raw: dict[str, Any] = {}

class PaymentList(BaseModel):
    items: list[PaymentRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class ListBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page number.")

class GetBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")

class CreateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_name: str = Field(description="Name of the bank account.")
    account_type: str = Field(default="bank", description="Account type: bank, credit_card, etc.")
    currency_code: str = Field(default="USD", description="Account currency code.")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteBankAccountParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    account_id: str = Field(description="Unique identifier of the bank account.")

class BankAccountRecord(BaseModel):
    id: str
    name: str
    account_type: str = "bank"
    balance: float = 0.0
    currency: str = "USD"
    status: str = "active"
    raw: dict[str, Any] = {}

class BankAccountList(BaseModel):
    items: list[BankAccountRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class ListTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Max records to return (1-100).")
    cursor: str = Field(default="", description="Pagination cursor or page number.")

class GetTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_id: str = Field(description="Unique identifier of the tax rate.")

class CreateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_name: str = Field(description="Name of the tax.")
    tax_percentage: float = Field(description="Tax percentage (e.g. 20.0).")
    details: Optional[dict[str, Any]] = Field(default=None, description="Detailed attributes and payload.")

class UpdateTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_id: str = Field(description="Unique identifier of the tax rate.")
    fields: dict[str, Any] = Field(description="Attributes to update.")

class DeleteTaxRateParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    tax_id: str = Field(description="Unique identifier of the tax rate.")

class TaxRateRecord(BaseModel):
    id: str
    name: str
    tax_percentage: float = 0.0
    status: str = "active"
    raw: dict[str, Any] = {}

class TaxRateList(BaseModel):
    items: list[TaxRateRecord]
    total: int
    has_more: bool = False
    next_cursor: Optional[str] = None

class AuditHealthReport(BaseModel):
    health_status: str
    organization_id: str
    region: str
    overdue_invoices_sample: int
    api_status: str
    timestamp: str

class CashFlowSummary(BaseModel):
    accounts_count: int
    total_liquid_balance: float
    currency: str
    generated_at: str

class AuditAccountingHealthResult(BaseModel):
    status: str = "ok"
    total_customers: int = 0
    total_invoices: int = 0
    total_bills: int = 0
    bank_accounts_count: int = 0
    overdue_invoices_count: int = 0
    overdue_bills_count: int = 0
    summary: str = ""

class GetCashFlowSummaryResult(BaseModel):
    total_receivables: float = 0.0
    total_payables: float = 0.0
    net_cash_flow: float = 0.0
    currency: str = "USD"
    bank_accounts: list[dict[str, Any]] = []
    summary: str = ""
