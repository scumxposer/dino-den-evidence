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
SUMMARIES_FILE = "tools/summaries.json"
SYNC_FILE = "tools/summary-sync.tsv"
HEDGES = r"\b(appear\w*|may|might|say|says|said|claim\w*|report\w*|alleged\w*|suggest\w*|according)\b"
FACTS_FILE = "tools/facts.json"

# High-risk wording. Each hit needs a human (or Claude) to confirm the line says
# no more than its source supports. Keep the lists specific: every term here
# caught a real mistake or is a known trap.
RISKY = {
    "certainty": r"\b(prove[sn]?|proof|confirm(?:s|ed)?|definitely|clearly|obviously|certainly|undeniabl\w*)\b",
    "automatic route": r"\b(end(?:s|ed)? up|convert(?:s|ed)?|turns? into|closed loop|feeds?|Patreon-funded|funded by|paid for by|sells? on|sells? for|are (?:\w+ )?sold|get sold)\b",
    "absolute": r"\b(everything|always|never|every|none|nobody|no one|everyone|all of|entirely|completely|only|all (?:the )?(?:conflicts|discrepancies|evidence|claims|figures|sources|players|staff|admins|patrons|members))\b",
    "motive": r"\b(spoof\w*|mock\w*|laugh(?:ed)? at|deliberately|intentionally|on purpose|in order to|scam\w*|fraud\w*|rigged|lie[sd]?|lying|faked?|illegal\w*|crimes?)\b",
    "generalisation": r"\b(many players|most players|routinely|regularly|repeatedly|often|usually|typically|pattern)\b",
    "completed action": r"\b(lifted|reversed|overturned|unbanned|refused|banned|removed|wiped|stripped|muted|kicked|deleted)\b",
    "actor": r"\b(?:the creator|the owner|the operator|staff|admins?|Dino Den)\b[^.;|]{0,40}?\b(?:made|set|chose|decided|hid|changed|turned)\b",
    "completeness": r"\b(covering|in full|complete(?:ly)?|entire|exhaustive|comprehensive)\b",
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
            m = re.search(r'[^.!?…]"\*? +(?:He|She|They|It|The|This|That|A|An|In|On|But|And|So|One|Two)\b', line)
            if m:
                problems.append(f"{f}:{n}: missing full stop after a quote: …{m.group(0)}…")
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


def says_column_hits(path, text):
    """Lines in a table column headed 'What … says' whose cell has words outside quotes.
    Such a column must hold the source's own words; anything else is the writer's reading."""
    hits = {}
    if path in ROOT_FILES_EXCLUDED_FROM_WORDING:
        return hits
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i + 1]):
            head = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            cols = [k for k, h in enumerate(head) if re.match(r"(?i)what .* says", h)]
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                cells_ = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                for k in cols:
                    if k < len(cells_):
                        rest = re.sub(r'\*"[^"]*"\*|"[^"]*"', " ", strip_code(cells_[k]))
                        words = re.findall(r"[A-Za-z']+", rest)
                        if len(words) > 3:
                            hits[j + 1] = "says column: words outside quotes (is this the source's claim, or ours?)"
                j += 1
            i = j
        else:
            i += 1
    return hits


NUMBERS = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def count_hits(line):
    """'four tiers (A, B and C)': the number must match the items listed."""
    out = []
    t = re.sub(r'\*"[^"]*"\*|"[^"]*"', lambda m: m.group(0).replace(",", " ").replace(" and ", " "), strip_code(line))
    for m in re.finditer(r"\b(two|three|four|five|six|seven|eight|nine|ten)\b([A-Za-z' -]{0,60}?)\(([^()]{3,300})\)", t, re.I):
        items = [x for x in re.split(r",|;|\band\b|\bor\b", m.group(3)) if x.strip()]
        if len(items) > 1 and len(items) != NUMBERS[m.group(1).lower()]:
            out.append(f"count: '{m.group(1)}{m.group(2)}' but {len(items)} items listed")
    return out


def norm_quote(q):
    return re.sub(r"\s+", " ", q.replace("’", "'").replace("…", "...").strip().lower())


def linked_quote_hits(path, line, texts):
    """Quotes on a line that cites another file in this repository must appear in that file."""
    if path in ROOT_FILES_EXCLUDED_FROM_WORDING:
        return []
    targets = []
    for link in re.findall(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)", line):
        target = os.path.normpath(os.path.join(os.path.dirname(path), link))
        if target in texts and target != path:
            targets.append(target)
    if not targets:
        return []
    out = []
    for q in re.findall(r'\*"([^"]{4,})"\*', line):
        parts = [x for x in re.split(r"…|\.\.\.", q) if len(x.strip()) > 3]
        if not all(any(norm_quote(x) in norm_quote(texts[t]) for t in targets) for x in parts):
            out.append(f"quote not found in the linked file: \"{q[:60]}\"")
    return out


SAME_PERSON = r"(?i)\bsame (player|poster|person|uploader)\b|\bone player\b|\bthe player who\b|\bthe same\b"
PLURAL = r"\b(Players|other players|another (?:player|poster)|a (?:third|second|frequent)\b|several)"


def poster_hits(path, text):
    """One person must not read as several: within a section, a second line quoting the same
    poster (or one line quoting them twice) has to say it is the same person."""
    out = {}
    if not os.path.exists("tools/sources.json") or path in ROOT_FILES_EXCLUDED_FROM_WORDING:
        return out
    reg = {k: v for k, v in json.load(open("tools/sources.json", encoding="utf-8")).items() if not k.startswith("_")}
    seen = {}
    for n, line in enumerate(text.split("\n"), 1):
        if line.startswith("#"):
            seen = {}
            continue
        quotes = " ".join(re.findall(r'"([^"]+)"', line))
        if path == "community-reports.md" and re.search(r"steamcommunity|Reddit|reddit", line):
            for q in re.findall(r'\*"([^"]{8,})"\*', line):
                if not any(f.lower() in q.lower() or q.lower() in f.lower() for frags in reg.values() for f in frags):
                    out[n] = f"player quote not in tools/sources.json: \"{q[:50]}\" (record who wrote it)"
        labels = [lab for lab, frags in reg.items() for f in frags if f.lower() in quotes.lower()]
        for lab in set(labels):
            repeated = labels.count(lab) > 1 and re.search(PLURAL, line)
            if (lab in seen or repeated) and not re.search(SAME_PERSON, line):
                out[n] = f"same poster as line {seen.get(lab, n)} ({lab}); say it is the same person"
            seen.setdefault(lab, n)
    return out


_OCR = {}


def ocr_text(img):
    """Text of a screenshot, read with tesseract (dark-mode images are inverted first)."""
    if img in _OCR:
        return _OCR[img]
    import subprocess, tempfile
    txt = ""
    try:
        from PIL import Image, ImageOps
        im = Image.open(img).convert("L")
        if sum(im.resize((50, 50)).tobytes()) / 2500 < 128:
            im = ImageOps.invert(im)
        im = im.resize((im.width * 2, im.height * 2))
        with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
            im.save(tmp.name)
            txt = subprocess.run(["tesseract", tmp.name, "-", "--psm", "4"], capture_output=True, text=True).stdout
    except Exception:
        txt = None
    _OCR[img] = txt
    return txt


def _norm_ocr(s):
    s = s.lower().replace("’", "'")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9#' ]+", " ", s)).strip()


def screenshot_quote_hits(path, text):
    """Quotes on a line that links a screenshot, or in a section that embeds one, must be readable in it."""
    import difflib
    out = {}
    current = None
    for n, line in enumerate(text.split("\n"), 1):
        if re.match(r"#{1,3} ", line):
            current = None
        emb = re.search(r"!\[[^\]]*\]\(([^)]*screenshots/[^)]+\.png)\)", line)
        if emb:
            current = os.path.normpath(os.path.join(os.path.dirname(path), emb.group(1)))
            continue
        linked = [os.path.normpath(os.path.join(os.path.dirname(path), m))
                  for m in re.findall(r"\]\(([^)]*screenshots/[^)]+\.png)\)", line)]
        imgs = linked or ([current] if current else [])
        if not imgs:
            continue
        texts = [ocr_text(i) for i in imgs if os.path.exists(i)]
        if not texts or any(t is None for t in texts):
            continue
        hay = " ".join(_norm_ocr(t) for t in texts)
        for q in re.findall(r'\*"([^"]{8,})"\*', line):
            nq = _norm_ocr(q.split("…")[0] if "…" in q else q)
            if not nq or nq in hay:
                continue
            words = hay.split(" ")
            k = len(nq.split(" "))
            best = max((difflib.SequenceMatcher(None, nq, " ".join(words[i:i + k])).ratio()
                        for i in range(max(1, len(words) - k + 1))), default=0)
            if best < 0.85:
                out.setdefault(n, []).append(f"quote not readable in the screenshot (best match {best:.2f}): \"{q[:50]}\"")
    return out


def check_hedges(problems):
    """README findings rows that are not Documented must not read as established fact."""
    for n, line in enumerate(open("README.md", encoding="utf-8").read().split("\n"), 1):
        if not line.startswith("| ") or line.startswith("| Finding"):
            continue
        cells_ = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells_) != 3:
            continue
        finding, status = cells_[0], cells_[1]
        if re.search(r"\*\*(Supported|Player claims?|Unconfirmed)\*\*", status) and not re.search(HEDGES, finding, re.I):
            problems.append(f"README.md:{n}: finding labelled '{re.search(r'[*][*]([^*]+)[*][*]', status).group(1)}' is worded as fact; "
                            "add who says it or 'appear'/'may' so the wording matches the label")


def file_hash(path):
    return hashlib.sha1(open(path, "rb").read()).hexdigest()[:16]


def load_sync():
    out = {}
    if os.path.exists(SYNC_FILE):
        for row in open(SYNC_FILE, encoding="utf-8").read().splitlines()[1:]:
            if row.strip():
                parts = row.split("\t")
                out[parts[0]] = parts
    return out


def check_summaries(problems):
    """When a detail file changes, every summary of it must be re-read before the check passes."""
    if not os.path.exists(SUMMARIES_FILE):
        problems.append(f"{SUMMARIES_FILE} is missing")
        return
    summaries = json.load(open(SUMMARIES_FILE, encoding="utf-8"))
    sync = load_sync()
    for detail, where in summaries.items():
        if detail.startswith("_"):
            continue
        if not os.path.exists(detail):
            problems.append(f"{SUMMARIES_FILE}: {detail} does not exist")
            continue
        if detail not in sync or sync[detail][1] != file_hash(detail):
            problems.append(
                f"{detail} has changed since its summaries were last checked. Re-read these and make sure they say "
                f"the same thing, with the same context and strength:\n    - " + "\n    - ".join(where) +
                f"\n  Then record it: python3 tools/check.py --synced {detail} \"what you checked\"")


def synced(detail, note):
    summaries = json.load(open(SUMMARIES_FILE, encoding="utf-8"))
    if detail not in summaries:
        print(f"{detail} is not in {SUMMARIES_FILE}")
        return 1
    if len(note.strip()) < 15:
        print("Say what you checked.")
        return 1
    sync = load_sync()
    sync[detail] = [detail, file_hash(detail), note.strip().replace("\t", " ")]
    with open(SYNC_FILE, "w", encoding="utf-8") as f:
        f.write("detail file\thash\tnote\n")
        for k in sorted(sync):
            f.write("\t".join(sync[k]) + "\n")
    print(f"Recorded summaries of {detail} as checked")
    return 0


def scan_outside(paths):
    """Run the wording scan on text that lives outside the repository (posts, replies, emails).
    Nothing is recorded: every hit must be checked against the repository before posting."""
    total = 0
    for p in paths:
        for n, line in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            hits = risky_hits("outside", line)
            if hits:
                total += 1
                print(f"{p}:{n}: [{'; '.join(hits)}]\n    {line.strip()[:300]}")
    print(f"{total} line(s) to check against the repository (same strength, same context) before posting.")
    return 0


def list_quotes():
    """Every quote on a line that cites an outside web page, grouped by the pages that line cites.
    In a full review, open each page and confirm each quote appears there word for word."""
    groups = {}
    for f in md_files():
        if f in ROOT_FILES_EXCLUDED_FROM_WORDING:
            continue
        for n, line in prose_lines(open(f, encoding="utf-8").read()):
            urls = sorted(set(re.findall(r"https?://[^\s)>\]\"*]+", line)))
            quotes = re.findall(r'\*"([^"]{6,})"\*', line)
            if urls and quotes:
                groups.setdefault(" ".join(urls), []).append((f"{f}:{n}", quotes))
    print(json.dumps(groups, indent=1, ensure_ascii=False))
    return 0


def check_wording(files, problems):
    reviews = load_reviews()
    texts = {f: open(f, encoding="utf-8").read() for f in files}
    unreviewed = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        says = says_column_hits(f, text)
        posters = poster_hits(f, text)
        shots = screenshot_quote_hits(f, text)
        for n, line in prose_lines(text):
            hits = (risky_hits(f, line) + ([says[n]] if n in says else []) + ([posters[n]] if n in posters else [])
                    + shots.get(n, [])
                    + count_hits(line) + linked_quote_hits(f, line, texts))
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
    texts = {f: open(f, encoding="utf-8").read() for f in md_files()}
    if (not risky_hits(path, line) and int(n) not in says_column_hits(path, "\n".join(lines))
            and not count_hits(line) and not linked_quote_hits(path, line, texts)
            and int(n) not in poster_hits(path, "\n".join(lines))
            and int(n) not in screenshot_quote_hits(path, "\n".join(lines))):
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
    if argv[:1] == ["--synced"] and len(argv) == 3:
        return synced(argv[1], argv[2])
    if argv[:1] == ["--quotes"]:
        return list_quotes()
    if argv[:1] == ["--outside"] and len(argv) > 1:
        return scan_outside(argv[1:])
    files = md_files()
    problems = []
    check_links_and_tables(files, problems)
    check_sentences(files, problems)
    check_facts(files, problems)
    check_dates(problems)
    check_wording(files, problems)
    check_hedges(problems)
    check_summaries(problems)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(files)} files: links, tables, sentences, facts, dates, reviewed wording, finding labels and summaries all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
