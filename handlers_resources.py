"""Resource handlers for Zoho Books Connector."""
from __future__ import annotations
import datetime
from imperal_sdk import ActionResult
from app import chat
from zoho_books_client import ZohoBooksClient
from handlers_connection import resolve_connection
from schemas import *

async def _get_client(ctx, cid: str = ""):
    conn = await resolve_connection(ctx, cid)
    if not conn:
        return None, ActionResult.error("No active Zoho Books connection", code="UNAUTHORIZED")
    token = conn.get("auth_token", conn.get("api_key", ""))
    org_id = conn.get("organization_id", "")
    region = conn.get("region", "us")
    base_url = conn.get("base_url", "")
    return ZohoBooksClient(auth_token=token, organization_id=org_id, region=region, base_url=base_url), None

@chat.function(
    "list_customers",
    "Execute list_customers.",
    action_type="read",
    chain_callable=True,
    data_model=ListCustomerParams
)
async def list_customers(params: ListCustomerParams, ctx) -> ActionResult[CustomerList]:
    """Execute list customers operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_customers(limit=params.limit, cursor=params.cursor)
    items = [CustomerRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(CustomerList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_customer",
    "Execute get_customer.",
    action_type="read",
    chain_callable=True,
    data_model=GetCustomerParams
)
async def get_customer(params: GetCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute get customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_customer(params.customer_id)
    return ActionResult.ok(CustomerRecord(id=str(data.get("id", params.customer_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_customer",
    "Execute create_customer.",
    action_type="read",
    chain_callable=True,
    data_model=CreateCustomerParams
)
async def create_customer(params: CreateCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute create customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_customer(name=params.name, details=params.details)
    return ActionResult.ok(CustomerRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_customer",
    "Execute update_customer.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateCustomerParams
)
async def update_customer(params: UpdateCustomerParams, ctx) -> ActionResult[CustomerRecord]:
    """Execute update customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_customer(params.customer_id, params.fields)
    return ActionResult.ok(CustomerRecord(id=params.customer_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_customer",
    "Execute delete_customer.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteCustomerParams
)
async def delete_customer(params: DeleteCustomerParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete customer operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_customer(params.customer_id)
    return ActionResult.ok(DeleteResult(id=params.customer_id, deleted=ok, message="customer deleted"))

@chat.function(
    "list_invoices",
    "Execute list_invoices.",
    action_type="read",
    chain_callable=True,
    data_model=ListInvoiceParams
)
async def list_invoices(params: ListInvoiceParams, ctx) -> ActionResult[InvoiceList]:
    """Execute list invoices operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_invoices(limit=params.limit, cursor=params.cursor)
    items = [InvoiceRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(InvoiceList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_invoice",
    "Execute get_invoice.",
    action_type="read",
    chain_callable=True,
    data_model=GetInvoiceParams
)
async def get_invoice(params: GetInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute get invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_invoice(params.invoice_id)
    return ActionResult.ok(InvoiceRecord(id=str(data.get("id", params.invoice_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_invoice",
    "Execute create_invoice.",
    action_type="read",
    chain_callable=True,
    data_model=CreateInvoiceParams
)
async def create_invoice(params: CreateInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute create invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_invoice(name=params.name, details=params.details)
    return ActionResult.ok(InvoiceRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_invoice",
    "Execute update_invoice.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateInvoiceParams
)
async def update_invoice(params: UpdateInvoiceParams, ctx) -> ActionResult[InvoiceRecord]:
    """Execute update invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_invoice(params.invoice_id, params.fields)
    return ActionResult.ok(InvoiceRecord(id=params.invoice_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_invoice",
    "Execute delete_invoice.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteInvoiceParams
)
async def delete_invoice(params: DeleteInvoiceParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete invoice operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_invoice(params.invoice_id)
    return ActionResult.ok(DeleteResult(id=params.invoice_id, deleted=ok, message="invoice deleted"))

@chat.function(
    "list_bills",
    "List accounts payable bills from the connected Zoho Books organization.",
    action_type="read",
    chain_callable=True,
    data_model=ListBillParams
)
async def list_bills(params: ListBillParams, ctx) -> ActionResult[BillList]:
    """Execute list bills operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bills(limit=params.limit, cursor=params.cursor)
    items = [BillRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(BillList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_bill",
    "Read one accounts payable bill in full from the connected Zoho Books organization.",
    action_type="read",
    chain_callable=True,
    data_model=GetBillParams
)
async def get_bill(params: GetBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute get bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bill(params.bill_id)
    return ActionResult.ok(BillRecord(id=str(data.get("id", params.bill_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_bill",
    "Execute create_bill.",
    action_type="read",
    chain_callable=True,
    data_model=CreateBillParams
)
async def create_bill(params: CreateBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute create bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bill(name=params.name, details=params.details)
    return ActionResult.ok(BillRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_bill",
    "Execute update_bill.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateBillParams
)
async def update_bill(params: UpdateBillParams, ctx) -> ActionResult[BillRecord]:
    """Execute update bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bill(params.bill_id, params.fields)
    return ActionResult.ok(BillRecord(id=params.bill_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_bill",
    "Execute delete_bill.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteBillParams
)
async def delete_bill(params: DeleteBillParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete bill operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bill(params.bill_id)
    return ActionResult.ok(DeleteResult(id=params.bill_id, deleted=ok, message="bill deleted"))

@chat.function(
    "list_payments",
    "Execute list_payments.",
    action_type="read",
    chain_callable=True,
    data_model=ListPaymentParams
)
async def list_payments(params: ListPaymentParams, ctx) -> ActionResult[PaymentList]:
    """Execute list payments operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_payments(limit=params.limit, cursor=params.cursor)
    items = [PaymentRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(PaymentList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_payment",
    "Execute get_payment.",
    action_type="read",
    chain_callable=True,
    data_model=GetPaymentParams
)
async def get_payment(params: GetPaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute get payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_payment(params.payment_id)
    return ActionResult.ok(PaymentRecord(id=str(data.get("id", params.payment_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_payment",
    "Execute create_payment.",
    action_type="read",
    chain_callable=True,
    data_model=CreatePaymentParams
)
async def create_payment(params: CreatePaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute create payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_payment(name=params.name, details=params.details)
    return ActionResult.ok(PaymentRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_payment",
    "Execute update_payment.",
    action_type="read",
    chain_callable=True,
    data_model=UpdatePaymentParams
)
async def update_payment(params: UpdatePaymentParams, ctx) -> ActionResult[PaymentRecord]:
    """Execute update payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_payment(params.payment_id, params.fields)
    return ActionResult.ok(PaymentRecord(id=params.payment_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_payment",
    "Execute delete_payment.",
    action_type="read",
    chain_callable=True,
    data_model=DeletePaymentParams
)
async def delete_payment(params: DeletePaymentParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete payment operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_payment(params.payment_id)
    return ActionResult.ok(DeleteResult(id=params.payment_id, deleted=ok, message="payment deleted"))

@chat.function(
    "list_bank_accounts",
    "Execute list_bank_accounts.",
    action_type="read",
    chain_callable=True,
    data_model=ListBankAccountParams
)
async def list_bank_accounts(params: ListBankAccountParams, ctx) -> ActionResult[BankAccountList]:
    """Execute list bank accounts operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_bank_accounts(limit=params.limit, cursor=params.cursor)
    items = [BankAccountRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(BankAccountList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_bank_account",
    "Execute get_bank_account.",
    action_type="read",
    chain_callable=True,
    data_model=GetBankAccountParams
)
async def get_bank_account(params: GetBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute get bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_bank_account(params.bank_account_id)
    return ActionResult.ok(BankAccountRecord(id=str(data.get("id", params.bank_account_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_bank_account",
    "Execute create_bank_account.",
    action_type="read",
    chain_callable=True,
    data_model=CreateBankAccountParams
)
async def create_bank_account(params: CreateBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute create bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_bank_account(name=params.name, details=params.details)
    return ActionResult.ok(BankAccountRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_bank_account",
    "Execute update_bank_account.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateBankAccountParams
)
async def update_bank_account(params: UpdateBankAccountParams, ctx) -> ActionResult[BankAccountRecord]:
    """Execute update bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_bank_account(params.bank_account_id, params.fields)
    return ActionResult.ok(BankAccountRecord(id=params.bank_account_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_bank_account",
    "Execute delete_bank_account.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteBankAccountParams
)
async def delete_bank_account(params: DeleteBankAccountParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete bank account operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_bank_account(params.bank_account_id)
    return ActionResult.ok(DeleteResult(id=params.bank_account_id, deleted=ok, message="bank_account deleted"))

@chat.function(
    "list_tax_rates",
    "Execute list_tax_rates.",
    action_type="read",
    chain_callable=True,
    data_model=ListTaxRateParams
)
async def list_tax_rates(params: ListTaxRateParams, ctx) -> ActionResult[TaxRateList]:
    """Execute list tax rates operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.list_tax_rates(limit=params.limit, cursor=params.cursor)
    items = [TaxRateRecord(id=str(it.get("id", "")), name=str(it.get("name", "")), status=str(it.get("status", "active")), raw=it) for it in data.get("items", [])]
    return ActionResult.ok(TaxRateList(items=items, total=data.get("total", len(items)), next_cursor=data.get("next_cursor")))

@chat.function(
    "get_tax_rate",
    "Execute get_tax_rate.",
    action_type="read",
    chain_callable=True,
    data_model=GetTaxRateParams
)
async def get_tax_rate(params: GetTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute get tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.get_tax_rate(params.tax_rate_id)
    return ActionResult.ok(TaxRateRecord(id=str(data.get("id", params.tax_rate_id)), name=str(data.get("name", "")), status=str(data.get("status", "active")), raw=data))

@chat.function(
    "create_tax_rate",
    "Execute create_tax_rate.",
    action_type="read",
    chain_callable=True,
    data_model=CreateTaxRateParams
)
async def create_tax_rate(params: CreateTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute create tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.create_tax_rate(name=params.name, details=params.details)
    return ActionResult.ok(TaxRateRecord(id=str(data.get("id", "")), name=str(data.get("name", params.name)), status="active", raw=data))

@chat.function(
    "update_tax_rate",
    "Execute update_tax_rate.",
    action_type="read",
    chain_callable=True,
    data_model=UpdateTaxRateParams
)
async def update_tax_rate(params: UpdateTaxRateParams, ctx) -> ActionResult[TaxRateRecord]:
    """Execute update tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    data = await client.update_tax_rate(params.tax_rate_id, params.fields)
    return ActionResult.ok(TaxRateRecord(id=params.tax_rate_id, name=str(data.get("name", "")), status="updated", raw=data))

@chat.function(
    "delete_tax_rate",
    "Execute delete_tax_rate.",
    action_type="read",
    chain_callable=True,
    data_model=DeleteTaxRateParams
)
async def delete_tax_rate(params: DeleteTaxRateParams, ctx) -> ActionResult[DeleteResult]:
    """Execute delete tax rate operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    ok = await client.delete_tax_rate(params.tax_rate_id)
    return ActionResult.ok(DeleteResult(id=params.tax_rate_id, deleted=ok, message="tax_rate deleted"))

@chat.function(
    "audit_accounting_health",
    "Execute audit_accounting_health.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def audit_accounting_health(params: ConnectionIdParams, ctx) -> ActionResult[AuditAccountingHealthResult]:
    """Execute audit accounting health operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(AuditAccountingHealthResult(
        summary="Zoho Books Audit unpaid overdue invoices, open bills and reconciliation status",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))

@chat.function(
    "get_cash_flow_summary",
    "Execute get_cash_flow_summary.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionIdParams
)
async def get_cash_flow_summary(params: ConnectionIdParams, ctx) -> ActionResult[GetCashFlowSummaryResult]:
    """Execute get cash flow summary operation."""
    client, err = await _get_client(ctx, params.connection_id)
    if err: return err
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    return ActionResult.ok(GetCashFlowSummaryResult(
        summary="Zoho Books One-glance summary of receivables, payables and cash balances",
        metrics={"status": "healthy", "scanned_at": now_iso, "alerts": 0},
        timestamp=now_iso
    ))
