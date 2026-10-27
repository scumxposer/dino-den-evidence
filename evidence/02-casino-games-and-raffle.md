# 02 — Casino games, the raffle and crates

Captured 27 October 2026. Raw data: [snapshots/2026-10-27/api-snapshot.json](snapshots/2026-10-27/api-snapshot.json).

## The operator calls them casino games

From The Dino Den's FAQ (`https://main.dinoden.gg/faq`):

- *"A casino game crashed or did not pay out."* — the heading of one FAQ entry.
- *"How do I earn ClawCoins? … Patreon tiers add a ClawCoin boost on top. You can also win (or lose...) ClawCoins in our casino games."*
- *"Can I set gambling limits or exclude myself? Yes. You can self-exclude from all casino games."*

The site's Games menu lists Roll, Crash, Blackjack, Crates and Coinflip.

## Games switched on

Source: `https://api.dinoden.gg/features`

| Switched on | Switched off |
|---|---|
| blackjack, coinflip, crash, crates, roll, **jackpot**, **poker** | mines, slots, "viking" (a second slot machine) |

Jackpot and poker are switched on but do not appear in the Games menu as of 27 October 2026. Slots and the "viking" slot machine exist in the site's code but are switched off.

## A double-or-nothing flip only for patrons

From the FAQ: after server downtime, *"everyone who was an active patron during the outage can claim compensation… take it straight up, or flip a coin up to 3 times to double it each time. Careful: one lost flip and it is gone."*

## The weekly raffle rewards wagering

Source: `https://api.dinoden.gg/raffle/current`

- Tickets come from two sources: **10 per hour played** and **1 per 100,000 ClawCoins wagered**.
- Neither source is capped (`maxPlaytimeTickets: 0`, `maxWagerTickets: 0`; the site's code only applies a cap when the value is above 0).
- Prize pool: **100,000,000 ClawCoins** a week across 20 places (top prize 25,000,000).

| Raffle | Dates (UTC) | Entrants | Tickets |
|---|---|---|---|
| #5 (open) | 25 Oct – 1 Nov 2026 | 12,206 so far | 737,023 so far |
| #4 | 18 – 25 Oct 2026 | 22,908 | 3,708,647 |

## Crates

Source: `https://api.dinoden.gg/games/crates`

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

Source: The Dino Den's own news posts (`https://api.dinoden.gg/news`) and Item Shop (`https://api.dinoden.gg/shop/items`), read 27 October 2026.

- A new "edition" of Lucky Bags has been announced every 14 days since May 2026 (Edition #4 on 2 May to Edition #17 on 26 October), each with *"Clawcoin prizes up to 20000k CC jackpot."*
- Edition #17 lists five bag tiers with random ClawCoin prizes and jackpots, for example Common *"Up to 5k CC · Jackpot: 500k CC"* and Rare *"Up to 50k CC · Jackpot: 5000k CC"*, plus random decorations.
- In the Item Shop, bags are sold in limited stock: Epic and Legendary bags for 10–15 Pumpkins (the Halloween event currency), and one Legendary Lucky Bag for 250,000 ClawCoins.

## An item that changes odds

The site's code defines a consumable labelled *"Lucky — Better RNG on lucky bags & games."* How players obtain it could not be confirmed.
