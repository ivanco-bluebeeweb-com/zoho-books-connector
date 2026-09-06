# Zoho Books Connector — Ideal Onboarding Experience

## User Journey
1. **Prerequisites Guide:**
   - In Zoho Books, open Settings -> Organization Profile to find your `Organization ID`.
   - In Zoho Developer Console (api-console.zoho.com), register a Self-Client or OAuth application.
   - Generate a token with scope `ZohoBooks.fullaccess.all`.
2. **Connecting to Imperal:**
   - Open Zoho Books connector in Imperal OS.
   - Enter Connection Label (e.g. 'Main Operations').
   - Paste OAuth Access Token.
   - Enter Organization ID.
   - Select your Data Center Region (e.g. EU for European accounts).
   - Click 'Connect Zoho Books'.
3. **Verification:**
   - Connector runs `verify_auth()` against `/organizations`.
   - Instant visual feedback confirms active connection status.
