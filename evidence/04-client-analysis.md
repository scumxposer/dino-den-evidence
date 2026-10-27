# 04 — The DinoDen Client: what it does and does not do

A static review of the DinoDen Client for Windows, version 0.2.0 (released 29 September 2026). Nothing was executed. This file describes findings only; it does not reproduce the client's code.

## Summary

The client is an Electron desktop app: proximity voice chat with push-to-talk, an in-game overlay (minimap, vitals, chat, quests) and account features. **No code was found that reads game memory, injects into the game or modifies game files**, which matches the operator's claim. Its main privacy-relevant feature is a system-wide keyboard and mouse hook used for push-to-talk and hotkeys.

## What was checked

| Area | Finding |
|---|---|
| Memory access / injection | None. No use of `ReadProcessMemory`, `OpenProcess`, `WriteProcessMemory`, `CreateRemoteThread` or similar. |
| Native Windows calls | Only `user32.dll`, via the `koffi` FFI library: finding The Isle's window (`UnrealWindow`, process `TheIsleClient`), reading its size and position, checking focus, and bringing a window to the front (using a simulated Alt key press, a common workaround). |
| Keyboard and mouse | `uiohook-napi`, a system-wide input hook. Key presses are compared against configured hotkeys and push-to-talk; no code was found that logs or transmits key presses. |
| Where in-game data comes from | The minimap, vitals and allies come from the operator's servers (`api.dinoden.gg`), not from the user's PC. The minimap draws only the user's group and clan mates. |
| Network | Only `dinoden.gg` / `api.dinoden.gg` and LiveKit (voice). The computer's hostname is sent once at sign-in. |
| Stored credentials | Login token stored with Windows' built-in encryption (Electron `safeStorage`). |
| Permissions | Microphone and notifications only. No screen capture is used. |
| Updates | Checks `api.dinoden.gg/client/releases` every 2 minutes and installs updates automatically. The server can also disable the client or gate it per account. |
| `elevate.exe` | A standard helper (Johannes Passing's "Elevate", 2007) bundled by the Electron build tool to run installers with admin approval. Normal. |

## Features exposed through the client

Park, prime, slay and pause-growth for the player's live dinosaur; teleport to friends; redeeming dinosaurs and skins from the website inventory; quest rewards paid in ClawCoins, AmberShards and Pumpkins; and the player's Patreon tier (read from `/client/me`).

## Caveats

- This covers version 0.2.0 only. Automatic updates mean future versions could behave differently.
- The `app.asar` reviewed did not match the integrity hash recorded in the executable reviewed alongside it, most likely because they came from different builds. This is not evidence of tampering.
- The installer is unsigned; Windows shows an "unknown publisher" warning.
