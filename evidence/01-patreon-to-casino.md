# 01 — How Patreon money reaches the casino games

All figures captured 27 October 2026 from The Dino Den's public API, without logging in. Raw data: [snapshots/2026-10-27/api-snapshot.json](snapshots/2026-10-27/api-snapshot.json).

## Step 1 — Patreon tiers pay AmberShards

Source: <https://api.dinoden.gg/patreon/tiers>

| Tier | Minimum pledge (site setting) | AmberShards every 14 days | Troodons this buys (1,000 AS each) | ClawCoin earning multiplier |
|---|---|---|---|---|
| Juvie | $12 | 18,000 | 18 | 1.5x |
| Sub | $22 | 28,000 | 28 | 2x |
| Adult | $33 | 40,000 | 40 | 2.5x |
| Elder | $44 | 60,000 | 60 | 3x |
| Apex | $55 | 80,000 | 80 | 4.5x |

- The pledge column is the site's own `minCents` setting, not the price on Patreon. Patreon displayed different prices in October 2026 ($10.50–$47.40 during a 40% promotion). See [DISCREPANCIES.md §2](../DISCREPANCIES.md#2-patreon-prices-vs-the-sites-tier-minimums).
- The operator's FAQ (<https://main.dinoden.gg/faq>): *"Active patrons receive their tier's AmberShards every 14 days… Tier upgrades grant the difference between the tiers immediately."*
- **Apex multiplier is stated inconsistently.** The multiplier column shows the configured `clawcoinBoost` values. For Apex, the tier's own description says *"Maximum 3.5x Clawcoin boost"* and Patreon showed 3.5x, while the configured value is `4.5`. Which rate members actually receive can't be verified, and the configured value is in members' favour. Sources: [DISCREPANCIES.md §1](../DISCREPANCIES.md#1-apex-clawcoin-boost-35x-or-45x).

### Other ways to get AmberShards (for balance)

Patreon is not the only source. The operator's weekly "Daily Rewards" posts offer free login rewards (for the week of 26 Oct – 2 Nov 2026: *"up to 58.0k Clawcoins, 786 AmberShards"* — <https://api.dinoden.gg/news/daily-rewards-2026-10-26>), and the [Dino Den Rewards](https://den.dinoden.gg/twitch/leaderboard) Twitch program lets viewers *"earn ClawCoins and AmberShards"* for watching Dino Den streams (lifetime totals shown: 734M ClawCoins and 32M AmberShards across 7,492 viewers). For scale: a week of free login rewards gives up to 786 AmberShards, while the lowest Patreon tier gives 18,000 every two weeks.

## Step 2 — AmberShards buy dinosaurs

Source: <https://api.dinoden.gg/shop/dinos>

The Dino Shop sells 22 species priced in AmberShards: 1,000 AS for a Troodon, Pteranodon or Beipiaosaurus, up to 6,000 AS for a Tyrannosaurus or Triceratops (7,000 AS as a prime). The site's purchase code deducts the price from the account's AmberShard balance.

## Step 3 — Shop dinosaurs are sold to other players for ClawCoins

Source: <https://api.dinoden.gg/market/listings>

- The Marketplace lists dinosaurs for sale in ClawCoins (the listing form labels prices with the site's ClawCoins name). Listing fees seen ranged from 10% to 25%.
- Dinosaurs bought from the Dino Shop carry an ID that starts `shop-<offer id>-…`. The offer ids match the Dino Shop's own offer numbers (for example `shop-21-` = Tyrannosaurus, `shop-38-` = Troodon).
- On 27 October 2026 at 08:33 UTC, **117 of 877 active listings** carried `shop-` IDs, covering 17 shop offers. The largest groups:

| Shop offer | Dinosaur | Listings |
|---|---|---|
| 21 | Tyrannosaurus | 37 |
| 38 | Troodon | 37 |
| 24 | Deinosuchus | 8 |
| 34 | Omniraptor | 6 |
| 39 | Pteranodon | 6 |

Example listing ids: 913900, 913902–913906 (six Troodons listed within four minutes by one seller), 913963 (Allosaurus), 913976 (Deinosuchus).

**Limits of this step:**
- Reading `shop-` as "bought from the Dino Shop" is an interpretation of the ID format. The second part matches the shop's offer numbers and the third part matches the seller's account number; the site does not document the format.
- Listings show asking prices, not completed sales.

## Step 4 — ClawCoins are wagered

ClawCoins are the stake in the site's casino-style games and the price of most crates. The operator's FAQ: *"You can also win (or lose...) ClawCoins in our casino games."* Details in [02-casino-games-and-raffle.md](02-casino-games-and-raffle.md).

## The second route: the ClawCoin multiplier

Every tier multiplies the ClawCoins a player earns from playtime, quests and rewards (1.5x to 4.5x). The FAQ: *"Patreon tiers add a ClawCoin boost on top."* So a paying member gets more of the wagering currency directly, without going through the shop.

## Worked example

A Juvie member ($12 minimum) receives 18,000 AmberShards every two weeks. That buys 18 Troodons from the Dino Shop. Each can be listed on the Marketplace for ClawCoins, which can then be wagered.
