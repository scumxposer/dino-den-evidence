# 01 — How Patreon money reaches the casino games

Figures were captured on 27 October 2026 from The Dino Den's public API without logging in, unless another source is named (site pages, Discord screenshots or a patron's screenshot). Raw data: [snapshots/2026-10-27/api-snapshot.json](snapshots/2026-10-27/api-snapshot.json).

## Step 1 — Patreon tiers pay AmberShards

Source: <https://api.dinoden.gg/patreon/tiers>

| Tier | Price on the site's Patreon page | AmberShards every 14 days | Troodons this buys (1,000 AS each) | ClawCoin earning multiplier |
|---|---|---|---|---|
| Juvie | £12 | 18,000 | 18 | 1.5x |
| Sub | £22 | 28,000 | 28 | 2x |
| Adult | £33 | 40,000 | 40 | 2.5x |
| Elder | £44 | 60,000 | 60 | 3x |
| Apex | £55 | 80,000 | 80 | 4.5x |

- The price column is shown on <https://main.dinoden.gg/patreon> (from the `minCents` setting; the site always shows it in pounds). Patreon charges US viewers $17.50–$79 a month, 7.5–9.5% more than these prices converted at the market rate. See [DISCREPANCIES.md §2](../DISCREPANCIES.md#2-patreon-prices-vs-the-sites-tier-minimums).
- The operator's FAQ (<https://main.dinoden.gg/faq>): *"Active patrons receive their tier's AmberShards every 14 days… Tier upgrades grant the difference between the tiers immediately."*
- **Apex multiplier is stated inconsistently.** The multiplier column shows the configured `clawcoinBoost` values. For Apex, the tier's own description says *"Maximum 3.5x Clawcoin boost"* and Patreon showed 3.5x, while the configured value is `4.5`. Which rate members actually receive can't be verified, and the configured value is in members' favour. Sources: [DISCREPANCIES.md §1](../DISCREPANCIES.md#1-apex-clawcoin-boost-35x-or-45x).

### Other patron perks

The site's patron-only "Patreon Access" page (<https://main.dinoden.gg/subscriber>) offers *"Live server population, species unlocks and the skin designer for patrons."* Patrons can unlock a capped species on a server for a limited time (Dino Den caps each species per server). The site's code treats an unlock as a server-wide state (*"Unlocks on [server] only"*, *"Already unlocked on this server"*), and players say it benefits everyone there; a separate *"respawn"* mode respawns the patron as the species. Some species need a minimum tier: Tyrannosaurus is marked "APEX+" in a patron's October 2026 screenshot, and a Senior Admin wrote on 9 Oct 2026 that *"Allos and rexes can be unlock if you are APEX patreon, otherwise its popcontrol on them"* ([screenshot](screenshots/2026-10-09-discord-senior-admin-apex-unlock.png)). See [DISCREPANCIES.md §11](../DISCREPANCIES.md#11-patreon-perks-discord-announcement-vs-the-sites-patreon-page).

### Other ways to get AmberShards (for balance)

Patreon is not the only source. The operator's weekly "Daily Rewards" posts offer free login rewards (for the week of 26 Oct – 2 Nov 2026: *"up to 58.0k Clawcoins, 786 AmberShards"* — <https://api.dinoden.gg/news/daily-rewards-2026-10-26>), and the [Dino Den Rewards](https://den.dinoden.gg/twitch/leaderboard) Twitch program lets viewers *"earn ClawCoins and AmberShards"* for watching Dino Den streams (lifetime totals as displayed on that page, 27 Oct 2026: 734M ClawCoins and 32M AmberShards across 7,492 viewers). For scale: a week of free login rewards gives up to 786 AmberShards, while the lowest Patreon tier gives 18,000 every two weeks.

## Step 2 — AmberShards buy dinosaurs

Source: <https://api.dinoden.gg/shop/dinos>

The Dino Shop sells 22 species priced in AmberShards: from 1,000 AS (Troodon, Pteranodon, Beipiaosaurus, Dryosaurus, Hypsilophodon) up to 6,000 AS for a Tyrannosaurus or Triceratops (7,000 AS as a prime). Full price list in the snapshot. The site's purchase code deducts the price from the account's AmberShard balance.

The operator's own Discord announcement (8 Dec 2025) describes this step for patrons: *"Bi-weekly Amber Shards – use them to instantly purchase full-grown dinos!"* ([screenshot](screenshots/2025-12-08-discord-support-the-server.png); see [DISCREPANCIES.md §11](../DISCREPANCIES.md#11-patreon-perks-discord-announcement-vs-the-sites-patreon-page)).

## Step 3 — Shop dinosaurs are sold to other players for ClawCoins

Source: <https://api.dinoden.gg/market/listings>

- The Marketplace lists dinosaurs for sale in ClawCoins (the listing form labels prices with the site's ClawCoins name). Listing fees seen ranged from 10% to 25%.
- Dinosaurs bought from the Dino Shop carry an ID that starts `shop-<offer id>-…`. The offer ids match the Dino Shop's own offer numbers (for example `shop-21-` = Tyrannosaurus, `shop-38-` = Troodon).
- On 27 October 2026 at 08:33 UTC, **117 of 877 active listings** carried `shop-` IDs, covering 17 shop offers. 16 of these are in the current Dino Shop; one (offer 41, one Beipiaosaurus listing) is not, and may be a retired offer. The largest groups:

| Shop offer | Dinosaur | Listings |
|---|---|---|
| 21 | Tyrannosaurus | 37 |
| 38 | Troodon | 37 |
| 24 | Deinosuchus | 8 |
| 34 | Omniraptor | 6 |
| 39 | Pteranodon | 6 |

Example listing ids: 913900, 913902–913906 (six Troodons listed within four minutes by one seller), 913963 (Allosaurus), 913976 (Deinosuchus).

Dinosaurs are also sold for ClawCoins through **Auctions** (<https://api.dinoden.gg/auctions>; 10% fee seen). On 27 Oct 2026 at about 10:40 UTC, 2 of 17 active auctions were dinosaurs with `shop-` IDs, one of them a Tyrannosaurus (`shop-21-`). Not in the 08:33 UTC snapshot.

**Limits of this step:**
- Reading `shop-` as "bought from the Dino Shop" is an interpretation of the ID format, which the site does not document. The second part matches the shop's offer numbers. The third part equals the seller's account number in most listings (83 of 104 `shop-` listings at about 17:55 UTC on 27 Oct 2026); where it differs, the dinosaur has probably changed hands, so the third part is most likely the original buyer.
- Listings show asking prices, not completed sales.

## Step 4 — ClawCoins are wagered

ClawCoins are the stake in the site's casino-style games and the price of most crates. The operator's FAQ: *"You can also win (or lose...) ClawCoins in our casino games."* Details in [02-casino-games-and-raffle.md](02-casino-games-and-raffle.md).

## The second route: the ClawCoin multiplier

Every tier multiplies the ClawCoins a player earns from playtime, quests and rewards (1.5x to 4.5x as configured; the Apex tier is described as 3.5x, see [DISCREPANCIES.md §1](../DISCREPANCIES.md#1-apex-clawcoin-boost-35x-or-45x)). The FAQ: *"Patreon tiers add a ClawCoin boost on top."* So a paying member gets more of the wagering currency directly, without going through the shop.

## Worked example

A Juvie member (£12 a month on the site; $17.50 on Patreon for US viewers) receives 18,000 AmberShards every two weeks. That buys 18 Troodons from the Dino Shop. Each can be listed on the Marketplace for ClawCoins, which can then be wagered.
