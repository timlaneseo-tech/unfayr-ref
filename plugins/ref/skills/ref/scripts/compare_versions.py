#!/usr/bin/env python3
"""Section-aware diff between two versions of a marketing asset.

Usage: compare_versions.py OLD NEW [--kind text|html] [--json]
Only produces the diff; the judgment about what it means is Claude's.
"""
import argparse
import difflib
import json
import re
import sys
from html.parser import HTMLParser

TOP = "(top)"
BLOCK_TAGS = {"p", "li", "h4", "h5", "h6", "td", "th", "div", "tr", "ul", "ol",
              "table", "section", "blockquote"}
SECTION_TAGS = {"h1", "h2", "h3"}
SKIP_TAGS = {"script", "style"}
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
LIST_ITEM = re.compile(r"^(?:[-*+]|\d+[.)])\s+")
RENAME_THRESHOLD = 0.6
PAIR_THRESHOLD = 0.5
LINK_UNIT = re.compile(r"\s\[[^\]\s]*[:/#][^\]\s]*\]$")


def _collapse(s):
    return re.sub(r"\s+", " ", s).strip()


class _HtmlSections(HTMLParser):
    """Collects (section title, [units]); a unit is one block, link or image."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sections = []
        self.title = TOP
        self.units = []
        self.buf = []
        self.skip = 0
        self.in_title = False
        self.heading = None  # text parts while inside h1-h3
        self.anchor = None   # (href, text parts) while inside <a href>

    def _flush(self):
        text = _collapse("".join(self.buf))
        self.buf = []
        if text:
            self.units.append(text)

    def _end_section(self):
        self._flush()
        if self.units or self.title != TOP:
            self.sections.append((self.title, self.units))
        self.units = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in SKIP_TAGS:
            self.skip += 1
        elif tag == "title":
            self.in_title = True
            self._flush()
        elif tag in SECTION_TAGS:
            self._end_section()
            self.heading = []
        elif tag in BLOCK_TAGS:
            self._flush()
        elif tag == "br":
            self.buf.append(" ")
        elif tag == "a" and a.get("href"):
            self._flush()
            self.anchor = (a["href"].strip(), [])
        elif tag == "img" and (a.get("alt") or "").strip():
            self._flush()
            self.units.append("[image: %s]" % _collapse(a["alt"]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS:
            self.skip = max(0, self.skip - 1)
        elif tag == "title":
            self.in_title = False
        elif tag in SECTION_TAGS and self.heading is not None:
            self.title = _collapse("".join(self.heading)) or TOP
            self.heading = None
        elif tag in BLOCK_TAGS:
            self._flush()
        elif tag == "a" and self.anchor:
            href, parts = self.anchor
            self.anchor = None
            text = _collapse("".join(parts))
            self.units.append("%s [%s]" % (text, href) if text else "[%s]" % href)

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_title:
            text = _collapse(data)
            if text:
                self.units.append(text)
        elif self.heading is not None:
            self.heading.append(data)
        elif self.anchor:
            self.anchor[1].append(data)
        else:
            self.buf.append(data)


def _html_sections(text):
    p = _HtmlSections()
    p.feed(text)
    p.close()
    p._end_section()
    return [(t, "\n".join(u)) for t, u in p.sections]


def _text_sections(text):
    sections, title, units, para = [], TOP, [], []

    def flush_para():
        if para:
            units.append(_collapse(" ".join(para)))
            para.clear()

    def end_section():
        flush_para()
        if units or title != TOP:
            sections.append((title, "\n".join(units)))

    for line in text.splitlines():
        s = line.strip()
        m = HEADING.match(s)
        if m:
            end_section()
            title, units = _collapse(m.group(1)) or TOP, []
        elif not s:
            flush_para()
        else:
            if LIST_ITEM.match(s):
                flush_para()
            para.append(s)
    end_section()
    return sections


def extract_sections(text, kind):
    """Return [(section_title, normalized_body)]; body units are newline-separated."""
    text = text.lstrip("﻿")
    if kind == "html":
        return _html_sections(text)
    if kind == "text":
        return _text_sections(text)
    raise ValueError("kind must be 'text' or 'html'")


def _sentences(body):
    out = []
    for unit in body.split("\n"):
        if LINK_UNIT.search(unit):
            out.append(unit)  # "text [href]" link units stay whole
        else:
            out.extend(s for s in SENTENCE_SPLIT.split(unit) if s)
    return out


def _ratio(a, b):
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def _match_sections(old, new):
    """Return ([(old_idx or None, new_idx)] in new order, unmatched old indexes)."""
    match, used = {}, set()
    for j, (nt, _) in enumerate(new):
        for i, (ot, _) in enumerate(old):
            if i not in used and ot == nt:
                match[j] = i
                used.add(i)
                break
    cands = []
    for j, (_, nb) in enumerate(new):
        if j in match:
            continue
        for i, (_, ob) in enumerate(old):
            if i not in used:
                r = _ratio(ob, nb)
                if r >= RENAME_THRESHOLD:
                    cands.append((r, i, j))
    for _, i, j in sorted(cands, key=lambda c: -c[0]):
        if j not in match and i not in used:
            match[j] = i
            used.add(i)
    pairs = [(match.get(j), j) for j in range(len(new))]
    return pairs, [i for i in range(len(old)) if i not in used]


def _item(section, change, before, after):
    return {"section": section, "change": change, "before": before, "after": after}


def _pair_replaced(section, old_s, new_s):
    """Pair removed with added units by best similarity (greedy, ratio at least
    PAIR_THRESHOLD, ties broken by position). Unpaired units are removed or added."""
    cands = sorted((-_ratio(x, y), i, j) for i, x in enumerate(old_s)
                   for j, y in enumerate(new_s))
    pair_of_new, used_old = {}, set()
    for neg, i, j in cands:
        if -neg < PAIR_THRESHOLD:
            break
        if i not in used_old and j not in pair_of_new:
            pair_of_new[j] = i
            used_old.add(i)
    items = [_item(section, "removed", x, "") for i, x in enumerate(old_s) if i not in used_old]
    for j, y in enumerate(new_s):
        if j in pair_of_new:
            items.append(_item(section, "modified", old_s[pair_of_new[j]], y))
        else:
            items.append(_item(section, "added", "", y))
    return items


def _diff_bodies(section, ob, nb):
    a, b = _sentences(ob), _sentences(nb)
    items = []
    matcher = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "delete":
            items += [_item(section, "removed", s, "") for s in a[i1:i2]]
        elif op == "insert":
            items += [_item(section, "added", "", s) for s in b[j1:j2]]
        elif op == "replace":
            items += _pair_replaced(section, a[i1:i2], b[j1:j2])
    return items


def compare(old, new, kind):
    o, n = extract_sections(old, kind), extract_sections(new, kind)
    pairs, removed = _match_sections(o, n)
    items = []
    for i, j in pairs:
        nt, nb = n[j]
        if i is None:
            items += [_item(nt, "added", "", s) for s in _sentences(nb)] or [_item(nt, "added", "", "")]
            continue
        ot, ob = o[i]
        label = nt if ot == nt else "%s -> %s" % (ot, nt)
        if ot != nt:
            items.append(_item(label, "modified", ot, nt))
        items += _diff_bodies(label, ob, nb)
    for i in removed:
        ot, ob = o[i]
        items += [_item(ot, "removed", s, "") for s in _sentences(ob)] or [_item(ot, "removed", "", "")]
    return items


def format_markdown(items):
    if not items:
        return "No differences."
    lines, current = [], None
    for it in items:
        if it["section"] != current:
            if lines:
                lines.append("")
            current = it["section"]
            lines.append("### %s" % current)
        lines.append("- change: %s" % it["change"])
        lines.append("- before: %s" % it["before"])
        lines.append("- after: %s" % it["after"])
    return "\n".join(lines)


def _kind_for(path):
    return "html" if path.lower().endswith((".html", ".htm")) else "text"


def _read(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def _emit(text):
    data = (text + "\n").encode("utf-8")
    buf = getattr(sys.stdout, "buffer", None)
    if buf is not None:
        buf.write(data)
        buf.flush()
    else:
        sys.stdout.write(text + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Section-aware diff of two asset versions.")
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--kind", choices=["text", "html"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        old, new = _read(args.old), _read(args.new)
    except (OSError, UnicodeDecodeError) as e:
        _emit("Cannot read input file: %s" % (getattr(e, "filename", None) or e))
        return 2
    items = compare(old, new, args.kind or _kind_for(args.new))
    _emit(json.dumps(items, indent=2, ensure_ascii=False) if args.json else format_markdown(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
