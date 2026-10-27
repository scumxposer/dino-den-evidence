# Discrepancies, with sources

Every place where two sources disagree, side by side. Each item names both sources, when they were read, and what can and cannot be concluded. Unless stated otherwise, sources were read on **27 October 2026** without logging in; API values are preserved in [the snapshot](evidence/snapshots/2026-10-27/api-snapshot.json).

---

## 1. Apex ClawCoin boost: 3.5x or 4.5x?

| Source | Says |
|---|---|
| Apex tier **description** in the site's tier configuration — <https://api.dinoden.gg/patreon/tiers> (field `description`) | *"Maximum 3.5x Clawcoin boost"* |
| Apex tier **configured value**, same endpoint (field `clawcoinBoost`) | `4.5` |
| The site's own code, which builds the perk badge shown on Dino Den's Patreon pages from `clawcoinBoost` (template `` `${clawcoinBoost}x Clawcoin Boost` ``, seen in the site's JavaScript on 27 Oct 2026) | would display **4.5x** |
| Patreon tier page for [patreon.com/TheDinoDen](https://www.patreon.com/TheDinoDen), as captured in the author's screenshots for the 26 Oct 2026 report to Patreon | 3.5x |

**Can be concluded:** Dino Den states two different multipliers for the same tier. The other four tiers' descriptions match their configured values (Sub "double" = 2, Adult "2.5x" = 2.5, Elder "triple" = 3).
**Cannot be concluded:** which multiplier members actually receive — earnings are calculated on Dino Den's servers. The configured value is *higher* than advertised, so if it is applied, members get more than promised. This is an inconsistency, not evidence of members being short-changed.

## 2. Patreon prices vs the site's tier minimums

| Source | Juvie | Sub | Adult | Elder | Apex |
|---|---|---|---|---|---|
| Site setting `minCents` — <https://api.dinoden.gg/patreon/tiers> | $12 | $22 | $33 | $44 | $55 |
| Patreon page, discounted price shown during a 40% promotion (author's screenshots, Oct 2026) | $10.50 | $18.90 | $28.50 | $37.80 | $47.40 |
| Patreon full price implied by the 40% discount (calculated) | $17.50 | $31.50 | $47.50 | $63.00 | $79.00 |

**Can be concluded:** the site's per-tier minimums do not match the prices Patreon displays.
**Cannot be concluded:** what `minCents` is used for. It may be a threshold the site uses to match pledges to tiers rather than a price. The Patreon screenshots are not reproduced here; check current prices on [the Patreon page](https://www.patreon.com/TheDinoDen).

## 3. Age requirement changed

| Source | Says |
|---|---|
| Terms of Service, last updated 2026-01-20, archived 2 April 2026 — <https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms> (§4 Eligibility) | *"If you are a minor, you may use the Service only with the consent of a parent or legal guardian (where required by law)."* |
| Current Terms of Service, last updated 11 June 2026 — <https://main.dinoden.gg/tos> (§1) | *"You must be at least 18 years old to use the service."* |
| Current Privacy Policy, last updated 11 June 2026 — <https://main.dinoden.gg/privacy> | *"The service is intended for adults and not directed at anyone under 18."* |
| The author's own sign-in (October 2026) | No age check or parental-consent step before reaching the games, shop and marketplace |

**Can be concluded:** the operator moved from allowing minors (with consent) to adults-only in June 2026. The original site, na.dinoden.gg, is currently offline (error 521); the archived copy is the source.
**Cannot be concluded:** whether an age check has been added since the author's sign-in; it has not been re-tested.

## 4. "Not gambling" vs the operator's own descriptions

| Source | Says |
|---|---|
| Current Terms §2 — <https://main.dinoden.gg/tos> | games *"are played exclusively with virtual currency, are provided for entertainment only and are not gambling for money or anything of monetary value."* |
| Earlier Terms §7 "Chance-Based Games (Entertainment Only)" — [archived copy](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms) | *"Any chance-based features (including, without limitation, coin flips, jackpots, loot boxes, plinko, spins, raffles, or similar mechanics)…"* |
| FAQ — <https://main.dinoden.gg/faq> | *"A casino game crashed or did not pay out."*; *"You can also win (or lose...) ClawCoins in our casino games."*; *"Can I set gambling limits or exclude myself?"* |
| Patreon tiers, Dino Shop and Marketplace data — see [evidence/01](evidence/01-patreon-to-casino.md) | paid tiers supply the currencies that end up wagered |

**Can be concluded:** the operator itself describes the games as casino and chance-based games with gambling controls, while its Terms say they are not gambling for anything of value.
**Cannot be concluded:** whether this meets any legal definition of gambling. That is for Patreon and regulators to judge.

## 5. "Memberships are not purchases of Virtual Items"

| Source | Says |
|---|---|
| Current Terms §3 — <https://main.dinoden.gg/tos> | *"memberships are not purchases of Virtual Items"* |
| Tier configuration — <https://api.dinoden.gg/patreon/tiers> | each tier is defined by `amberShardsBiWeekly` (18,000–80,000 AmberShards every 14 days) |
| FAQ — <https://main.dinoden.gg/faq> | *"Active patrons receive their tier's AmberShards every 14 days… Tier upgrades grant the difference between the tiers immediately."* |

## 6. Games menu vs games switched on

| Source | Says |
|---|---|
| Games menu in the site footer — <https://main.dinoden.gg> | Roll, Crash, Blackjack, Crates, Coinflip |
| Feature switches — <https://api.dinoden.gg/features> | also `game.jackpot: true` and `game.poker: true`; `game.slots`, `game.viking`, `game.mines` false |

**Can be concluded:** jackpot and poker are enabled but not listed in the menu. **Cannot be concluded:** whether they are reachable by ordinary players (the site's code contains routes for both).

## 7. Server-browser player counts vs measured behaviour

| Source | Says |
|---|---|
| In-game server browser (as recorded by trackers) | e.g. [NA #1] THE DINO DEN at 357/475 at 09:05 UTC on 27 Oct 2026 |
| [TheSpoofingIsle — NA #1](https://thespoofingisle.com/server/51.222.255.170%3A7777), [EU #2](https://thespoofingisle.com/server/45.88.230.190%3A7777) (read ~09:00 UTC, 27 Oct 2026) | "Spoofing" scores 75 and 83; join bursts up to +173 players in 3 minutes; refills faster than clients can load after restarts; ~15-minute repeating curve |
| Kadin's EOS session check (Discord post, ~Nov 2025; screenshot held by the author) | most listed players on "The Dino Den" and "NERF Official" were not real |

**Cannot be concluded:** that counts are definitely faked. The tracker's restart check also fires on an official developer server ([Official US 1](https://thespoofingisle.com/server/172.237.147.22%3A31067)), and the 15-minute pattern appears on unrelated servers (e.g. [ORIGIN](https://thespoofingisle.com/server/216.39.241.102%3A7777)). Dino Den's own public data (raffle tickets, playtime leaderboard) neither confirms nor rules out the displayed counts. Full detail: [community-reports.md](community-reports.md#inflated-player-counts).

## 8. Privacy policy vs the DinoDen Client

| Source | Says |
|---|---|
| Privacy Policy — <https://main.dinoden.gg/privacy> | lists IP address, browser user agent, SteamID and gameplay data; no mention of the desktop client |
| DinoDen Client v0.2.0, static review ([evidence/04](evidence/04-client-analysis.md)) | sends the computer's hostname (`deviceName`) once at sign-in; uses the microphone for proximity voice |

**Can be concluded:** the policy does not describe data the client sends. This is a documentation gap, not evidence of misuse.

---

## Checked, no discrepancy found

| Claim by Dino Den | Source | Result |
|---|---|---|
| The client *"does not inject anything into The Isle, does not read game memory and does not modify game files"* — <https://main.dinoden.gg/dinoden-client> | Static review of v0.2.0 ([evidence/04](evidence/04-client-analysis.md)) | No such code found |
| Client is *"Free for every Dino Den player"* | `client.patreonOnly: false` at <https://api.dinoden.gg/features> | Consistent |
| *"the only real-money support is our Patreon"* (FAQ) | Site code and API | No other real-money store found |
