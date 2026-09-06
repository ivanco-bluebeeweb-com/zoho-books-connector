# Zoho Books Connector — UI Component Plan

## Sidebar Architecture (slot="left")
Conforms strictly to `UI_INTERFACE_STANDARD.md`:
- `slot="left"`, `align="stretch"` on root container and child stacks.
- All form inputs provide explicit labels and contextual placeholders:
  - Auth Token: label='OAuth Access Token', placeholder='1000.xxxx.xxxx'
  - Organization ID: label='Organization ID', placeholder='e.g. 700123456'
  - Region: label='Data Center Region', placeholder='us, eu, in, au, jp, ca, sa'
- Connection status badge displays active connection, masked token and region.
- Help modal provides onboarding step-by-step setup guide without sidebar clutter.
- App Settings secondary button links directly to `__panel__zoho_books_settings`.
