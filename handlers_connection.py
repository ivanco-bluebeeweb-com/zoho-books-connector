"""Connection lifecycle for Zoho Books Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from zoho_books_client import ZohoBooksClient
from app import chat
from schemas import (
    NoParams,
    ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord, DeleteResult
)

_SECRET = "zoho_books_connections"

def _mask(value: str) -> str:
    return value[:4] + "…" + value[-4:] if len(value) > 10 else "***"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw: return []
    try: data = json.loads(raw)
    except: return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns: return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c["id"] == connection_id:
            return c
    return None

@chat.function(
    "connect_zoho_books",
    "Connect your own Zoho Books account with OAuth token, Organization ID, and regional datacenter.",
    action_type="write",
    chain_callable=True,
    event="zoho-books-connector.connect_zoho_books",
    effects=["create:connection"],
    data_model=ConnectParams
)
async def connect_zoho_books(ctx, params: ConnectParams) -> ActionResult[ConnectionRecord]:
    """Connect a new account."""
    client = ZohoBooksClient(
        auth_token=params.auth_token,
        organization_id=params.organization_id,
        region=params.region,
        base_url=params.base_url
    )
    v_res = await client.verify_auth()
    if v_res.get("status") == "error":
        return ActionResult.error(
            f"Failed to authenticate with Zoho Books: {v_res.get('message', 'invalid credentials or organization ID')}",
            code=v_res.get("code", "UNAUTHORIZED")
        )

    conns = await _load_connections(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    record = {
        "id": cid,
        "label": params.label or f"Zoho Books ({params.organization_id})",
        "auth_token": params.auth_token,
        "organization_id": params.organization_id,
        "region": params.region.lower(),
        "base_url": client.base_url,
        "is_active": True
    }
    for c in conns: c["is_active"] = False
    conns.append(record)
    await _save_connections(ctx, conns)
    return ActionResult.ok(
        ConnectionRecord(
            id=cid,
            label=record["label"],
            masked_key=_mask(params.auth_token),
            organization_id=params.organization_id,
            region=params.region.lower(),
            base_url=client.base_url,
            is_active=True
        )
    )

@chat.function(
    "list_connections",
    "List connected Zoho Books organizations without exposing sensitive tokens.",
    action_type="read",
    chain_callable=True,
    data_model=NoParams
)
async def list_connections(ctx, params: NoParams) -> ActionResult[ConnectionList]:
    """List connected accounts."""
    conns = await _load_connections(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=_mask(c.get("auth_token", c.get("api_key", ""))),
            organization_id=c.get("organization_id", ""),
            region=c.get("region", "us"),
            base_url=c.get("base_url", ""),
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult.ok(ConnectionList(connections=records, total=len(records)))

@chat.function(
    "disconnect_zoho_books",
    "Disconnect a Zoho Books organization.",
    action_type="write",
    chain_callable=True,
    event="zoho-books-connector.disconnect_zoho_books",
    effects=["delete:connection"],
    data_model=ConnectionIdParams
)
async def disconnect_zoho_books(ctx, params: ConnectionIdParams) -> ActionResult[DeleteResult]:
    """Disconnect an account."""
    conns = await _load_connections(ctx)
    target = await resolve_connection(ctx, params.connection_id)
    if not target:
        return ActionResult.error("Connection not found", code="NOT_FOUND")
    new_conns = [c for c in conns if c["id"] != target["id"]]
    if new_conns and target.get("is_active"):
        new_conns[0]["is_active"] = True
    await _save_connections(ctx, new_conns)
    return ActionResult.ok(DeleteResult(id=target["id"], deleted=True, message="Disconnected successfully"))
