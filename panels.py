"""Panel UI for Zoho Books Connector following UI_INTERFACE_STANDARD.md and AUTH_AND_CREDENTIALS_STANDARD.md."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__zoho_books_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I connect Zoho Books?", variant="ghost", size="sm"),
        title="Connecting Zoho Books",
        children=[
            ui.Text(
                "1. Sign in to your Zoho Books organization (books.zoho.com or your local DC).\n"
                "2. Find your Organization ID under Settings > Organization Profile.\n"
                "3. In Zoho Developer Console (api-console.zoho.com), create a Self-Client or Server-based App to generate an OAuth Access Token with ZohoBooks.fullaccess.all scope.\n"
                "4. Select your data center region (US, EU, IN, AU, JP, CA, SA), enter credentials and click Connect.",
                variant="body"
            )
        ]
    )

@ext.panel("zoho_books_sidebar", slot="left")
async def zoho_books_sidebar(ctx, **kwargs) -> ui.UINode:
    return ui.Stack(
        direction="v",
        gap=3,
        align="stretch",
        children=[
            ui.Text("Zoho Books", variant="heading"),
            ui.Text("Manage invoices, customers, bills, bank accounts and tax rates via Zoho Books API v3.", variant="caption"),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Zoho Books",
                action=ui.Call("connect_zoho_books"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        align="stretch",
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=1,
                                align="stretch",
                                children=[
                                    ui.Text("Connection Label", variant="label"),
                                    ui.Input(param_name="label", placeholder="e.g. Production Zoho Books"),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                align="stretch",
                                children=[
                                    ui.Text("Data Center Region", variant="label"),
                                    ui.Select(
                                        param_name="region",
                                        value="us",
                                        options=[
                                            {"label": "United States (.com)", "value": "us"},
                                            {"label": "Europe (.eu)", "value": "eu"},
                                            {"label": "India (.in)", "value": "in"},
                                            {"label": "Australia (.com.au)", "value": "au"},
                                            {"label": "Japan (.jp)", "value": "jp"},
                                            {"label": "Canada (.ca)", "value": "ca"},
                                            {"label": "Saudi Arabia (.sa)", "value": "sa"},
                                        ]
                                    ),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                align="stretch",
                                children=[
                                    ui.Text("Organization ID", variant="label"),
                                    ui.Input(param_name="organization_id", placeholder="e.g. 7001234567"),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                align="stretch",
                                children=[
                                    ui.Text("OAuth Access Token", variant="label"),
                                    ui.Input(param_name="auth_token", placeholder="Paste Zoho OAuth Access Token / Self-Client token"),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                align="stretch",
                                children=[
                                    ui.Text("Custom Base URL (optional)", variant="label"),
                                    ui.Input(param_name="base_url", placeholder="Leave blank to use official regional API"),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
