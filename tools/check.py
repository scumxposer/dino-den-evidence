#!/usr/bin/env python3
"""Consistency checks for this repository (see MAINTAINING.md).

Checks every Markdown file for:
  - internal links that point to missing files or missing heading anchors
  - tables whose rows have a different number of columns from the header

Run from the repository root:  python3 tools/check.py
Exits with status 1 if any problem is found.
"""
import glob
import os
import re
import sys


def slug(heading):
    h = heading.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def cells(line):
    # Count unescaped pipes.
    return len(re.findall(r"(?<!\\)\|", line))


def main():
    files = sorted(glob.glob("**/*.md", recursive=True))
    anchors = {
        f: {slug(m) for m in re.findall(r"^#+ (.+)$", open(f, encoding="utf-8").read(), re.M)}
        for f in files
    }
    problems = []

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

    if problems:
        print("\n".join(problems))
        return 1
    print(f"OK: {len(files)} files, all internal links and tables consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
