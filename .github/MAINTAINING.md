# Maintaining this repository: standard procedure

This procedure applies to **every** change, whoever makes it: the owner, a contributor, or an automated task. The repository is a public record about a real company and real people. It is only useful if every file agrees with every other file and every claim can be traced to its source. Skipping a step is how contradictions creep in.

## 1. Before changing anything

- Read the file you are changing **in full**, and every other file that covers the same topic (see the topic map below).
- Write down the source for each claim you are about to add or change.

## 2. Verify against the source, now

- **Re-open the original source in this session.** Do not rely on memory, an earlier summary, a previous run, or the repository's own text.
- **Quotes are word for word.** Mark omissions with "…". Record the date (and UTC time for figures that change).
- **Units and currencies:** the API stores amounts in hundredths. The site shows Patreon tier prices in pounds (£); Patreon shows US viewers dollars.
- **Claims that something does not exist** (no menu entry, no process, no perk, not reachable) are the easiest to get wrong. Before writing one, check every place it could appear: the page itself, the site's main navigation menu (defined in the site's JavaScript; the visible menu may be collapsed), the footer, the FAQ, the Terms, the Privacy Policy and the site's route list.
- **Label everything** with how well it is supported: **Documented** (the operator's own pages, data, terms or official announcements, or evidence anyone can check directly), **Supported** (independent technical evidence, not conclusive), **Player claims** (unverified, with counterpoints), **Unconfirmed**, or **Not supported**. Label the owner's own observations as such.
- **Scope:** only add what is relevant to the two subjects: (1) Patreon money, the currencies and the casino-style games, including the operator's statements and terms and player counts; (2) how the owners and staff treat players.
- **Personal information:** follow [CONTRIBUTING.md](../CONTRIBUTING.md). Owners and staff are named by the handles they use as staff, with their role, only for what they did in that role. Hide every player's username and avatar in quotes and screenshots, and check the image after redacting. No private messages between other people, no accusations of crimes without published evidence.
- If you cannot verify something, **do not add it**. Note it as "needs checking" instead.

## 3. Make the change everywhere

Search the whole repository for the topic (for example `grep -rn "jackpot" .`) and update **every** passage, not just the one you started with. Use the topic map:

| Topic | Where it appears |
|---|---|
| Patreon tiers, prices, perks, multiplier, the AmberShard → ClawCoin route | README (short version, key findings, why it matters), DISCREPANCIES §1, §2, §4, §5, §10 (UK gambling law), §11, evidence/01, evidence/03, community-reports, verify-yourself, reports-filed |
| Games, jackpot, poker, raffle, crates, Lucky Bags, gambling wording | README (short version, key findings), DISCREPANCIES §4, §6, evidence/02, evidence/03, verify-yourself |
| Terms, FAQ, age rule, moderation and appeals | README (staff section, key findings, why it matters), DISCREPANCIES §3, §5, §9, §10, §12, evidence/03, evidence/05 |
| Staff and owner conduct | README (staff section, key findings), DISCREPANCIES §12, evidence/05, community-reports, CONTRIBUTING, CODE_OF_CONDUCT, evidence/03 |
| Player counts | README (key findings), DISCREPANCIES §7, community-reports |
| Client app | README (key findings), DISCREPANCIES §8, evidence/04 |
| Submission and privacy rules | README (submit section, "does not include"), CONTRIBUTING, CODE_OF_CONDUCT, CORRECTIONS (policy), .github/ISSUE_TEMPLATE/evidence.yml, this file (.github/MAINTAINING.md) |

Also:
- Re-read anything marked "cannot be concluded", "not re-tested", "unconfirmed" or "not confirmed" that the new finding affects, and update it.
- Do not rename existing section headings: links from outside the repository depend on them. Add new sections instead.

## 4. Check

From the repository root, run `python3 tools/check.py`. It must print `OK` before anything is committed. It checks:

- **Links and tables:** every internal link and anchor exists; every table row has the right number of columns.
- **Sentences:** broken sentences left by edits (a lowercase word after a full stop, doubled words, unbalanced quotes, brackets or italics, stray punctuation).
- **Facts:** figures that appear in more than one file match `tools/facts.json`. When a figure changes, change it in every file and in `facts.json` together. When a new figure appears in two or more files, add it to `facts.json`.
- **Dates:** the README's "Last updated" matches the latest entry in CORRECTIONS.md.
- **Wording review:** every line with high-risk wording must have a recorded review. The categories are: certainty ("confirmed", "proves"), automatic routes ("ends up", "converts", "Patreon-funded"), absolutes ("always", "only", "every"), motives ("mocking", "deliberately", "rigged"), generalisations ("often", "pattern"), staleness ("still", "currently", "so far"), and a player claim inside a **Documented** row. Direct quotes are skipped because they are checked word for word against the source. Editing a line cancels its review, so a changed line is always looked at again.

How to clear a wording flag:
1. Re-open the source for that line.
2. Ask whether the line says more than the source supports: more certain, more general, automatic rather than possible, a motive rather than an action, out of date, or a player claim labelled as documented. If it does, fix the line.
3. Address **every** flagged word, not just the first one: a line flagged for "now" and "still" needs both checked.
4. For actions ("lifted", "banned", "refused"), check that the source shows the action happened, not only a promise or a claim of it.
5. Only if the line is accurate, record it: `python3 tools/check.py --ack FILE:LINE "the source and why the wording is accurate"`. Never record reviews in bulk or with rule-matched notes: read each line and write its own reason, naming the source.

Then re-read the README from top to bottom as a first-time reader. The summary, the findings table and the detail files must say the same thing.

## 5. Log and commit

- Add a row to the log in [CORRECTIONS.md](../CORRECTIONS.md) describing the change. If an earlier version was wrong, say so plainly and say what was wrong.
- Commit messages describe the change and end with a `Co-Authored-By:` line where applicable. Never include chat or session links.

## 6. Anything that leaves the repository

Reddit posts and replies, YouTube or Steam comments, and emails to platforms repeat claims from the repository. They are held to the same standard:

- Every factual claim in a draft must match a line in the repository, with the same strength. If the repository says "can", the draft cannot say "does".
- Run each draft through the same questions as the wording review: certainty, automatic routes, absolutes, motives, generalisations, staleness, and player claims stated as fact.
- **After every correction**, search for the old wording and its synonyms in:
  - the repository;
  - any drafts not yet posted;
  - what has already been sent or posted.

  `reports-filed.md` records what was sent to platforms, so check the sent emails against the corrected repository and list any statements that have since changed. Tell the owner which posted text needs editing.

## 7. Full review

A request for a full review means every step below, in order. Report what was done, with the numbers, not just "reviewed".

1. `git pull`, then run `python3 tools/check.py`. Fix everything it reports, including every wording flag (section 4).
2. Read every file in full, top to bottom: README, DISCREPANCIES, evidence/01–05, community-reports, verify-yourself, reports-filed, CONTRIBUTING, CODE_OF_CONDUCT, CORRECTIONS (policy and the last ten log rows), this file and the issue templates. Count them.
3. For each row of the README's key findings table, open the file it links to and check that the finding, its status label and its wording match the detail.
4. Re-open the live sources for anything time-sensitive (FAQ, Terms, tier configuration, Patreon page) and compare them with the repository.
5. Read it as a hostile critic would, and as a fair one: for each finding about the operator or staff, is there an innocent explanation or common practice the reader should know (a counterpoint)? Is anything said by the operator that cuts the other way left out? For each claim, what would someone defending The Dino Den say is overstated or missing? Fix anything they would be right about.
6. Check everything outside the repository (section 6): the sent emails in reports-filed and any drafts.
7. Log the review in CORRECTIONS.md with what was checked and what was found. Say plainly if an earlier review missed something.

## 8. Publish

- Automated tasks push only to a review branch named `updates/YYYY-MM-DD`. The owner reviews and merges it.
- Never force-push to main and never delete branches.

## Mistakes this procedure exists to prevent

These all happened once and were corrected (see the log in CORRECTIONS.md):

- Saying no reporting or appeal process existed when the FAQ describes one.
- Saying jackpot was missing from the menu when the main menu lists it.
- Giving prices in dollars when the site shows pounds.
- Leaving "not re-tested" in place after a re-test.
- A table row broken by an edit.
- Privacy rules worded differently in different files.
- Attributing forum comments to Dino Den when, in a thread covering several servers, they were about another server.
- Paraphrases drifting from the source ("a critical review" for a forum post; "two posters" for one). Quote the source where possible and re-read it before summarising.
- A detail added without any source (who developed a community tool).
- Describing a possible route as automatic (AmberShards only become ClawCoins if a player chooses to sell), or calling items "Patreon-funded" when their source can't be known.
- Putting a player-reported effect under a **Documented** label (who benefits from a patron's species unlock).
- Present-tense or "still" statements left undated ("currently offline", "so far", "still advertises").
- A broken sentence left by a scripted edit (". and some species").
- Reddit drafts and a sent email repeating wording the repository had already corrected.
- Calling reviews "thorough" when they were only searches for the phrase just fixed. Section 7 exists because of this.
- Recording wording reviews with rule-matched notes, which let an undated "still offered" through on a line whose note only covered "now".
- Reporting a promise as an action: "lifted a permanent ban" when the owner only wrote "Dw i will unban you".
- Leaving out a fair counterpoint: ban-trap channels are a common anti-spam tool, and ClawCoins cannot be cashed out.
- Giving a share without data ("most AmberShards come from Patreon") when another source (Twitch rewards, 32M paid out) was never compared.
