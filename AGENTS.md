# Orsay Cinema repository guidance

## Purpose

This is an independent, standalone personal-media client for Samsung's pre-Tizen Orsay TVs, compatible with Plex Media Server. Read README.md, PRIVACY.md and SECURITY.md before installation or connection changes. AI_SETUP_PROMPT.md is the user-facing guided-install workflow.

## Constraints

- Preserve ES5-style JavaScript and legacy WebKit compatibility. Do not introduce a transpilation/runtime dependency without a concrete supported-device reason.
- All interface assets are bundled on the TV. Runtime requests go directly to the configured Plex server; never reintroduce a coding-computer proxy or live-code loader.
- Server addresses and optional tokens belong in TV-side local configuration, not tracked source. Installer addresses go only in generated dist/widgetlist.xml. Keep private logs, credentials, library paths and media screenshots out of commits/issues.
- Do not disable authentication, bypass certificates, root devices, flash firmware or reset Smart Hub to work around app bugs.
- The TV supplies Common.API and the native player plugin; do not vendor Samsung system scripts or SDK binaries.
- Keep original project artwork and independent branding. Do not replace the icon with the Plex chevron or imply endorsement.
- Developer sync catalogs can affect other developer apps. build.py must preserve other catalog entries and unique identities. Keep their ZIPs available when using a shared catalog.

## Files

- app.js: ES5 UI, connection setup, direct/native playback and subtitle workflow.
- index.html, style.css: bundled interface.
- build.py: standard-library, reproducible widget ZIP and optional installer catalog.
- serve.py: temporary local installation server serving dist only.
- test.js and test_build.py: synthetic regression fixtures and packaging checks.

## Validation

Run the applicable documented checks after changing code:

    node --check app.js
    node test.js
    python3 -m unittest test_build.py
    python3 build.py

Use synthetic or public-domain data for examples. Check proposed public files for secrets and personal addresses. Browser tests do not validate Samsung native APIs, codec support or subtitle display. Distinguish automated checks, desktop UI checks and user-confirmed TV results.

Only H6203 firmware 1230 has the original standalone playback/subtitle test evidence. The generic connection screen and optional token flow need additional TV validation; do not claim broad model support. Native seek/subtitle changes can buffer noticeably.

When assisting installation, verify TV-origin catalog/package requests, then actual launch and playback. Stop the installer and repeat a fresh subtitle operation to prove independence. Document a blocker rather than inventing a successful test. Do not publish local work unless the user requests publication.
