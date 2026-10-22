# Security

This project targets obsolete TV platforms and is a community beta, not a hardened internet-facing service. Keep the TV and Plex server on an appropriately secured network. Do not expose the installation server to the internet or disable Plex authentication to accommodate this app.

Use your own authorized Plex credentials if required. Tokens are stored locally on the TV and may travel in URLs used by the legacy player. HTTP is not encrypted; legacy TLS support may limit HTTPS interoperability. The app does not bypass certificate checks.

Before reporting a bug, remove tokens, account identifiers, server addresses, media paths and personal library data. For a suspected security issue, open a minimal issue asking for a private reporting channel without publishing exploit details or secrets.
