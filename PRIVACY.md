# Privacy

The app stores the chosen Plex server address, optional Plex token, app preferences, subtitle choices and resume positions in the TV browser's local storage. It has no project-operated analytics or cloud service.

Requests go to the configured Plex server for library metadata, posters, playback, transcoding and subtitle operations. When requested, Plex contacts its subtitle provider; the search can disclose the media title, release/hash information, language and related request details to Plex/provider infrastructure. Those services' own privacy policies apply.

A Plex token is a credential. Legacy local storage is not an encrypted credential vault. The token can be included in request URLs where required by the TV player or image loader, so it may appear in local server/network logs. Only configure a TV and network you trust. Changing the configured server clears the stored token. Do not share a token, storage export or private logs in an issue.

The temporary installer serves generated package/catalog files only and can be stopped after installation. Your actual server address and token are entered on the TV; neither belongs in the source repository. Uninstall/reset behavior for local storage varies by TV firmware.
