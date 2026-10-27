# Verify it yourself

Every documented figure here comes from public pages and public API endpoints that anyone can open in a browser, without logging in. Values may have changed since 27 October 2026.

## Pages (open normally)

| Page | What to look for |
|---|---|
| <https://main.dinoden.gg/faq> | "casino games", self-exclusion, Patreon AmberShard payouts, patron-only coin flip |
| <https://main.dinoden.gg/tos> | §1 age requirement, §2 virtual items and games, §3 Patreon |
| <https://main.dinoden.gg/privacy> | data collected, "intended for adults" |
| [Earlier Terms, archived 2 Apr 2026](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms) | §4 minors allowed with parental consent; §7 "Chance-Based Games" |
| <https://main.dinoden.gg/dinoden-client> | client claims (no injection, free) |
| <https://find-and-update.company-information.service.gov.uk/company/16970676> | THE DINO DEN LTD company record |
| <https://www.patreon.com/TheDinoDen> | current tier prices and stated perks (compare with `/patreon/tiers`) |
| <https://thespoofingisle.com> | third-party player-count analysis (search "DINO DEN") |

These pages load their content with JavaScript, so use a normal browser.

## API endpoints (open in a browser tab; they return JSON)

| Endpoint | What it shows |
|---|---|
| <https://api.dinoden.gg/patreon/tiers> | Tier pledges (`minCents`), AmberShards (`amberShardsBiWeekly` ÷ 100), ClawCoin multiplier (`clawcoinBoost`) |
| <https://api.dinoden.gg/shop/dinos> | Dino Shop prices (`priceNormal` ÷ 100 = AmberShards) and offer ids |
| <https://api.dinoden.gg/market/listings?page=1&limit=100&sort=newest> | Marketplace listings; look for `dino.uniqueID` values starting `shop-` |
| <https://api.dinoden.gg/features> | Which games are switched on |
| <https://api.dinoden.gg/raffle/current> | Raffle ticket rates (`wagerPerTicket` ÷ 100 = ClawCoins), prize pool, entrants |
| <https://api.dinoden.gg/games/crates> | Crate prices (÷ 100) and how often each was opened (`_count.openings`) |
| <https://api.dinoden.gg/platform-config> | Currency names, Patreon URL |

## Units

The site stores currency amounts in hundredths. Divide `price`, `priceNormal`, `amberShardsBiWeekly`, `prizePool` and `wagerPerTicket` by 100 to get the amounts the site displays.

## Counting shop dinosaurs on the Marketplace

Page through `/market/listings` (`page=1, 2, …` until `totalPages`) and count listings whose `dino.uniqueID` starts with `shop-`. The number after `shop-` is the Dino Shop offer id from `/shop/dinos`.

## Archive what you see

Before the operator changes anything, save copies with the Wayback Machine (<https://web.archive.org/save>) or take dated screenshots.
