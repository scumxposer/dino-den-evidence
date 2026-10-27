# 02 — Casino games, the raffle and crates

Captured 27 October 2026. Raw data: [snapshots/2026-10-27/api-snapshot.json](snapshots/2026-10-27/api-snapshot.json).

## The operator calls them casino games

From The Dino Den's FAQ (<https://main.dinoden.gg/faq>):

- *"A casino game crashed or did not pay out."* — the heading of one FAQ entry.
- *"How do I earn ClawCoins? … Patreon tiers add a ClawCoin boost on top. You can also win (or lose...) ClawCoins in our casino games."*
- *"Can I set gambling limits or exclude myself? Yes. You can self-exclude from all casino games."*

The account settings shown to signed-in players (text from the site's JavaScript, read 27 Oct 2026) go further. A section titled *"Gambling Self-Exclusion"* says: *"Lock yourself out of all gambling games (Crash, Roll, Mines, Blackjack) for a fixed period."* Once set, it shows *"Gambling locked"*. The list names four games, while the FAQ says self-exclusion covers *"all casino games"*; whether it also blocks Coinflip, Jackpot and Crates could not be checked. See [DISCREPANCIES.md §4](../DISCREPANCIES.md#4-not-gambling-vs-the-operators-own-descriptions).

The earlier Terms of Service (20 January 2026, [archived](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms)) had a section titled *"Chance-Based Games (Entertainment Only)"* covering *"coin flips, jackpots, loot boxes, plinko, spins, raffles, or similar mechanics."*

The site's main navigation menu lists Roll, Crash, Blackjack, Coinflip, Jackpot and Crates; the footer list leaves out Jackpot.

## Games switched on

Source: <https://api.dinoden.gg/features>

| Switched on | Switched off |
|---|---|
| blackjack, coinflip, crash, crates, roll, **jackpot**, **poker** | mines, slots, "viking" (a second slot machine) |

Jackpot is live and in the main menu. Poker (*"Texas Hold'em — Provably Fair"*) is switched on but not in any menu, and its page sends any account below role level 40 (apparently staff) back to the home page, so ordinary players cannot use it. Slots, the "viking" slot machine and mines exist in the site's code but are switched off. See [DISCREPANCIES.md §6](../DISCREPANCIES.md#6-games-menu-vs-games-switched-on).

## Jackpot

Source: <https://main.dinoden.gg/games/jackpot> and its "How it works" panel, read 27 Oct 2026 (the page loads without signing in).

- *"Every bet goes into one shared pot… Your chance to win is your share of the pot, and one player wins all of it."* Players bet against each other, not against the house.
- Three rooms: *"Low 10,000 to 250,000 CC, Mid 250,000 to 2,500,000 CC, High 2,500,000 to 25,000,000 CC"* per player per round.
- *"The winner receives the pot minus a 2.5% tax."* The site keeps a cut of every pot.
- The draw is described as "provably fair": a secret server seed is combined with the hash of *"a future EOS block"* (EOS appears to mean the EOS blockchain) to pick the winning ticket.
- The round counter shown in the Low room read #17,088 at about 10:40 UTC on 27 Oct 2026.

## A double-or-nothing flip only for patrons

From the FAQ: after server downtime, *"everyone who was an active patron during the outage can claim compensation… take it straight up, or flip a coin up to 3 times to double it each time. Careful: one lost flip and it is gone."*

## The weekly raffle rewards wagering

Source: <https://api.dinoden.gg/raffle/current>

- Tickets come from two sources: **10 per hour played** and **1 per 100,000 ClawCoins wagered**.
- Neither source is capped (`maxPlaytimeTickets: 0`, `maxWagerTickets: 0`; the site's code only applies a cap when the value is above 0).
- Prize pool: **100,000,000 ClawCoins** a week across 20 places (top prize 25,000,000).

| Raffle | Dates (UTC) | Entrants | Tickets |
|---|---|---|---|
| #5 (open) | 25 Oct – 1 Nov 2026 | 12,206 so far | 737,023 so far |
| #4 | 18 – 25 Oct 2026 | 22,908 | 3,708,647 |

## Crates

Source: <https://api.dinoden.gg/games/crates>

25 crates are active: 22 priced in ClawCoins and 3 seasonal crates priced in Pumpkins. The site's code allows dinosaurs, skins, ClawCoins and AmberShards as crate drops, and also supports pricing crates in AmberShards (none are priced that way today). Most crates are made by players, who receive a 0.5% revenue share.

| Crate | Price (ClawCoins) | Times opened |
|---|---|---|
| Hidden In Plain Sight | 25,000 | 5,423,186 |
| I'm only loooosing | 9,999.99 | 4,281,490 |
| Irie's Crate 2 | 69,148 | 379,195 |
| 1 in 1000 | 19,058 | 121,008 |
| Money Money Money! | 70,719 | 111,198 |
| Go Big or Go Broke | 544,069 | 7,865 |

Six of 25 shown; the full list is in the snapshot.

## Lucky Bags

Source: The Dino Den's own news posts (<https://api.dinoden.gg/news>) and Item Shop (<https://api.dinoden.gg/shop/items>), read 27 October 2026.

- A new "edition" of Lucky Bags has been announced roughly every two weeks since May 2026: Edition #4 on 2 May, #5 on 11 May, then every 14 days up to Edition #17 on 26 October. Edition #17 advertises *"Clawcoin prizes up to 20000k CC jackpot."*
- Edition #17 lists five bag tiers with random ClawCoin prizes and jackpots, for example Common *"Up to 5k CC · Jackpot: 500k CC"* and Rare *"Up to 50k CC · Jackpot: 5000k CC"*, plus random decorations.
- In the Item Shop, 13 bags are listed in limited stock: Epic bags for 10 Pumpkins and Legendary bags for 15 Pumpkins (the Halloween event currency), and one Legendary Lucky Bag for 250,000 ClawCoins. On 27 October 2026 all 13 showed no stock remaining.

## An item that changes odds

The site's code defines a consumable labelled *"Lucky — Better RNG on lucky bags & games."* How players obtain it could not be confirmed.
