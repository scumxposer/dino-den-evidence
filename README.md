# The Dino Den: Patreon money, virtual currency and casino games

A sourced, one-stop record of how **The Dino Den** — a large unofficial server network for *The Isle: Evrima*, operated by THE DINO DEN LTD (Company No. 16970676, England) — links paid Patreon memberships to casino-style games on its website.

Everything in the **Documented** sections comes from the operator's own public website, API, FAQ and Terms of Service, captured on **27 October 2026**. Anyone can re-check it (see [verify-yourself.md](verify-yourself.md)). Player complaints are kept separately, labelled as claims, with their sources and counterpoints.

> This repository is not affiliated with The Dino Den, Afterthought LLC (developer of *The Isle*), or Patreon. It is not legal advice. Corrections and responses from The Dino Den are welcome — see [CORRECTIONS.md](CORRECTIONS.md).

## The short version

Patreon money reaches The Dino Den's casino games through a loop that runs entirely on the operator's own site:

```
Patreon pledge ($12–$55 per tier)
  └─► AmberShards (18,000–80,000 every 14 days)
        └─► Dino Shop: dinosaurs for 1,000–7,000 AmberShards each
              └─► Marketplace: dinosaurs resold to other players for ClawCoins
                    └─► ClawCoins wagered on crash, roll, blackjack, coinflip, jackpot, poker and crates
                          └─► every 100,000 ClawCoins wagered = 1 entry in a weekly 100,000,000-ClawCoin raffle

Patreon pledge ──(1.5x–4.5x ClawCoin earning multiplier)──► ClawCoins   (a second, direct route)
```

On 27 October 2026, **117 of 877 active Marketplace listings** were dinosaurs carrying Dino Shop purchase IDs, listed for sale in ClawCoins — 37 of them Tyrannosaurus.

## Key findings

Every place where two sources disagree is listed side by side, with links, in **[DISCREPANCIES.md](DISCREPANCIES.md)**.

| Finding | Status | Detail |
|---|---|---|
| Patreon tiers pay out AmberShards, which buy dinosaurs | **Documented** | [evidence/01](evidence/01-patreon-to-casino.md) |
| Shop-bought dinosaurs are listed for ClawCoins on the Marketplace | **Documented** (ID format interpretation explained) | [evidence/01](evidence/01-patreon-to-casino.md) |
| ClawCoins are wagered on casino-style games the operator itself calls "casino games" | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Weekly raffle gives more entries the more a player wagers | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Double-or-nothing coin flip available only to active patrons | **Documented** (operator's FAQ) | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Apex ClawCoin boost stated inconsistently: 3.5x in the tier description and on Patreon, 4.5x in the site's configuration (in members' favour; rate actually applied can't be verified) | **Documented inconsistency** | [DISCREPANCIES.md §1](DISCREPANCIES.md#1-apex-clawcoin-boost-35x-or-45x) |
| Age rule changed from "minors with parental consent" (Jan 2026 Terms) to 18+ (June 2026 Terms) | **Documented** | [DISCREPANCIES.md §3](DISCREPANCIES.md#3-age-requirement-changed) |
| Jackpot and poker switched on but not shown in the Games menu | **Documented** | [evidence/02](evidence/02-casino-games-and-raffle.md) |
| Terms say the games are "not gambling for money or anything of monetary value" | **Documented** (their position) | [evidence/03](evidence/03-operator-statements.md) |
| Server-browser player counts inflated on Dino Den (and NERF) servers | **Supported** by two independent technical analyses (late 2025, Oct 2026); not conclusive | [community-reports.md](community-reports.md#inflated-player-counts) |
| DinoDen Client reads game memory or injects code | **Not supported** — static analysis found no such code | [evidence/04](evidence/04-client-analysis.md) |
| Patreon perks advertised but not delivered; paid-only access to restricted dinosaurs; weak anti-cheat moderation; bans after criticism | **Player claims**, several independent sources, unverified | [community-reports.md](community-reports.md) |

## Why it matters

Patreon's Commerce Guidelines ("Gambling, Raffles, and Sweepstakes") say creators may not use Patreon to access, provide or facilitate gambling for money or an exchange of value, including digital currencies. A report has been filed with Patreon Trust & Safety — see [reports-filed.md](reports-filed.md).

The Dino Den's Terms of Service also require users to be 18 or older.

## What this repository deliberately does not include

- Accusations of crimes (for example, DDoS attacks on rival servers). Rumours of this circulate on forums, but no evidence, target or date has been published. See [community-reports.md](community-reports.md#claims-we-do-not-repeat).
- Real names, Steam profile links, alleged alt accounts, or anyone's private messages.
- Screenshots of individuals' Discord messages.
- The Dino Den's software or other copyrighted material — only findings about it.

## Contents

- [DISCREPANCIES.md](DISCREPANCIES.md) — every discrepancy, with both sources side by side
- [evidence/01-patreon-to-casino.md](evidence/01-patreon-to-casino.md) — the value chain, Patreon tiers, Dino Shop, Marketplace
- [evidence/02-casino-games-and-raffle.md](evidence/02-casino-games-and-raffle.md) — games, raffle, crates, patron-only coin flip
- [evidence/03-operator-statements.md](evidence/03-operator-statements.md) — FAQ and Terms of Service, and where they conflict with the evidence
- [evidence/04-client-analysis.md](evidence/04-client-analysis.md) — what the DinoDen Client does and does not do
- [evidence/snapshots/2026-10-27/api-snapshot.json](evidence/snapshots/2026-10-27/api-snapshot.json) — the raw data behind the figures, personal data removed
- [community-reports.md](community-reports.md) — player complaints, sources and counterpoints
- [reports-filed.md](reports-filed.md) — reports made to platforms
- [verify-yourself.md](verify-yourself.md) — how to check every figure
- [CORRECTIONS.md](CORRECTIONS.md) — corrections policy and right of reply

*Last updated: 27 October 2026.*
