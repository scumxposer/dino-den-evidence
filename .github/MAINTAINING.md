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
- **Personal information:** follow [CONTRIBUTING.md](../CONTRIBUTING.md). Owners and staff are named only by the names they use as staff, and only for what they did in that role. No ordinary players' names, no private messages between other people, no accusations of crimes without published evidence.
- If you cannot verify something, **do not add it**. Note it as "needs checking" instead.

## 3. Make the change everywhere

Search the whole repository for the topic (for example `grep -rn "jackpot" .`) and update **every** passage, not just the one you started with. Use the topic map:

| Topic | Where it appears |
|---|---|
| Patreon tiers, prices, perks, multiplier | README (short version, key findings), DISCREPANCIES §1, §2, §11, evidence/01, verify-yourself, reports-filed |
| Games, jackpot, poker, raffle, crates, Lucky Bags | README (short version, key findings), DISCREPANCIES §4, §6, evidence/02, verify-yourself |
| Terms, FAQ, age rule, moderation and appeals | README (staff section, key findings, why it matters), DISCREPANCIES §3, §5, §9, §10, evidence/03 |
| Staff and owner conduct | README (staff section, key findings), community-reports, CONTRIBUTING, CODE_OF_CONDUCT, evidence/03 |
| Player counts | README (key findings), DISCREPANCIES §7, community-reports |
| Client app | README (key findings), DISCREPANCIES §8, evidence/04 |
| Submission and privacy rules | README (submit section, "does not include"), CONTRIBUTING, CODE_OF_CONDUCT, CORRECTIONS (policy), .github/ISSUE_TEMPLATE/evidence.yml, this file (.github/MAINTAINING.md) |

Also:
- Re-read anything marked "cannot be concluded", "not re-tested", "unconfirmed" or "not confirmed" that the new finding affects, and update it.
- Do not rename existing section headings: links from outside the repository depend on them. Add new sections instead.

## 4. Check

- From the repository root, run `python3 tools/check.py`. It checks every internal link and anchor, and that every table row has the right number of columns.
- Re-read the README from top to bottom as a first-time reader. The summary, the findings table and the detail files must say the same thing.

## 5. Log and commit

- Add a row to the log in [CORRECTIONS.md](../CORRECTIONS.md) describing the change. If an earlier version was wrong, say so plainly and say what was wrong.
- Commit messages describe the change and end with a `Co-Authored-By:` line where applicable. Never include chat or session links.

## 6. Publish

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
