# Verify it yourself

Most documented figures come from public pages and public API endpoints that anyone can open in a browser, without logging in. The exceptions are the rows marked "signed in" (their wording is also in the site's public JavaScript), the Discord row, which needs you to join the server, and figures from screenshots held by the author, which are labelled where they are used. Values may have changed since 27 October 2026.

## Pages (open normally)

| Page | What to look for |
|---|---|
| <https://main.dinoden.gg/faq> | "casino games", self-exclusion, Patreon AmberShard payouts, patron-only coin flip |
| Account settings on main.dinoden.gg (signed in) | the "Gambling Self-Exclusion" section |
| <https://main.dinoden.gg/subscriber> (signed in as a patron) | per-species online counts and caps, tier badges such as "APEX+", species unlocks ("Unlocks on [server] only" or "Respawns you as [dino]"; whether an unlock lets other players spawn as that species can be checked in-game) |
| <https://main.dinoden.gg/tos> | §1 age requirement, §2 virtual items and games, §3 Patreon |
| <https://main.dinoden.gg/privacy> | data collected, "intended for adults" |
| [Earlier Terms, archived 2 Apr 2026](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms) | §4 minors allowed with parental consent; §7 "Chance-Based Games" |
| <https://main.dinoden.gg/dinoden-client> | client claims (no injection, free) |
| <https://main.dinoden.gg/patreon> | tier prices in £, perks, and the Apex card showing both 3.5x and 4.5x |
| <https://main.dinoden.gg/games/jackpot> | rooms and limits; "How it works" (2.5% tax) |
| <https://find-and-update.company-information.service.gov.uk/company/16970676> | THE DINO DEN LTD company record |
| <https://www.patreon.com/TheDinoDen> | current tier prices and stated perks (compare with `/patreon/tiers`) |
| <https://graphtreon.com/creator/TheDinoDen> | paid-member history up to 28 Mar 2026, when the counts were made private |
| <https://thespoofingisle.com> | third-party player-count analysis (search "DINO DEN") |
| The Dino Den Discord (join through the site's Discord link) | public channels `#wall-of-shame` and `#sent-to-hell` |

These pages load their content with JavaScript, so use a normal browser.

## API endpoints (open in a browser tab; they return JSON)

| Endpoint | What it shows |
|---|---|
| <https://api.dinoden.gg/patreon/tiers> | Tier prices (`minCents` ÷ 100, shown on the site in £), AmberShards (`amberShardsBiWeekly` ÷ 100), ClawCoin multiplier (`clawcoinBoost`) |
| <https://api.dinoden.gg/shop/dinos> | Dino Shop prices (`priceNormal` ÷ 100 = AmberShards) and offer ids |
| <https://api.dinoden.gg/market/listings?page=1&limit=100&sort=newest> | Marketplace listings; look for `dino.uniqueID` values starting `shop-` |
| <https://api.dinoden.gg/features> | Which games are switched on |
| <https://api.dinoden.gg/raffle/current> | Raffle ticket rates (`wagerPerTicket` ÷ 100 = ClawCoins), prize pool, entrants |
| <https://api.dinoden.gg/games/crates> | Crate prices (÷ 100) and how often each was opened (`_count.openings`) |
| <https://api.dinoden.gg/platform-config> | Currency names, Patreon URL |
| <https://api.dinoden.gg/auctions> | Dinosaur auctions; look for `dino.uniqueID` values starting `shop-` |

## Units

The site stores currency amounts in hundredths. Divide `price`, `priceNormal`, `amberShardsBiWeekly`, `prizePool` and `wagerPerTicket` by 100 to get the amounts the site displays.

## Counting shop dinosaurs on the Marketplace

Page through `/market/listings` (`page=1, 2, …` until `totalPages`) and count listings whose `dino.uniqueID` starts with `shop-`. The number after `shop-` is the Dino Shop offer id from `/shop/dinos`.

## Archive what you see

Before the operator changes anything, save copies with the Wayback Machine (<https://web.archive.org/save>) or take dated screenshots.
