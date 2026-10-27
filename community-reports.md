# Community reports

These are **claims made by players** in public forums. Unless marked otherwise, none of them has been independently verified. They are included because several unconnected people describe the same problems over many months, and each is listed with its source and with the counterpoints raised at the time. Dates without a year in Steam threads are 2026.

Reports about how the owners and staff treat players are collected here too (see *Bans after criticism* and *Cheaters not dealt with; admins absent* below). New evidence is welcome through the [evidence form](../../issues/new/choose).

Most of the public discussion is on Steam's *The Isle* General Discussions forum. Reddit could not be accessed directly for this repository; the one Reddit post cited below is from a screenshot held by the author.

## Recurring complaints

### Patreon perks advertised but not delivered
- A former Dino Den trial admin wrote that listed benefits, including Rex access on lower tiers, priority queue and a dino-cap bypass, did not work. — [Steam thread, 9 Nov 2025, edited Jan 2026](https://steamcommunity.com/app/376210/discussions/14/669474588663616129/)
- A player who otherwise defended the server's admins called the Patreon *"kind of a scam"* (11 May 2026). — same thread, page 12
- **Counterpoint:** the thread author had his own dispute with the server (see below).

### Restricted dinosaurs unlocked by paying
- *"dinoden restrict the Rexs and big carnivore,"* with unrestricted play for monthly "apex" members (31 Mar 2026). — [Beware of pay to win servers](https://steamcommunity.com/app/376210/discussions/14/802343728582771226/)
- **Now partly documented:** the operator's own Discord announcement of 8 Dec 2025 advertised *"Unlock currently locked dinos"* and *"Apex Role access to Rex – Apex tier supporters can play Rex even when it's locked"* as Patreon perks ([DISCREPANCIES.md §11](DISCREPANCIES.md#11-patreon-perks-discord-announcement-vs-the-sites-patreon-page)). Whether this is still offered is not confirmed.
- Related documented fact: 37 shop-bought Tyrannosaurus were listed on the Marketplace on 27 Oct 2026 ([evidence/01](evidence/01-patreon-to-casino.md)).

### Cheaters not dealt with; admins absent
- Several players (Jul–Aug 2026) say cheaters return within days, admins are often offline during the day, and admins mainly moderate chat. — [Dino Den faking numbers and botting](https://steamcommunity.com/app/376210/discussions/14/573793348713953746/), [Honest Opinion thread](https://steamcommunity.com/app/376210/discussions/14/582804934666261638/), [Hackers on AU1 and AU2](https://steamcommunity.com/app/376210/discussions/14/581678695778932381/)
- **Counterpoint:** other players report hundreds of hours without admin problems, and cheating is a game-wide problem in *The Isle*, not unique to one server.

### Bans after criticism
- A player says they were banned after posting a critical review on Steam (8 Aug 2026). — [Honest Opinion thread](https://steamcommunity.com/app/376210/discussions/14/582804934666261638/)
- The former trial admin says they were removed from staff and muted after criticising senior staff. — [Steam thread](https://steamcommunity.com/app/376210/discussions/14/669474588663616129/)
- **Counterpoint:** other players say that admin was banned for streaming himself breaking rules (overpacking); one says they personally reported him. He disputes this and says he holds DMs showing otherwise, but did not publish them when asked repeatedly.

### Inflated player counts

**Status: supported by two independent technical analyses, a year apart. Not conclusive.**

The in-game server browser shows whatever player count each server reports to Epic Online Services (EOS), so a server can display more players than are really connected.

| Evidence | When | What it shows | Limits |
|---|---|---|---|
| EOS session check by Kadin, developer of the community [Isle Tools](https://thetoprat.github.io/Isletools-web/) | ~Nov 2025 | Queried the EOS sessions of "The Dino Den" and "NERF Official" and reported that most listed players were not real. Session ids were published so others could repeat the check. | Shared as a Discord post (screenshot held by the author; no public link available). The sessions have since expired, so it cannot be reproduced now. Nothing found indicates Kadin is Afterthought staff. |
| [TheSpoofingIsle](https://thespoofingisle.com/about), an automated tracker of every public server (read ~09:00 UTC, 27 Oct 2026; scores change over time) | Oct 2026 | Flags seven Dino Den servers: six "Spoofing" with scores of 73–83 (NA #1–#3 and EU #1–#3; see for example [NA #1](https://thespoofingisle.com/server/51.222.255.170%3A7777) and [EU #2](https://thespoofingisle.com/server/45.88.230.190%3A7777)) and AU #2 "Suspect" (60). It also flags [NERF NA](https://thespoofingisle.com/server/66.51.99.127%3A7778) "Spoofing" (73). Reasons given: counts that refill faster than clients can load after restarts, a curve that repeats every ~15 minutes, and join bursts of up to +173 players in 3 minutes. | Anonymous operator; it states a flag is "a starting point… not proof". Its restart check also fires on an official developer server ([Official US 1](https://thespoofingisle.com/server/172.237.147.22%3A31067)), and the 15-minute pattern appears on several unrelated large servers (e.g. [ORIGIN](https://thespoofingisle.com/server/216.39.241.102%3A7777)), so it does not single out Dino Den. |
| Player observations | Jun–Aug 2026 | Servers showing 450/450 with about ten players visible in game; counts full immediately after restarts. — [Steam thread](https://steamcommunity.com/app/376210/discussions/14/573793348713953746/) | Anecdotal. |
| Alleged admission by the owner on a livestream that they "stopped spoofing a long time ago" | ~2025 | Cited by both a Reddit post in r/theisle (~Nov 2025) and Kadin's Discord post (screenshots held by the author; no public links available). Dino Den's site lists its Twitch channel as `vireluxx` (<https://api.dinoden.gg/twitch/live>). | **Unconfirmed** — no recording or clip has been found. |
| Dino Den's own public data: raffle tickets (<https://api.dinoden.gg/raffle/current>) and the 24h playtime leaderboard (<https://api.dinoden.gg/leaderboard/playtime?scope=current>) | 27 Oct 2026 | Last week's 3,708,647 raffle tickets (10 per hour played, plus wagering) cap account-holders at roughly 2,200 online on average; the server-browser 24h averages across Dino Den servers summed to about 1,470. The top 100 players alone averaged 88 online. | Neither confirms nor rules out spoofing: tickets also come from wagering, the leaderboard only returns the top 100, and players without website accounts aren't counted. |

A NERF administrator is also said to have acknowledged false counts in the official *The Isle* Discord while denying responsibility (source: Kadin's Discord post, above). Those messages were reportedly deleted and cannot be checked.

### Link to the NERF server network
- Two forum posters say NERF is run by the same people as Dino Den (Apr and Aug 2026). — [Steam thread, page 11](https://steamcommunity.com/app/376210/discussions/14/669474588663616129/?ctp=11), [Honest Opinion thread](https://steamcommunity.com/app/376210/discussions/14/582804934666261638/)
- **Status:** unverified.

## Claims we do not repeat

Forum posts and screenshots circulating about Dino Den also include accusations of crimes (such as DDoS attacks on rival servers), allegations about individuals' private conduct, and alleged leaked messages. These are not reproduced here because **no evidence has been published for them**: no logs, no named target, no dates, no statement from a hosting provider or an affected server.

If you have verifiable evidence, [submit it here](../../issues/new/choose) (see also [CORRECTIONS.md](CORRECTIONS.md)). Evidence of a crime should go to the platform concerned or law enforcement, not to a public repository.
