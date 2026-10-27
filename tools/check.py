#!/usr/bin/env python3
"""Consistency checks for this repository (see .github/MAINTAINING.md).

Run from the repository root:

    python3 tools/check.py                    run every check
    python3 tools/check.py --ack FILE:LINE "why it is accurate"
                                              record that a flagged line was reviewed
    python3 tools/check.py --prune            drop review records for lines that no longer exist

Checks:
  1. Links: internal links point to existing files and headings.
  2. Tables: every row has the same number of columns as its header.
  3. Sentences: broken sentences left by edits (a lowercase word after a full
     stop, doubled words, unbalanced quotes, brackets or italics).
  4. Facts: figures that appear in more than one file have the same value
     everywhere (tools/facts.json).
  5. Dates: the README's "Last updated" date matches the latest correction.
  6. Wording review: every line containing high-risk wording (certainty,
     automatic routes, motives, generalisations, staleness, or a player claim
     under a Documented label) must have been reviewed. A review is recorded
     with --ack and stored in tools/reviewed-wording.tsv. Editing a reviewed
     line invalidates its review, so changed lines are always looked at again.

Exits with status 1 if any problem is found.
"""
import glob
import hashlib
import json
import os
import re
import sys

# Rule and policy files state rules ("always hidden"), not findings, so their wording is not reviewed.
ROOT_FILES_EXCLUDED_FROM_WORDING = {"CORRECTIONS.md", ".github/MAINTAINING.md", "LICENSE", "CODE_OF_CONDUCT.md", "CONTRIBUTING.md"}
REVIEW_FILE = "tools/reviewed-wording.tsv"
FACTS_FILE = "tools/facts.json"

# High-risk wording. Each hit needs a human (or Claude) to confirm the line says
# no more than its source supports. Keep the lists specific: every term here
# caught a real mistake or is a known trap.
RISKY = {
    "certainty": r"\b(prove[sn]?|proof|confirm(?:s|ed)?|definitely|clearly|obviously|certainly|undeniabl\w*)\b",
    "automatic route": r"\b(end(?:s|ed)? up|convert(?:s|ed)?|turns? into|closed loop|feeds?|Patreon-funded|funded by|paid for by)\b",
    "absolute": r"\b(always|never|every|none|nobody|no one|everyone|all of|entirely|completely|only)\b",
    "motive": r"\b(mock\w*|laugh(?:ed)? at|deliberately|intentionally|on purpose|in order to|scam\w*|fraud\w*|rigged|lie[sd]?|lying|faked?|illegal\w*|crimes?)\b",
    "generalisation": r"\b(many players|most players|routinely|regularly|repeatedly|often|usually|typically|pattern)\b",
    "staleness": r"\b(so far|currently|not yet|not re-tested|still|recently|today|now)\b",
}
CLAIM_WORDS = r"\b(players? say|player reports?|reportedly|alleged\w*|claims?|unverified)\b"

ALLOWED_REPEATS = {"Money Money", "that that", "had had"}  # crate name; grammatical repeats
ABBREVIATIONS = r"(?:e\.g|i\.e|etc|vs|No|approx|cf|al)\."


def slug(heading):
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def cells(line):
    return len(re.findall(r"(?<!\\)\|", line))


def strip_code(line):
    line = re.sub(r"`[^`]*`", "CODE", line)
    line = re.sub(r"\]\([^)]*\)", "]", line)   # link targets
    line = re.sub(r"<https?://[^>]*>", "URL", line)
    line = re.sub(r"https?://[^\s\"*)>]+", "URL", line)
    return line


def md_files():
    return sorted(glob.glob("**/*.md", recursive=True, include_hidden=True))


def prose_lines(text):
    """Yield (line number, line) for lines outside fenced code blocks."""
    fenced = False
    for n, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            yield n, line


def line_key(path, line):
    return hashlib.sha1(f"{path}\n{line.strip()}".encode()).hexdigest()[:16]


def load_reviews():
    reviews = {}
    if os.path.exists(REVIEW_FILE):
        for row in open(REVIEW_FILE, encoding="utf-8").read().splitlines()[1:]:
            if row.strip():
                key = row.split("\t", 1)[0]
                reviews[key] = row
    return reviews


def save_reviews(reviews):
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        f.write("key\tfile\tline excerpt\treview note\n")
        for row in sorted(reviews.values(), key=lambda r: (r.split("\t")[1], r)):
            f.write(row + "\n")


def risky_hits(path, line):
    if path in ROOT_FILES_EXCLUDED_FROM_WORDING or path.startswith("evidence/snapshots"):
        return []
    text = strip_code(line)
    # Direct quotes are checked word for word against their source instead.
    text = re.sub(r'\*"[^"]*"\*|"[^"]*"', "QUOTE", text)
    hits = []
    for cat, pat in RISKY.items():
        words = sorted({m.group(0).lower() for m in re.finditer(pat, text, re.I)})
        if words:
            hits.append(f"{cat}: {', '.join(words)}")
    if re.search(r"\*\*Documented", text) and re.search(CLAIM_WORDS, text, re.I):
        hits.append("label: player claim in a Documented row")
    return hits


def check_links_and_tables(files, problems):
    anchors = {
        f: {slug(m) for m in re.findall(r"^#+ (.+)$", open(f, encoding="utf-8").read(), re.M)}
        for f in files
    }
    for f in files:
        text = open(f, encoding="utf-8").read()
        for link in re.findall(r"\]\(([^)\s]+)\)", text):
            if link.startswith(("http://", "https://", "mailto:", "../../issues")):
                continue
            path, _, anchor = link.partition("#")
            target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
            if path and not os.path.exists(target):
                problems.append(f"{f}: link to missing file: {link}")
            elif anchor and target in anchors and anchor not in anchors[target]:
                problems.append(f"{f}: link to missing heading: {link}")
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i + 1]):
                expected = cells(lines[i])
                j = i
                while j < len(lines) and lines[j].startswith("|"):
                    if cells(lines[j]) != expected:
                        problems.append(f"{f}:{j + 1}: table row has {cells(lines[j]) - 1} columns, expected {expected - 1}")
                    j += 1
                i = j
            else:
                i += 1


def check_sentences(files, problems):
    for f in files:
        if f == "LICENSE":
            continue
        for n, line in prose_lines(open(f, encoding="utf-8").read()):
            t = strip_code(line)
            if not t.strip():
                continue
            u = re.sub(ABBREVIATIONS, "", t)
            m = re.search(r"[a-z)][.] +([a-z][\w/.\-]*)", u)
            if m and not re.search(r"[/.\-]", m.group(1)):
                problems.append(f"{f}:{n}: lowercase word after a full stop (broken sentence?): …{m.group(0)}…")
            m = re.search(r"\b(\w+) \1\b", t)
            if m and not m.group(1).isdigit() and m.group(0) not in ALLOWED_REPEATS:
                problems.append(f"{f}:{n}: doubled word: {m.group(0)}")
            if t.count('"') % 2:
                problems.append(f"{f}:{n}: unbalanced double quotes")
            if t.count("(") != t.count(")"):
                problems.append(f"{f}:{n}: unbalanced parentheses")
            if t.count("[") != t.count("]"):
                problems.append(f"{f}:{n}: unbalanced square brackets")
            if t.replace("**", "").count("*") % 2:
                problems.append(f"{f}:{n}: unbalanced italics (*)")
            if re.search(r"\S  +\S", t.rstrip()) and not t.startswith("|"):
                problems.append(f"{f}:{n}: double space")
            if re.search(r"[.,;:] ?[.,;](?![a-z])|,\.(?![a-z])", t.replace("...", "").replace("…", "")):
                problems.append(f"{f}:{n}: stray punctuation")


def check_facts(files, problems):
    if not os.path.exists(FACTS_FILE):
        problems.append(f"{FACTS_FILE} is missing")
        return
    facts = json.load(open(FACTS_FILE, encoding="utf-8"))
    for fact in facts:
        found = 0
        for f in files:
            if f in ("CORRECTIONS.md", "reports-filed.md"):
                continue  # these quote earlier, corrected figures on purpose
            for n, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
                for m in re.finditer(fact["pattern"], line):
                    found += 1
                    if list(m.groups()) != fact["expected"]:
                        problems.append(
                            f"{f}:{n}: {fact['name']}: found {list(m.groups())}, expected {fact['expected']} "
                            f"(update every file, or tools/facts.json if the figure changed)")
        if found == 0:
            problems.append(f"{FACTS_FILE}: fact '{fact['name']}' no longer appears anywhere; update or remove it")


def check_dates(problems):
    readme = open("README.md", encoding="utf-8").read()
    m = re.search(r"\*Last updated: (\d+ \w+ \d{4})\.\*", readme)
    log = re.findall(r"^\| (\d+ \w+ \d{4}) \|", open("CORRECTIONS.md", encoding="utf-8").read(), re.M)
    if not m:
        problems.append("README.md: no '*Last updated: …*' line")
    elif log and m.group(1)[:-5].split()[0] + " " + m.group(1).split()[1][:3] + m.group(1)[-5:] != log[-1]:
        problems.append(f"README.md: 'Last updated: {m.group(1)}' but the latest correction is {log[-1]}")


def check_wording(files, problems):
    reviews = load_reviews()
    unreviewed = []
    for f in files:
        for n, line in prose_lines(open(f, encoding="utf-8").read()):
            hits = risky_hits(f, line)
            if hits and line_key(f, line) not in reviews:
                unreviewed.append(f"{f}:{n}: [{'; '.join(hits)}]\n    {line.strip()[:300]}")
    if unreviewed:
        problems.append(
            f"{len(unreviewed)} line(s) with high-risk wording have not been reviewed since they last changed.\n"
            "For each one, re-read the source and ask: does the line say more than the source supports\n"
            "(more certain, more general, automatic, a motive, out of date, or a player claim labelled Documented)?\n"
            "Fix it, or record the review with: python3 tools/check.py --ack FILE:LINE \"why it is accurate\"\n\n"
            + "\n".join(unreviewed))


def ack(target, note):
    path, _, n = target.rpartition(":")
    lines = open(path, encoding="utf-8").read().split("\n")
    line = lines[int(n) - 1]
    if not risky_hits(path, line):
        print(f"{target} has no high-risk wording; nothing to record")
        return 0
    if len(note.strip()) < 15:
        print("Give a real reason (what source supports the wording).")
        return 1
    reviews = load_reviews()
    excerpt = line.strip()[:80].replace("\t", " ")
    reviews[line_key(path, line)] = f"{line_key(path, line)}\t{path}\t{excerpt}\t{note.strip()}"
    save_reviews(reviews)
    print(f"Recorded review of {target}")
    return 0


def prune():
    files = md_files()
    live = {line_key(f, l) for f in files for _, l in prose_lines(open(f, encoding="utf-8").read())}
    reviews = load_reviews()
    kept = {k: v for k, v in reviews.items() if k in live}
    save_reviews(kept)
    print(f"Pruned {len(reviews) - len(kept)} stale review record(s)")
    return 0


def main(argv):
    if argv[:1] == ["--ack"] and len(argv) == 3:
        return ack(argv[1], argv[2])
    if argv[:1] == ["--prune"]:
        return prune()
    files = md_files()
    problems = []
    check_links_and_tables(files, problems)
    check_sentences(files, problems)
    check_facts(files, problems)
    check_dates(problems)
    check_wording(files, problems)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(files)} files: links, tables, sentences, facts, dates and reviewed wording all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
