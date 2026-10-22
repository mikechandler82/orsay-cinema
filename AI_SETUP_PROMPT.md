# Let an AI agent help you install Orsay Cinema

Download or clone this repository and open its folder in Codex, Claude Code, or another coding agent with local file and terminal access. Paste the prompt below. A chat-only agent can explain the steps, but cannot build files or run an installer on your computer unless it has the necessary tools.

You do not need to fill in a server address before starting. The agent should ask for what it needs, and credentials should be entered privately on the TV rather than copied into chat or committed.

## Copy-and-paste prompt

```text
Help me build, install, and test Orsay Cinema on my own legacy Samsung TV.

Read README.md, AGENTS.md, PRIVACY.md, SECURITY.md, and the build/test scripts in this repository first. Work from the current source rather than assuming old Samsung instructions still apply. Explain things in plain language and give me one short set of TV remote steps at a time. Do the computer-side work you can actually perform; tell me clearly which taps I must do on the physical TV. Do not claim you can see or control the TV unless a working tool proves that.

My intended result is a standalone app installed on the TV. Browsing, playback, on-demand transcoding, subtitle search, download, and selection must connect directly to my Plex server. The coding or installation computer must not be needed after installation.

Start by checking the repository and available tools. Then ask only for missing information:
- My Samsung TV model, firmware, and whether it is pre-Tizen Orsay or Tizen.
- The installation computer's operating system and local network address.
- Whether the TV and my authorized Plex server can reach each other.
- Whether other developer-installed apps must be preserved.

Do not assume every old Samsung TV is supported. The tested baseline is the H6203 on firmware 1230; other hardware and the generic setup/token workflow need explicit verification. If my TV is Tizen, stop the Orsay installation path and explain the mismatch.

With the information I provide:
1. Inspect prerequisites. Run the documented JavaScript and Python checks. Build the widget using the standard-library build script. If a prerequisite is missing, explain what needs installing and follow the tool's normal approval rules.
2. Distinguish the installation computer's address, used in the developer sync catalog, from the Plex server's address, entered on the TV. Never bake either address, account details, tokens, media paths, screenshots of my library, or logs into tracked source.
3. Preserve all existing developer apps in the sync catalog, with separate app identities and their package files available. Do not replace an existing multi-app catalog with a one-app list. Explain this before syncing.
4. Serve only the generated dist directory over the local network for installation. Do not expose my home folder, create internet port forwarding, or install a permanent background service.
5. Walk me through the relevant TV steps: developer login, Apps, holding OK, IP Setting, saving the installation computer address, and Start User App Sync. On the tested model this is the develop account, not the Tizen developer-mode process. Menus can differ by firmware; ask what is visible rather than guessing. Blank IP boxes after reopening do not by themselves prove that saving failed.
6. Verify a real request from my TV for widgetlist.xml and the expected widget ZIP. A message saying sync requested is not proof of download or successful installation.
7. Have me reopen Smart Hub and launch Orsay Cinema. Guide me through entering my Plex server address and, if required, my own token privately on the TV. Never ask me to disable authentication, share a password/token in chat, or publish credentials. Do not change Plex security settings, reset Smart Hub, uninstall unrelated apps, root the TV, or flash firmware as a shortcut.
8. Test Movies, TV Shows, poster scrolling, alphabet jumps, filters/sorting, direct playback, a file requiring compatibility playback, pause/seek, resume, and a fresh subtitle search/download/selection. A server conversion decision is not proof that picture, sound, or subtitles actually display. Wait for the TV result before marking each item passed.
9. Stop the installation server. Fully close and reopen the TV app, then repeat playback and a fresh subtitle operation. This is the independence test: no requests should need the installation computer. Also have me reopen after a normal TV restart to check the installed app persists.
10. Give me a short result: what was installed, checks that passed, anything unverified, how to change the Plex connection, how to stop/remove the temporary installer, and how to recover using the package backup. Keep private notes and generated catalogs out of Git.

Make only changes needed for this installation or a clearly identified compatibility fix. Keep ES5-compatible code for the old browser. If you find a bug, reproduce it, make the smallest relevant correction, run appropriate checks, and explain the next TV test. Do not publish my local changes or contact other people without my instruction.

If a step needs my action, request the specific action and continue independent computer-side work when possible. Do not say the installation is complete until the TV tests and the installation-server-off test have passed, or clearly state the remaining blocker.
```

## Short prompt for an existing install

```text
Read this repository's README.md and AGENTS.md, then help me diagnose my Orsay Cinema installation. Start with read-only checks, identify my TV model/firmware and installed app version, and distinguish installation-computer, TV, and Plex-server addresses. Keep credentials and private library data out of logs and Git. Preserve standalone operation and other developer apps. Reproduce the issue before changing code, then run appropriate checks and guide me through only the TV test needed to verify the fix. Do not reset the TV, weaken authentication, or claim a TV result from a desktop-only test.
```

## What the agent can and cannot do

An agent with local tools can inspect source, run tests, build the widget, prepare the catalog, start/stop the installer, and examine its request log. You still operate the TV remote and confirm actual picture, sound, subtitle timing, and menu behavior. Browser previews and simulated tests cannot certify hardware support.

Repository guidance for Codex follows the documented [AGENTS.md mechanism](https://developers.openai.com/codex/guides/agents-md/). CLAUDE.md points other agent workflows to the same project guidance. Agent features and approval policies vary; this prompt does not override them.
