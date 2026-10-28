#!/usr/bin/env python3
"""Consistency checks for this repository (see .github/MAINTAINING.md).

Run from the repository root:

    python3 tools/check.py                    run every check
    python3 tools/check.py --ack FILE:LINE "why it is accurate"
                                              record that a flagged line was reviewed
    python3 tools/check.py --prune            drop review records for lines that no longer exist
    python3 tools/check.py --synced FILE "what you checked"
                                              record that a changed detail file's summaries were re-read
    python3 tools/check.py --quotes           list the quotes the audit still has to check (unverified, changed,
                                              or from a live page), by the page they come from
    python3 tools/check.py --quotes --all     list every quote, verified or not
    python3 tools/check.py --verified SOURCE "how you checked"
                                              record every quote currently listed under SOURCE as checked
                                              (SOURCE is a URL, or FILE§HEADING for quotes with no link on the line)
    python3 tools/check.py --acks [CATEGORY]  list recorded reviews with their reasons, to re-check in a full review
    python3 tools/check.py --outside FILES    scan posts, replies and emails before (and after) they go out

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

  7. Known errors: wording corrected once (tools/known-errors.json) must not
     come back anywhere, in the repository or in outside text. These cannot
     be cleared with --ack.

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
    "absolute": r"\b(unrestricted|everything|always|never|every|none|nobody|no one|everyone|all of|entirely|completely|only|all (?:the )?(?:conflicts|discrepancies|evidence|claims|figures|sources|players|staff|admins|patrons|members))\b",
    "motive": r"\b(spoof\w*|mock\w*|laugh(?:ed)? at|deliberately|intentionally|on purpose|in order to|scam\w*|fraud\w*|rigged|lie[sd]?|lying|faked?|illegal\w*|crimes?)\b",
    "generalisation": r"\b(many players|most players|routinely|regularly|repeatedly|often|usually|typically|pattern)\b",
    "completed action": r"\b(lifted|reversed|overturned|unbanned|refused|banned|removed|wiped|stripped|muted|kicked|deleted)\b",
    "actor": r"\b(?:the creator|the owner|the operator|staff|admins?|Dino Den)\b[^.;|]{0,40}?\b(?:made|set|chose|decided|hid|changed|turned)\b",
    "completeness": r"\b(covering|in full|complete(?:ly)?|entire|exhaustive|comprehensive)\b",
    "staleness": r"\b(so far|currently|not yet|not re-tested|still|recently|today|now)\b",
    # Whether something breaks a platform's rules or the law is for that platform or a regulator to decide.
    "verdict": r"\b(?:go(?:es)?|going|went|is|are|runs?) against\b[^.;|]{0,30}\b(?:rules|guidelines|polic(?:y|ies)|law|terms)\b|\bbreak(?:s|ing)?\b[^.;|]{0,30}\b(?:rules|guidelines|polic(?:y|ies)|law)\b|\bviolat\w+|\bin breach\b|\bunlawful\b|\bshouldn't\b|\bnot allowed\b",
}
KNOWN_ERRORS_FILE = "tools/known-errors.json"
# Files that record past errors on purpose.
KNOWN_ERRORS_EXEMPT = {"CORRECTIONS.md", ".github/MAINTAINING.md"}
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


# Checks added after a line was reviewed must still be looked at: a review records the kinds of hit it
# covered (5th column). Records made before kinds were recorded cover everything except these.
KINDS_ADDED_LATER = {"quote punctuation"}


def hit_kind(hit):
    if hit.startswith("quote punctuated differently"):
        return "quote punctuation"
    return hit.split(":")[0].split("(")[0].strip()[:40]


def review_covers(row, hits):
    cols = row.split("\t")
    kinds = {hit_kind(h) for h in hits}
    if len(cols) >= 5:
        return kinds <= set(cols[4].split(","))
    return not (kinds & KINDS_ADDED_LATER)


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
        f.write("key\tfile\tline excerpt\treview note\tchecks covered\n")
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
        if "snapshot" in fact:
            snapfile = sorted(glob.glob("evidence/snapshots/*/api-snapshot.json"))[-1]
            data = json.load(open(snapfile, encoding="utf-8"))
            vals = []
            for path_ in fact["snapshot"]:
                is_len = path_.startswith("len:")
                cur = data
                for part in path_.replace("len:", "").split("."):
                    cur = cur[part]
                vals.append(f"{len(cur) if is_len else cur:,}")
            if vals != fact["expected"]:
                problems.append(f"{FACTS_FILE}: fact '{fact['name']}' expects {fact['expected']} but the snapshot says {vals}")


def check_dates(problems):
    """README 'Last updated' must not be earlier than the newest correction, and must be today (US Pacific)
    whenever content files have changed since the last commit; a new correction row must carry today's date."""
    import datetime, subprocess
    readme = open("README.md", encoding="utf-8").read()
    m = re.search(r"\*Last updated: (\d+ \w+ \d{4})\.\*", readme)
    log = re.findall(r"^\| (\d+ \w+ \d{4}) \|", open("CORRECTIONS.md", encoding="utf-8").read(), re.M)
    parse = lambda d: datetime.datetime.strptime(d[:-5].split()[0] + " " + d.split()[1][:3] + d[-5:], "%d %b %Y").date()
    pacific = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=7)).date()
    if not m:
        problems.append("README.md: no '*Last updated: …*' line")
        return
    updated = parse(m.group(1))
    if log and updated < max(parse(d) for d in log):
        problems.append(f"README.md: 'Last updated: {m.group(1)}' is earlier than the newest correction ({log[-1]})")
    def changed(paths):
        try:
            return subprocess.run(["git", "diff", "--quiet", "HEAD", "--"] + paths).returncode == 1
        except OSError:
            return False
    if changed(md_files()) and updated != pacific:
        problems.append(f"README.md: content has changed, so 'Last updated' should be today ({pacific.day} {pacific.strftime('%B')} {pacific.year})")
    try:
        old = subprocess.run(["git", "show", "HEAD:CORRECTIONS.md"], capture_output=True, text=True).stdout
    except OSError:
        old = ""
    old_rows = set(re.findall(r"^\|.*$", old, re.M))
    for row in re.findall(r"^\| \d+ \w+ \d{4} \|.*$", open("CORRECTIONS.md", encoding="utf-8").read(), re.M):
        d = re.match(r"^\| (\d+ \w+ \d{4})", row).group(1)
        if old and not os.environ.get("RESTRUCTURE_CORRECTIONS") and row not in old_rows and parse(d) != pacific and not any(r.startswith("| " + d) and r[len(d) + 5:][:60] == row[len(d) + 5:][:60] for r in old_rows):
            problems.append(f"CORRECTIONS.md: a new row is dated {d} but today is {pacific.day} {pacific.strftime('%b')} {pacific.year} (US Pacific)")


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


def _quote_words(q):
    return " ".join(re.findall(r"[a-z0-9#@']+", q.replace("’", "'").lower()))


def quote_variant_hits(texts):
    """The same quote must be punctuated the same way everywhere. A quote that ends with a full stop
    (or ? !) is flagged when another quote of the same words, or a longer quote containing them,
    shows no such punctuation at that point: one of the two is wrong, so check the source. Summaries
    do not always link the detail file on the same line, so the comparison is across all files."""
    quotes = []
    for f, text in texts.items():
        if f in ROOT_FILES_EXCLUDED_FROM_WORDING:
            continue
        for n, line in prose_lines(text):
            # pair quotation marks in order, so a short quote ("locked") can't shift the pairing
            for q in [q for q in re.findall(r'"([^"]*)"', line) if len(q) >= 8]:
                quotes.append((f, n, norm_quote(q), _quote_words(q)))
    out = {}
    for f, n, raw, words in quotes:
        if not re.search(r"(?<!\.)[.!?]$", raw) or len(words.split()) < 3:
            continue  # no end punctuation to check, or an ellipsis
        mark = raw[-1]
        pat = re.compile(r"\W+".join(re.escape(w) for w in words.split()) + r"(?P<after>\W*)")
        for f2, n2, raw2, words2 in quotes:
            if (f2, n2) == (f, n) or words not in words2:
                continue
            m = pat.search(raw2)
            after = re.sub(r"[^.!?]", "", m.group("after")) if m else ""
            if m and not after.startswith(mark) and (after or m.end() < len(raw2) or raw2 == raw2.rstrip(".!?")):
                out.setdefault(f, {})[n] = (f"quote punctuated differently from {f2}:{n2} "
                                           f"(\"…{raw[-30:]}\" ends with '{mark}' where the other has '{after[:1] or "nothing"}'): check the source and make them agree")
                break
    return out


SAME_PERSON = (r"(?i)\bsame (player|poster|person|uploader)\b|\bone player\b|\bthe player who\b|\bthe same\b"
               r"|former trial admin|author of the Honest Opinion thread|same Reddit player")
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
            continue  # the same person can recur across sections, so the check covers the whole file
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
        raw = re.sub(r"\s+", " ", " ".join(texts))
        # A full stop inside the quotation marks must be in the image too (OCR rarely invents one).
        for q in re.findall(r'\*"([^"]{8,}[.!?])"\*', line):
            tail = re.escape(re.sub(r"[.!?]$", "", q).split(" ")[-1])
            if re.search(tail + r"\b", raw, re.I) and not re.search(tail + r"\s?[.!?]", raw, re.I):
                out.setdefault(n, []).append(f"quote ends with '{q[-1]}' but the screenshot shows none after '{q.split(' ')[-1][:-1]}'")
        for q in re.findall(r'\*"([^"]{8,})"\*', line):
            nq = _norm_ocr(q.split("…")[0] if "…" in q else q)
            if not nq or nq in hay or nq.replace(" ", "") in hay.replace(" ", ""):
                continue
            words = hay.split(" ")
            qw = nq.split(" ")
            k = len(qw)

            def word_ok(a, b):
                # Exact match, or OCR noise inside a longer word (never for short words like "i", "ill").
                return a == b or (len(a) >= 5 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.8)

            best = max((sum(word_ok(a, b) for a, b in zip(qw, words[i:i + k])) / k
                        for i in range(max(1, len(words) - k + 1))), default=0)
            if best < 1.0:
                out.setdefault(n, []).append(f"quote not readable in the screenshot (best match {best:.2f}): \"{q[:50]}\"")
    return out


SOURCE_RULES_FILE = "tools/source-rules.json"


def _sentences(line):
    return re.split(r"(?<=[.;!?])\s+(?=[A-Z*(\[])|\s*\|\s*", line)


def check_source_rules(files, problems):
    """Dates and origins of particular sources must be stated the same way everywhere, and a poster
    who is quoted in several sections must be identified in each one (tools/source-rules.json)."""
    if not os.path.exists(SOURCE_RULES_FILE):
        return
    rules = json.load(open(SOURCE_RULES_FILE, encoding="utf-8"))
    month = r"\b(?:\d{1,2} )?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? \d{4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b"
    reg = {k: v for k, v in json.load(open("tools/sources.json", encoding="utf-8")).items() if not k.startswith("_")}
    for f in files:
        if f in ROOT_FILES_EXCLUDED_FROM_WORDING:
            continue
        text = open(f, encoding="utf-8").read()
        section, section_lines = "", []
        sections = []
        for n, line in prose_lines(text):
            if re.match(r"#{1,3} ", line):
                sections.append((section, section_lines))
                section, section_lines = line, []
            section_lines.append((n, line))
            for sent in _sentences(line):
                for r in rules.get("dated", []):
                    m = re.search(r["mention"], sent)
                    near = sent[max(0, m.start() - 45):m.end() + 45] if m else ""
                    if m and re.search(month, near) and not re.search(r["allowed"], sent):
                        problems.append(f"{f}:{n}: {r['name']} dated differently from its source ({r['why']}); use \"{r['allowed']}\"…\n    {sent.strip()[:200]}")
                for r in rules.get("attribution", []):
                    if re.search(r["pattern"], sent) and not re.search(r["require"], sent):
                        problems.append(f"{f}:{n}: {r['name']} stated without saying where it comes from ({r['why']})\n    {sent.strip()[:200]}")
        sections.append((section, section_lines))
        for img in sorted(set(re.findall(r"\]\(((?:\.\./)?(?:evidence/)?screenshots/[^)\s]+\.png)\)", text))):
            path_img = os.path.normpath(os.path.join(os.path.dirname(f), img))
            words = rules.get("image_forbidden", {}).get("words", [])
            if os.path.exists(path_img) and words:
                seen_text = ocr_text(path_img).lower()
                for w in words:
                    if re.search(r"\b" + re.escape(w), seen_text):
                        problems.append(f"{path_img}: the word \"{w}\" is readable in a published screenshot; hide it (no unproven accusations)")
        for heading, lines in sections:
            body = "\n".join(l for _, l in lines)
            for label, phrase in rules.get("identify", {}).items():
                for n, line in lines:
                    quotes = " ".join(re.findall(r'"([^"]+)"', line)).lower()
                    if any(fr.lower() in quotes for fr in reg.get(label, [])) and phrase.lower() not in body.lower():
                        problems.append(f"{f}:{n}: quotes {label} but the section ({heading.strip('# ')[:50]}) never says so "
                                        f"(add \"{phrase}\"), so one person can read as several")
                        break


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


def load_known_errors():
    if not os.path.exists(KNOWN_ERRORS_FILE):
        return []
    return json.load(open(KNOWN_ERRORS_FILE, encoding="utf-8"))


def known_error_hits(line, known=None):
    """Wording that was corrected once must never come back, anywhere. These cannot be cleared with --ack."""
    hits = []
    for e in (known if known is not None else load_known_errors()):
        text = line if e.get("match_quotes") else re.sub(r'\*"[^"]*"\*|"[^"]*"', "QUOTE", line)
        if re.search(e["pattern"], text, re.I):
            hits.append(f"KNOWN ERROR: {e['why']}")
    return hits


def check_known_errors(files, problems):
    known = load_known_errors()
    found = []
    for f in files:
        if f in KNOWN_ERRORS_EXEMPT or f.startswith("evidence/snapshots"):
            continue
        for n, line in prose_lines(open(f, encoding="utf-8").read()):
            for h in known_error_hits(line, known):
                found.append(f"{f}:{n}: [{h}]\n    {line.strip()[:300]}")
    if found:
        problems.append(f"{len(found)} line(s) repeat wording that was already corrected (tools/known-errors.json). "
                        "Fix them; these cannot be recorded as reviewed.\n" + "\n".join(found))


def list_acks(category=""):
    """Every recorded wording review that still applies, with its reason, for re-checking in a full review."""
    reviews = load_reviews()
    texts = {f: open(f, encoding="utf-8").read() for f in md_files()}
    count = 0
    for f in md_files():
        for n, line in prose_lines(texts[f]):
            k = line_key(f, line)
            if k not in reviews:
                continue
            hits = risky_hits(f, line)
            if category and not any(h.startswith(category) for h in hits):
                continue
            count += 1
            print(f"{f}:{n}: [{'; '.join(hits) or 'other check'}]\n    LINE: {line.strip()[:400]}\n    REASON: {reviews[k].split(chr(9))[3]}")
    print(f"{count} recorded review(s). Re-read each line against its source: is the reason still true, and does it cover every flagged word?")
    return 0


def scan_outside(paths):
    """Run the wording scan on text that lives outside the repository (posts, replies, emails).
    Nothing is recorded: every hit must be checked against the repository before posting."""
    total = 0
    for p in paths:
        for n, line in enumerate(open(p, encoding="utf-8").read().split("\n"), 1):
            hits = known_error_hits(line) + risky_hits("outside", line)
            if hits:
                total += 1
                print(f"{p}:{n}: [{'; '.join(hits)}]\n    {line.strip()[:300]}")
    print(f"{total} line(s) to check against the repository (same strength, same context) before posting.")
    return 0


VERIFIED_FILE = "tools/verified-sources.json"


def load_verified():
    if not os.path.exists(VERIFIED_FILE):
        return {"stability": [], "verified": {}}
    return json.load(open(VERIFIED_FILE, encoding="utf-8"))


def source_class(source, reg):
    """stable: old forum posts, videos, archives, legislation, screenshots (checked once, then only if
    the quote changes); slow: re-check after N days; live: re-check in every full review."""
    sec = reg.get("sections", {}).get(source)
    if sec:
        return sec["class"], sec.get("recheck_days", 0)
    for rule in reg.get("stability", []):
        if re.search(rule["match"], source):
            return rule["class"], rule.get("recheck_days", 0)
    return "live", 0


def quote_groups():
    groups = {}
    for f in md_files():
        if f in ROOT_FILES_EXCLUDED_FROM_WORDING:
            continue
        heading, last_url = "", None
        for n, line in prose_lines(open(f, encoding="utf-8").read()):
            if line.startswith("#"):
                heading, last_url = line.strip("# ").strip(), None
            urls = sorted(set(re.findall(r"https?://[^\s)>\]\"*]+", line)))
            quotes = re.findall(r'\*"([^"]{2,})"\*', line)
            if quotes:
                # A quote with no outside link on its line still has a source (the nearest link above in
                # the section, a screenshot, a file in this repository, or a source the line names): it is
                # keyed by file and section, and classed by that nearest link, so a live page stays live.
                # A line that links a published screenshot and no web page is keyed by the image: images
                # don't change, and the OCR check compares those quotes with the image on every run.
                shots = sorted(set(re.findall(r"\((?:\.\./)?(?:evidence/)?screenshots/([^)\s]+)\)", line)))
                if urls:
                    key = " ".join(urls)
                elif shots:
                    key = "screenshot:" + " ".join(shots)
                else:
                    key = f"{f}§{heading}" + (f" (nearest link: {last_url})" if last_url else "")
                groups.setdefault(key, []).append((f"{f}:{n}", quotes))
            if urls:
                last_url = urls[-1]
    return groups


def quotes_due(groups, reg, today=None):
    import datetime
    today = today or datetime.date.today()
    due = {}
    for key, items in groups.items():
        cls, days = source_class(key, reg)
        done = reg.get("verified", {}).get(key, {})
        for loc, qs in items:
            for q in qs:
                rec = done.get(q)
                if rec and q in reg.get("stable_quotes", {}):
                    continue  # this quote's own source is fixed (a screenshot, forum post or sent email)
                if rec and cls == "stable":
                    continue
                if rec and cls == "live" and rec[:10] == today.isoformat():
                    continue  # live pages: once per day
                if rec and cls == "slow":
                    when = datetime.date.fromisoformat(rec[:10])
                    if (today - when).days < days:
                        continue
                due.setdefault(key, []).append((loc, q, cls, rec or "never checked"))
    return due


def list_quotes(show_all=False):
    """The quote audit. In a full review, open each listed page (or image) and confirm each quote
    appears there word for word, written by the person and on the date the repository says."""
    reg = load_verified()
    groups = quote_groups()
    if show_all:
        print(json.dumps(groups, indent=1, ensure_ascii=False))
        return 0
    due = quotes_due(groups, reg)
    total = sum(len(qs) for v in groups.values() for _, qs in v)
    n_due = sum(len(v) for v in due.values())
    for key, items in due.items():
        print(key)
        for loc, q, cls, rec in items:
            print(f"    [{cls}; last: {rec[:60]}] {loc}: \"{q[:90]}\"")
    print(f"{n_due} of {total} quotes to check. Stable sources already verified are skipped "
          f"(record new checks with --verified SOURCE \"how\").")
    return 0


def verified(source, how):
    import datetime
    if len(how.strip()) < 15:
        print("Say how the quotes were checked (page opened, author and date, image compared).")
        return 1
    groups = quote_groups()
    if source not in groups:
        print(f"No quotes are listed under {source}; run --quotes --all to see the source keys.")
        return 1
    reg = load_verified()
    rec = reg.setdefault("verified", {}).setdefault(source, {})
    stamp = f"{datetime.date.today().isoformat()} {how.strip()}"
    qs = {q for _, qq in groups[source] for q in qq}
    for q in qs:
        rec[q] = stamp
    # drop records for quotes no longer in the repository under this source
    for q in [q for q in rec if q not in qs]:
        del rec[q]
    json.dump(reg, open(VERIFIED_FILE, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(VERIFIED_FILE, "a", encoding="utf-8").write("\n")
    print(f"Recorded {len(qs)} quote(s) under {source} as checked")
    return 0


def check_wording(files, problems):
    reviews = load_reviews()
    texts = {f: open(f, encoding="utf-8").read() for f in files}
    variants = quote_variant_hits(texts)
    unreviewed = []
    for f in files:
        text = open(f, encoding="utf-8").read()
        says = says_column_hits(f, text)
        posters = poster_hits(f, text)
        shots = screenshot_quote_hits(f, text)
        for n, line in prose_lines(text):
            hits = (risky_hits(f, line) + ([says[n]] if n in says else []) + ([posters[n]] if n in posters else [])
                    + ([variants[f][n]] if n in variants.get(f, {}) else [])
                    + shots.get(n, [])
                    + count_hits(line) + linked_quote_hits(f, line, texts))
            if hits and not (line_key(f, line) in reviews and review_covers(reviews[line_key(f, line)], hits)):
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
            and int(n) not in quote_variant_hits(texts).get(path, {})
            and int(n) not in screenshot_quote_hits(path, "\n".join(lines))):
        print(f"{target} has no high-risk wording; nothing to record")
        return 0
    if len(note.strip()) < 15:
        print("Give a real reason (what source supports the wording).")
        return 1
    text = "\n".join(lines)
    hits = (risky_hits(path, line) + ([says_column_hits(path, text)[int(n)]] if int(n) in says_column_hits(path, text) else [])
            + count_hits(line) + linked_quote_hits(path, line, texts)
            + ([poster_hits(path, text)[int(n)]] if int(n) in poster_hits(path, text) else [])
            + screenshot_quote_hits(path, text).get(int(n), [])
            + ([quote_variant_hits(texts)[path][int(n)]] if int(n) in quote_variant_hits(texts).get(path, {}) else []))
    reviews = load_reviews()
    old = reviews.get(line_key(path, line), "").split("\t")
    kinds = {hit_kind(h) for h in hits} | (set(old[4].split(",")) if len(old) >= 5 else set())
    excerpt = line.strip()[:80].replace("\t", " ")
    note = note.strip() if len(old) < 4 or note.strip() in old[3] else (old[3] + " | " + note.strip() if old[0] else note.strip())
    reviews[line_key(path, line)] = f"{line_key(path, line)}\t{path}\t{excerpt}\t{note}\t{','.join(sorted(kinds))}"
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
        return list_quotes(show_all="--all" in argv)
    if argv[:1] == ["--verified"] and len(argv) == 3:
        return verified(argv[1], argv[2])
    if argv[:1] == ["--acks"]:
        return list_acks(argv[1] if len(argv) > 1 else "")
    if argv[:1] == ["--outside"] and len(argv) > 1:
        return scan_outside(argv[1:])
    files = md_files()
    problems = []
    check_links_and_tables(files, problems)
    check_sentences(files, problems)
    check_facts(files, problems)
    check_dates(problems)
    check_wording(files, problems)
    check_known_errors(files, problems)
    check_hedges(problems)
    check_source_rules(files, problems)
    check_summaries(problems)
    live = {line_key(f, l) for f in files for _, l in prose_lines(open(f, encoding="utf-8").read())}
    stale = [k for k in load_reviews() if k not in live]
    if stale:
        problems.append(f"{len(stale)} review record(s) are for lines that no longer exist. A stale record would accept "
                        f"that old text if it came back. Run: python3 tools/check.py --prune")
    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(files)} files: links, tables, sentences, facts, dates, reviewed wording, finding labels and summaries all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
