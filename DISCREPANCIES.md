# Discrepancies, with sources

Every place where two sources disagree, side by side. Each item names both sources, when they were read, and what can and cannot be concluded. Unless stated otherwise, sources were read on **27 October 2026** without logging in; API values are preserved in [the snapshot](evidence/snapshots/2026-10-27/api-snapshot.json).

---

## 1. Apex ClawCoin boost: 3.5x or 4.5x?

| Source | Says |
|---|---|
| Apex tier **description** in the site's tier configuration — <https://api.dinoden.gg/patreon/tiers> (field `description`) | *"Maximum 3.5x Clawcoin boost"* |
| Apex tier **configured value**, same endpoint (field `clawcoinBoost`) | `4.5` |
| The site's own Patreon page — <https://main.dinoden.gg/patreon> (Apex card, read 27 Oct 2026) | shows both, on the same card: the description *"Maximum 3.5x Clawcoin boost"* and the perk line *"4.5x Clawcoin multiplier"* |
| Patreon tier page for [patreon.com/TheDinoDen](https://www.patreon.com/TheDinoDen), as captured in the author's screenshots for the 26 Oct 2026 report to Patreon, and re-checked by the author on 27 Oct 2026 | 3.5x |

**Can be concluded:** Dino Den states two different multipliers for the same tier: Patreon (where people pay) says 3.5x, while the website's Patreon page shows both 3.5x and 4.5x. The other four tiers' descriptions match their configured values (Sub "double" = 2, Adult "2.5x" = 2.5, Elder "triple" = 3).
**Cannot be concluded:** which multiplier members actually receive — earnings are calculated on Dino Den's servers. The configured value is *higher* than advertised, so if it is applied, members get more than promised. This is an inconsistency, not evidence of members being short-changed.

## 2. Patreon prices vs the site's tier minimums

| Source | Juvie | Sub | Adult | Elder | Apex |
|---|---|---|---|---|---|
| The site's Patreon page — <https://main.dinoden.gg/patreon> (from `minCents` at <https://api.dinoden.gg/patreon/tiers>; the site's code always adds a £ sign) | £12.00 / month | £22.00 | £33.00 | £44.00 | £55.00 |
| Site price converted at 1 GBP = 1.3313 USD ([rate on 27 Oct 2026](http://www.currency-converter.org.uk/currency-rates/convert/GBP-USD-rate.html?amount=1.00); calculated) | $15.98 | $29.29 | $43.93 | $58.58 | $73.22 |
| Patreon page viewed from the US, discounted price during a 40% promotion (author's screenshots, Oct 2026) | $10.50 | $18.90 | $28.50 | $37.80 | $47.40 |
| Patreon full price implied by the 40% discount (calculated) | $17.50 | $31.50 | $47.50 | $63.00 | $79.00 |
| Patreon full price vs converted site price | +9.5% | +7.5% | +8.1% | +7.5% | +7.9% |

The live Patreon page, fetched from the US on 27 Oct 2026, confirms the lowest tier: *"Access exclusive benefits starting at $17.50/month"* (<https://www.patreon.com/TheDinoDen>).

**Can be concluded:** the site lists tier prices in pounds, and Patreon charges US viewers 7.5–9.5% more than those prices converted at the market rate. The gap is similar for every tier, which suggests a single cause applied to all of them rather than prices set separately.
**Cannot be concluded:** the cause. It could be Patreon's own conversion rate or fees, tax, or prices set in dollars by the creator. The repository has no evidence for any one of these.

## 3. Age requirement changed

| Source | Says |
|---|---|
| Terms of Service, last updated 2026-01-20, archived 2 April 2026 — <https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms> (§4 Eligibility) | *"If you are a minor, you may use the Service only with the consent of a parent or legal guardian (where required by law)."* |
| Current Terms of Service, last updated 11 June 2026 — <https://main.dinoden.gg/tos> (§1) | *"You must be at least 18 years old to use the service."* |
| Current Privacy Policy, last updated 11 June 2026 — <https://main.dinoden.gg/privacy> | *"The service is intended for adults and not directed at anyone under 18."* |
| The author's sign-ins on two different Steam accounts (October 2026, and a separate account on 27 Oct 2026) | No age check or parental-consent step before reaching the games, shop and marketplace on either account |

**Can be concluded:** the operator moved from allowing minors (with consent) to adults-only in June 2026. The original site, na.dinoden.gg, is currently offline (error 521); the archived copy is the source.
**Cannot be concluded:** whether every new account sees the same sign-in flow. Both checks were made by the same person; confirmations from other players are welcome via the [evidence form](../../issues/new/choose).

## 4. "Not gambling" vs the operator's own descriptions

| Source | Says |
|---|---|
| Current Terms §2 — <https://main.dinoden.gg/tos> | games *"are played exclusively with virtual currency, are provided for entertainment only and are not gambling for money or anything of monetary value."* |
| Earlier Terms §7 "Chance-Based Games (Entertainment Only)" — [archived copy](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms) | *"Any chance-based features (including, without limitation, coin flips, jackpots, loot boxes, plinko, spins, raffles, or similar mechanics)…"* |
| FAQ — <https://main.dinoden.gg/faq> | *"A casino game crashed or did not pay out."*; *"You can also win (or lose...) ClawCoins in our casino games."*; *"Can I set gambling limits or exclude myself?"* |
| Account settings, shown to signed-in users (text from the site's JavaScript, read 27 Oct 2026; the setting calls the API endpoint `/me/gamble-block`) | section titled *"Gambling Self-Exclusion"*: *"Lock yourself out of all gambling games (Crash, Roll, Mines, Blackjack) for a fixed period."* When active: *"Gambling locked"* and *"You're locked out of gambling until"* a date |
| Patreon tiers, Dino Shop and Marketplace data — see [evidence/01](evidence/01-patreon-to-casino.md) | paid tiers supply the currencies that end up wagered |

**Can be concluded:** the operator itself describes the games as casino and chance-based games, and its own account settings call them *"gambling games"*, while its Terms say they are not gambling for anything of value.
**Cannot be concluded:** whether this meets any legal definition of gambling. That is for Patreon and regulators to judge. Also unclear: the self-exclusion text names four games (Crash, Roll, Mines, Blackjack) while the FAQ says it covers *"all casino games"*; whether it also blocks Coinflip, Jackpot and Crates could not be checked.

## 5. "Memberships are not purchases of Virtual Items"

| Source | Says |
|---|---|
| Current Terms §3 — <https://main.dinoden.gg/tos> | *"memberships are not purchases of Virtual Items"* |
| Tier configuration — <https://api.dinoden.gg/patreon/tiers> | each tier is defined by `amberShardsBiWeekly` (18,000–80,000 AmberShards every 14 days) |
| FAQ — <https://main.dinoden.gg/faq> | *"Active patrons receive their tier's AmberShards every 14 days… Tier upgrades grant the difference between the tiers immediately."* |

**Can be concluded:** the Terms say memberships are not purchases of Virtual Items, while every tier is defined by, and pays out, a fixed amount of AmberShards.
**Cannot be concluded:** how that wording would be treated by Patreon or a regulator.

## 6. Games menu vs games switched on

| Source | Says |
|---|---|
| Main navigation menu ("Games") — <https://main.dinoden.gg> (menu definition in the site's JavaScript, 27 Oct 2026) | Roll, Crash, Blackjack, Coinflip, **Jackpot** (*"One pot, one winner"*), Crates; Mines is defined but hidden while switched off. No poker entry |
| Games list in the site footer | Roll, Crash, Blackjack, Crates, Coinflip (no Jackpot) |
| Feature switches — <https://api.dinoden.gg/features> | `game.jackpot: true` and `game.poker: true`; `game.slots`, `game.viking`, `game.mines` false |
| Poker page — <https://main.dinoden.gg/games/poker> | titled *"Texas Hold'em — Provably Fair"*; the page's code sends any account below role level 40 back to the home page (guests are redirected). The author, signed in as an ordinary player, could not see it |
| Current Terms §2 — <https://main.dinoden.gg/tos> | games *"including crates, coinflip, crash, mines, blackjack, roll and similar"*: names mines (switched off), does not name jackpot or poker (switched on) |

**Can be concluded:** jackpot is live and open to ordinary players, including through the main menu (the page loads even without signing in), but it is missing from the footer list and from the games named in the Terms. Poker is built and switched on but limited to high-role accounts, which appear to be staff. Mines is named in the Terms but switched off.
**Cannot be concluded:** what role level 40 corresponds to, or whether poker will be opened to players.

## 7. Server-browser player counts vs measured behaviour

| Source | Says |
|---|---|
| In-game server browser (as recorded by trackers) | e.g. [NA #1] THE DINO DEN at 357/475 at 09:05 UTC on 27 Oct 2026 |
| [TheSpoofingIsle — NA #1](https://thespoofingisle.com/server/51.222.255.170%3A7777), [EU #2](https://thespoofingisle.com/server/45.88.230.190%3A7777) (read ~09:00 UTC, 27 Oct 2026) | "Spoofing" scores 75 and 83; join bursts up to +173 players in 3 minutes; refills faster than clients can load after restarts; ~15-minute repeating curve |
| Kadin's EOS session check (Discord post, ~Nov 2025; screenshot held by the author) | most listed players on "The Dino Den" and "NERF Official" were not real |

**Can be concluded:** two independent analyses, a year apart, flag Dino Den's displayed counts as inflated.
**Cannot be concluded:** that counts are definitely faked. The tracker's restart check also fires on an official developer server ([Official US 1](https://thespoofingisle.com/server/172.237.147.22%3A31067)), and the 15-minute pattern appears on unrelated servers (e.g. [ORIGIN](https://thespoofingisle.com/server/216.39.241.102%3A7777)). Dino Den's own public data (raffle tickets, playtime leaderboard) neither confirms nor rules out the displayed counts. Full detail, and a way to test it directly with Dino Den's own patron-only population page: [community-reports.md](community-reports.md#inflated-player-counts).

## 8. Privacy policy vs the DinoDen Client

| Source | Says |
|---|---|
| Privacy Policy — <https://main.dinoden.gg/privacy> | lists IP address, browser user agent, SteamID and gameplay data; no mention of the desktop client |
| DinoDen Client v0.2.0, static review ([evidence/04](evidence/04-client-analysis.md)) | sends the computer's hostname (`deviceName`) once at sign-in; uses the microphone for proximity voice |

**Can be concluded:** the policy does not describe data the client sends. This is a documentation gap, not evidence of misuse.
**Cannot be concluded:** how that data is stored or used on Dino Den's servers. The review covers version 0.2.0 only.

## 9. EU Digital Services Act: contact point and legal representative removed

| Source | Says |
|---|---|
| Terms of Service, last updated 2026-01-20 — [archived 2 Apr 2026](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms), §2 "EU Contact Point (DSA)" | *"If you are located in the European Union, you may contact us electronically via contact@dinoden.gg for matters related to the EU Digital Services Act (DSA). If we are legally required to appoint an EU legal representative, we will publish the representative's contact details in an easily accessible place on the Service."* |
| Same January Terms, §11 | *"Where reasonable, we may provide notice or an opportunity to appeal via our support channels."* |
| Current Terms of Service, last updated 11 June 2026 — <https://main.dinoden.gg/tos>, §12 Contact | *"Reach us through our Discord or in writing to"* a London postal address. No email address, no DSA section, no EU legal representative. |
| Current Terms §5 | *"Moderation decisions are made at our sole discretion and are final."*; accounts may be suspended *"with or without reason, and without prior notice"* |
| FAQ — <https://main.dinoden.gg/faq> ("Reports & Evidence", "Bans & Strikes") | Rule-breakers are reported by opening *"a rulebreak ticket on our Discord"* with *"Video links only"* as evidence; bans are appealed by opening *"an appeal ticket on our Discord"*, where *"we will tell you the exact reason and show the evidence where possible."* |
| The site's code and pages (searched 27 Oct 2026) | No mention of the DSA or an EU legal representative. No reporting option on the website itself or by email; reports and appeals go through Discord tickets, and nothing addresses reporting *illegal* content specifically |

**Relevant DSA provisions** (Regulation (EU) 2022/2065, [official text](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2065)):
- Art. 2(1): applies to intermediary services offered to recipients in the EU *"irrespective of where the providers… have their place of establishment"*; Art. 3(e) defines a *"substantial connection to the Union"* to include *"a significant number of recipients"* in a Member State or *"the targeting of activities towards one or more Member States."* Dino Den runs EU servers and hosts user content: its Terms §6 cover *"chat messages, names, profile content and uploads"*, and the Marketplace and player-made crates are user-created ([evidence/01](evidence/01-patreon-to-casino.md), [evidence/02](evidence/02-casino-games-and-raffle.md)).
- Art. 12(1): a single point of contact for users, *"by electronic means and in a user-friendly manner… which shall not solely rely on automated tools."*
- Art. 13(1): providers *"which do not have an establishment in the Union but which offer services in the Union shall designate, in writing"* a legal representative in a Member State.
- Art. 16(1): hosting providers must let anyone report illegal content *"exclusively by electronic means."*
- Art. 17(1): hosting providers must give *"a clear and specific statement of reasons"* to users for content removal or account suspension/termination.
- Art. 19(1): online-platform duties in Section 3 (including Art. 20 complaints, Art. 25 interface design and Art. 28 protection of minors), except Art. 24(3), do not apply to micro or small enterprises. Arts. 12, 13, 16 and 17 are not covered by that exemption.

**Can be concluded:** the operator's own January Terms acknowledged DSA duties (an EU contact point and a possible EU legal representative); the June Terms removed the DSA contact and email address and no representative is published.
**Cannot be concluded:** whether The Dino Den is legally required to meet these obligations, or whether its Discord ticket system satisfies them (Discord is an electronic channel, but it requires a Discord account). That is for regulators to decide. The company's size (relevant to the Art. 19 exemption) cannot be checked until its first accounts are filed (due October 2027, per [Companies House](https://find-and-update.company-information.service.gov.uk/company/16970676)). This is not legal advice.

## 10. UK Online Safety Act: 18+ rule with no age check; reporting and appeals

THE DINO DEN LTD is registered in England ([Companies House](https://find-and-update.company-information.service.gov.uk/company/16970676)).

| Source | Says |
|---|---|
| Current Terms §1 — <https://main.dinoden.gg/tos> | *"You must be at least 18 years old to use the service."* |
| Terms last updated 2026-01-20 — [archived copy](https://web.archive.org/web/20260402000811/https://na.dinoden.gg/terms), §4 | *"If you are a minor, you may use the Service only with the consent of a parent or legal guardian (where required by law)."* |
| The author's sign-ins to the website on two different Steam accounts (October 2026, and a separate account on 27 Oct 2026) | No age verification or age estimation step before reaching the games, shop and Marketplace on either account |
| Current Terms §5 | *"Moderation decisions are made at our sole discretion and are final."*; accounts may be suspended *"with or without reason, and without prior notice"* |
| Current Terms §12 | Contact through Discord or by post only |
| FAQ — <https://main.dinoden.gg/faq> ("Reports & Evidence", "Bans & Strikes") | Reports: *"Open a rulebreak ticket on our Discord"*, *"Video links only… no raw files, mp4 uploads, or screenshots."* Appeals: *"Open an appeal ticket on our Discord and we will tell you the exact reason and show the evidence where possible."* |
| The site's code and pages (searched 27 Oct 2026) | No reporting or complaints option on the website itself or by email; nothing addresses reporting *illegal* content specifically |
| User-generated content: Terms §6, Privacy Policy §1 (<https://main.dinoden.gg/privacy>), [evidence/01](evidence/01-patreon-to-casino.md), [evidence/02](evidence/02-casino-games-and-raffle.md) | *"chat messages, names, profile content and uploads"* (Terms §6); website global chat (FAQ); Marketplace listings; player-made crates |

**Relevant provisions of the Online Safety Act 2023:**
- [s.4](https://www.legislation.gov.uk/ukpga/2023/50/section/4): user-to-user services are regulated if they have *"links with the United Kingdom"*, which includes a significant number of UK users or the UK being *"one of the target markets for the service."*
- [s.20](https://www.legislation.gov.uk/ukpga/2023/50/section/20): services must have *"systems and processes that allow users and affected persons to easily report content"*, including illegal content.
- [s.21](https://www.legislation.gov.uk/ukpga/2023/50/section/21): services must have a complaints procedure that is *"easy to access, easy to use (including by children) and transparent"*, which covers users who are warned, suspended or banned. The Terms must set out how complaints are handled.
- [s.35(2)](https://www.legislation.gov.uk/ukpga/2023/50/section/35): a provider may conclude that children cannot access a service *only* if age verification or age estimation is used so that *"children are not normally able to access the service."* Ofcom's age assurance guidance (January 2025) says *"self-declaration of age… [is] not highly effective"* ([summary](https://www.lewissilkin.com/insights/2025/01/16/a-new-age-ofcom-publishes-final-version-of-age-assurance-guidance-102ju6k)).
- Ofcom deadlines ([source](https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/important-dates-for-online-safety-compliance)): illegal content risk assessments by 16 March 2025; children's access assessments by 16 April 2025; children's risk assessments, for services likely to be accessed by children, by 24 July 2025. Ofcom's page lists the illegal content risk assessment for all in-scope user-to-user services, with no size threshold.

**Can be concluded:** the Terms set an 18+ rule, but no age verification or estimation step was seen at sign-in. Under s.35(2), a rule in the Terms is not by itself enough to conclude that children cannot access a service. Until June 2026, the operator's own Terms allowed minors. Reports and ban appeals exist, but only as Discord tickets. The FAQ and the Terms also disagree: the FAQ says appeals will be told *"the exact reason"*, while the Terms say accounts may be suspended *"with or without reason"* and that decisions are *"final."*
**Cannot be concluded:** whether the Online Safety Act applies to The Dino Den, whether it complies, or whether a Discord-only ticket process meets s.20–21. Risk and access assessments do not have to be published, so their absence from the site proves nothing. Whether "a significant number of children" use the service is a question of evidence for Ofcom. Ofcom says it *"cannot respond to or investigate individual complaints"* but uses them to decide whether to act ([Ofcom](https://www.ofcom.org.uk/complaints/online-services-sites-apps/sites-and-apps/safety-measures)). This is not legal advice.

**UK gambling law, for completeness:** under the [Gambling Act 2005, s.6](https://www.legislation.gov.uk/ukpga/2005/19/section/6), a gaming prize must be *"money or money's worth."* The Gambling Commission treats virtual currency as money's worth when it *"can be exchanged for cash or traded for items of value"* ([Gambling Commission](https://www.gamblingcommission.gov.uk/licensees-and-businesses/guide/page/digital-and-virtual-currencies)). Dino Den has no cash-out, and its Terms ban real-money trading between players. Whether trading Patreon-funded dinosaurs for ClawCoins on the operator's own Marketplace counts as "traded for items of value" has not been decided by any authority found. Loot boxes are covered only by a voluntary 2023 industry code. Patreon's own Commerce Guidelines, which cover gambling for an exchange of value including digital currencies (see [README](README.md#why-it-matters)), are broader than UK law.

## 11. Patreon perks: Discord announcement vs the site's Patreon page

| Source | Says |
|---|---|
| Announcement posted by the operator's Discord app in `#support-the-server`, 8 December 2025 ([screenshot](evidence/screenshots/2025-12-08-discord-support-the-server.png), cropped to the announcement; time shown in the author's time zone) | *"Support the server on Patreon and unlock powerful perks that give you the edge in the wild!"* Perks include *"Queue skip – join instantly even when full"*, *"Bi-weekly Amber Shards – use them to instantly purchase full-grown dinos!"*, *"Unlock currently locked dinos"*, and *"Apex Role access to Rex – Apex tier supporters can play Rex even when it's locked"*. Tiers bring *"greater power on the island. Choose your path to dominance."* |
| The site's Patreon page — <https://main.dinoden.gg/patreon> (27 Oct 2026) | Each tier lists only AmberShards every 2 weeks, a ClawCoin multiplier and *"Unlimited Dino parking"*. No queue skip, locked-dino or Rex access listed |
| Patreon creator page — <https://www.patreon.com/TheDinoDen> (fetched 27 Oct 2026) | *"From Amber Shards every 2 weeks, to queue skip, to VIP-only access and event invites."* |
| Player reports — [community-reports.md](community-reports.md#restricted-dinosaurs-unlocked-by-paying) | Rex and big carnivores restricted, with unrestricted play for Apex members (Mar 2026); a former trial admin says Rex access on lower tiers and a *"dino-cap bypass"* did not work (Nov 2025) |
| *The Isle* patch 0.21.321, 28 December 2025 — [official news post](https://www.theisle-game.com/en/news/merry-x-mas-and-a-happy-new-patch-0-21-321) | adds the Tyrannosaurus as a playable dinosaur, three weeks after the announcement |
| The author's own observation (October 2026) | Dino Den limits how many Rexes can be on its low-rules servers at once; when the limit is reached, Rex is "locked" for other players |
| Dino Den's public website chat, 27 Oct 2026 (visible without signing in; players not named) | players saying Rex "stays locked" and asking for someone to "open rex" on EU 2 |
| The site's patron-only "Patreon Access" page — <https://main.dinoden.gg/subscriber> (text from the site's JavaScript, read 27 Oct 2026) | *"Live server population, species unlocks and the skin designer for patrons."* Each species shows *"Online"* as a count out of a per-server cap, and can carry a minimum tier badge (*"[tier]+"*, tooltip *"Requires [tier] or higher"*). Patrons can unlock a species on a server: *"[dino] unlocked on [server]"*, *"Playable for [time]"*, *"On cooldown for this server"*. *"Glitch skins are reserved for the APEX tier."* |
| Screenshot of that page from a Patreon supporter (received 27 Oct 2026; held by the author; taken between 28 Sep and 27 Oct 2026, as the Halloween event banner is showing) | AU #2: Tyrannosaurus marked *"APEX+"*, 15 of 16 online, *"Playable"*; Deinosuchus 5 of 80 |
| Reply by a Dino Den Senior Admin in the Dino Den Discord, 9 Oct 2026 ([screenshot](evidence/screenshots/2026-10-09-discord-senior-admin-apex-unlock.png), the player's name hidden; the staff member's Discord profile lists the roles Senior Admin, Admin, TDD Staff and Ticket Support) | replying to a player's message (shown truncated as *"how do we unlock the allow…"*): *"Allos and rexes can be unlock if you are APEX patreon, otherwise its popcontrol on them"* |

**Can be concluded:** in December 2025 the operator itself advertised paid access to dinosaurs that are otherwise locked, including Rex for the Apex tier, and described AmberShards as a way to *"instantly purchase full-grown dinos."* The current Patreon page on the website does not list the access perks, while Patreon itself still advertises queue skip and *"VIP-only access."*
"Locked" refers to Dino Den's own per-server species caps, not to the game. The perk is still offered: the site's patron-only page lets patrons unlock species on a server for a limited time, in a patron's screenshot from October 2026 Tyrannosaurus is marked as needing the Apex tier, and on 9 October 2026 a Senior Admin stated that Allosaurus and Tyrannosaurus *"can be unlock if you are APEX patreon, otherwise its popcontrol on them."*
**Cannot be concluded:** exactly how the unlock interacts with the cap (that logic runs on Dino Den's servers), the current unlock length and cooldown (shown only to patrons), or whether the perks always worked as advertised.

---

## Checked, no discrepancy found

| Claim by Dino Den | Source | Result |
|---|---|---|
| The client *"does not inject anything into The Isle, does not read game memory and does not modify game files"* — <https://main.dinoden.gg/dinoden-client> | Static review of v0.2.0 ([evidence/04](evidence/04-client-analysis.md)) | No such code found |
| Client is *"Free for every Dino Den player"* | `client.patreonOnly: false` at <https://api.dinoden.gg/features> | Consistent |
| *"the only real-money support is our Patreon"* (FAQ) | Site code and API | No other real-money store found |
