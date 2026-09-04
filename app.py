"""Extension declaration, capabilities, health check for Zoho Books Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "zoho-books-connector",
    version="0.1.0",
    display_name="Zoho Books",
    icon="icon.svg",
    capabilities=["zoho_books:manage"],
    description="Official Imperal connector for Zoho Books (C27. Accounting & Bookkeeping). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("zoho_books_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Zoho Books connection(s) configured." if count else "Not connected yet."
    }
