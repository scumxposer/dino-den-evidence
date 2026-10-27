# The Dino Den: Patreon money, casino games and staff conduct

A sourced, one-stop record of how **The Dino Den** — a large unofficial server network for *The Isle: Evrima*, operated by THE DINO DEN LTD (Company No. 16970676, England) — links paid Patreon memberships to casino-style games on its website, and of how its owners and staff treat players. It collects evidence of abuse of moderation powers, harassment of players and retaliation for criticism, held to the same standards as everything else here.

Everything in the **Documented** sections comes from the operator's own public website, API, FAQ and Terms of Service, captured on **27 October 2026**, plus a small number of the author's own observations (sign-in checks, Patreon page screenshots and a Discord screenshot), which are labelled as such wherever they are used. Anyone can re-check the public sources (see [verify-yourself.md](verify-yourself.md)). Player complaints, including reports about staff conduct, are kept separately, labelled as claims, with their sources and counterpoints.

> This repository is not affiliated with The Dino Den, Afterthought LLC (developer of *The Isle*), or Patreon. It is not legal advice. Corrections and responses from The Dino Den are welcome — see [CORRECTIONS.md](CORRECTIONS.md).

## Have evidence? Submit it

If you have something that supports, disproves or adds to anything here, **[open an issue](../../issues/new/choose)** — new evidence, corrections and counter-evidence are all welcome. This includes evidence of how the owners or staff have treated you or others: bans, mutes or wipes without reason, retaliation for criticism, harassment, or misuse of admin powers.

**Most useful:** original, uncropped screenshots that show the date and time; video clips with timestamps; links to public posts, pages or archived copies; ban or mute notices; anything someone else can check for themselves. For staff conduct, show the full context, not only the reply.

**Please don't submit:** real names, addresses, Steam profiles, alleged alt accounts, or private messages between other people. Messages a staff member or owner sent *to you* while acting as staff are accepted; ordinary players' names will be hidden before anything is published. Submissions are added only if they can be checked, and each is labelled by how well it is supported. Please don't harass the owners, staff or players. Details: [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## The short version

This repository covers two subjects: **the money** (how Patreon payments end up wagered in casino-style games) and **how the owners and staff treat players** (see [Staff and owner conduct](#staff-and-owner-conduct) below).

On the money side, Patreon money reaches The Dino Den's casino games through a loop that runs entirely on the operator's own site:

```
Patreon pledge (5 tiers, £12–£55 a month as shown on the site)
  └─► AmberShards (18,000–80,000 every 14 days)
        └─► Dino Shop: dinosaurs for 1,000–7,000 AmberShards each
              └─► Marketplace and Auctions: dinosaurs resold to other players for ClawCoins
                    └─► ClawCoins wagered on roll, crash, blackjack, coinflip, jackpot and crates
                          (jackpot: players' bets go into one pot, one player wins it, the site keeps 2.5%)
                          └─► every 100,000 ClawCoins wagered = 1 entry in a weekly 100,000,000-ClawCoin raffle

Patreon pledge ──(1.5x–4.5x ClawCoin earning multiplier as configured; Apex described as 3.5x)──► ClawCoins   (a second, direct route)
```

On 27 October 2026, **117 of 877 active Marketplace listings** were dinosaurs whose IDs match Dino Shop purchases (interpretation explained in [evidence/01](evidence/01-patreon-to-casino.md)), listed for sale in ClawCoins — 37 of them Tyrannosaurus.

## Staff and owner conduct

What is documented so far comes from the operator's own rules:

- The current Terms (§5) let staff suspend or terminate accounts *"with or without reason, and without prior notice or compensation"*, and say *"Moderation decisions are made at our sole discretion and are final."* Enforcement *"may extend across the website, our game servers, and connected community spaces such as our Discord."*
- The FAQ tells banned players to *"Open an appeal ticket on our Discord and we will tell you the exact reason and show the evidence where possible."* Reports and appeals go through Discord tickets only.
- The January 2026 Terms said only: *"Where reasonable, we may provide notice or an opportunity to appeal via our support channels."*

Players have reported bans after posting critical reviews, a trial admin removed and muted after criticising senior staff (disputed by other players), and cheaters not being dealt with. These are **unverified claims**, listed with counterpoints in [community-reports.md](community-reports.md). No verified evidence about an individual owner's or staff member's conduct has been published here yet. If you have some, [submit it](../../issues/new/choose) following [CONTRIBUTING.md](CONTRIBUTING.md#evidence-about-owner-and-staff-conduct).

## Key findings

Every place where two sources disagree is listed side by side, with links, in **[DISCREPANCIES.md](DISCREPANCIES.md)**.

| Finding | Status | Detail |
|---|---|---|
| Patreon tiers pay out AmberShards, which buy dinosaurs | **Documented** | [evidence/01](evidence/01-patreon-to-casino.md) |
| Shop-bought dinosaurs are listed for ClawCoins on the Marketplace | **Documented** (ID format interpretation explained) | [evidence/01](evidence/01-patreon-to-casino.md) |
| ClawCoins are wagered on casino-style games the operator itself calls "casino games" | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Weekly raffle gives more entries the more a player wagers | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Outage compensation can be gambled on a double-or-nothing coin flip; only active patrons can claim it | **Documented** (operator's FAQ) | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Apex ClawCoin boost stated inconsistently: Patreon says 3.5x; the site's own Patreon page shows "Maximum 3.5x" and "4.5x" on the same tier card (in members' favour; rate actually applied can't be verified) | **Documented inconsistency** | [DISCREPANCIES.md §1](DISCREPANCIES.md#1-apex-clawcoin-boost-35x-or-45x) |
| Patreon charges US viewers 7.5–9.5% more than the site's £ tier prices converted at the market rate | **Documented** (cause unknown) | [DISCREPANCIES.md §2](DISCREPANCIES.md#2-patreon-prices-vs-the-sites-tier-minimums) |
| Age rule changed from "minors with parental consent" (Jan 2026 Terms) to 18+ (June 2026 Terms) | **Documented** | [DISCREPANCIES.md §3](DISCREPANCIES.md#3-age-requirement-changed) |
| EU Digital Services Act contact point and legal-representative wording removed from the Terms in June 2026; none published | **Documented** (whether DSA duties apply is for regulators) | [DISCREPANCIES.md §9](DISCREPANCIES.md#9-eu-digital-services-act-contact-point-and-legal-representative-removed) |
| Terms require 18+, but no age verification at sign-in; reports and ban appeals go through Discord tickets only, and the Terms call moderation decisions "final" (relevant to the UK Online Safety Act) | **Documented** (whether the Act applies is for Ofcom) | [DISCREPANCIES.md §10](DISCREPANCIES.md#10-uk-online-safety-act-18-rule-with-no-age-check-reporting-and-appeals) |
| Player-vs-player jackpot with rooms up to 25,000,000 ClawCoins a round; the site takes 2.5% of each pot | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md#jackpot) |
| Poker (Texas Hold'em) is built and switched on but limited to high-role (apparently staff) accounts | **Documented** (site code) | [DISCREPANCIES.md §6](DISCREPANCIES.md#6-games-menu-vs-games-switched-on) |
| Dec 2025 Discord announcement advertised patron access to locked dinosaurs, Apex access to Rex "even when it's locked", queue skip, and AmberShards to "instantly purchase full-grown dinos" | **Documented** (operator's Discord; screenshot) | [DISCREPANCIES.md §11](DISCREPANCIES.md#11-patreon-perks-discord-announcement-vs-the-sites-patreon-page) |
| Terms say the games are "not gambling for money or anything of monetary value" | **Documented** (their position) | [evidence/03](evidence/03-operator-statements.md) |
| Server-browser player counts inflated on Dino Den (and NERF) servers | **Supported** by two independent technical analyses (late 2025, Oct 2026); not conclusive | [community-reports.md](community-reports.md#inflated-player-counts) |
| DinoDen Client reads game memory or injects code | **Not supported** — static analysis found no such code | [evidence/04](evidence/04-client-analysis.md) |
| Terms let staff suspend accounts "with or without reason" and call moderation decisions "final", while the FAQ promises appeals "the exact reason" | **Documented** | [DISCREPANCIES.md §10](DISCREPANCIES.md#10-uk-online-safety-act-18-rule-with-no-age-check-reporting-and-appeals) |
| Staff conduct: bans after critical reviews, a trial admin removed and muted after criticising senior staff, cheaters not dealt with and admins absent | **Player claims**, several independent sources, unverified and partly disputed (evidence wanted) | [community-reports.md](community-reports.md#bans-after-criticism) |
| Patreon perks advertised but not delivered | **Player claims**, unverified | [community-reports.md](community-reports.md#patreon-perks-advertised-but-not-delivered) |

## Why it matters

Patreon's [Commerce Guidelines](https://patreon.com/policy/benefits) (§5, "Gambling, Raffles, and Sweepstakes") say: *"Fans and creators may not use Patreon to access, provide, or facilitate gambling for money or an exchange of value, including digital currencies."* They list *"raffles, casinos and casino games"* among gambling activities. A report has been filed with Patreon Trust & Safety — see [reports-filed.md](reports-filed.md).

The Dino Den's Terms of Service also require users to be 18 or older, but no age check was seen at sign-in ([DISCREPANCIES.md §3](DISCREPANCIES.md#3-age-requirement-changed)).

How staff use their powers matters for the same players: dinosaurs, currency and Patreon-funded items all sit on accounts that the Terms let the operator suspend *"with or without reason"*, and the Terms also allow staff to *"remove Virtual Items"*, with decisions described as *"final."*

## What this repository deliberately does not include

- Accusations of crimes (for example, DDoS attacks on rival servers). Rumours of this circulate on forums, but no evidence, target or date has been published. See [community-reports.md](community-reports.md#claims-we-do-not-repeat).
- Real names, Steam profile links, alleged alt accounts, or private messages between other people.
- Ordinary players' names, or their Discord or private messages. Public forum posts are quoted without usernames and linked to their source; people who published their own analyses are credited by the name they published under.
- Anything about owners' or staff members' private lives or real identities. They are referred to only by the names they use as staff, and only for what they did in that role. (Official announcements posted by the operator's own Discord app are included, cropped to the announcement.)
- The Dino Den's software or other copyrighted material — only findings about it.

## Contents

- [DISCREPANCIES.md](DISCREPANCIES.md) — every discrepancy, with both sources side by side
- [evidence/01-patreon-to-casino.md](evidence/01-patreon-to-casino.md) — the value chain, Patreon tiers, Dino Shop, Marketplace
- [evidence/02-casino-games-and-raffle.md](evidence/02-casino-games-and-raffle.md) — games, raffle, crates, patron-only coin flip
- [evidence/03-operator-statements.md](evidence/03-operator-statements.md) — FAQ and Terms of Service, and where they conflict with the evidence
- [evidence/04-client-analysis.md](evidence/04-client-analysis.md) — what the DinoDen Client does and does not do
- [evidence/snapshots/2026-10-27/api-snapshot.json](evidence/snapshots/2026-10-27/api-snapshot.json) — the raw data behind the figures, personal data removed
- [community-reports.md](community-reports.md) — player complaints, including reports about staff conduct, with sources and counterpoints
- [reports-filed.md](reports-filed.md) — reports made to platforms
- [verify-yourself.md](verify-yourself.md) — how to check every figure
- [CORRECTIONS.md](CORRECTIONS.md) — corrections policy and right of reply
- [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — how to submit evidence, and the rules
- [MAINTAINING.md](MAINTAINING.md) — the standard procedure every change follows, and `tools/check.py`

## License

The text, analysis and data compilations in this repository are licensed under [CC BY 4.0](LICENSE). You may share and adapt them, including commercially, as long as you give credit and link back, for example: *"The Dino Den evidence repository, https://github.com/scumxposer/dino-den-evidence"*. Linking back also lets readers find the latest corrections.

**Not covered by this license:** material owned by others and quoted or reproduced here for reporting and criticism. That includes text, data and images from The Dino Den's website, Terms, FAQ, API and Discord (including the screenshot in `evidence/screenshots/`), and quotes from Patreon, Steam forum posts, regulators and legislation. Those remain the property of their owners.

*Last updated: 27 October 2026.*
