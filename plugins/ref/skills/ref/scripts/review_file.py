"""Ref review file: data model, parsing and validation.

Standard library only. The review file is Markdown with a readable section
on top and a fenced JSON data block (the source of truth) after DATA_MARKER.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import tempfile

REF_VERSION = "1.0.0"
SCHEMA = "ref/1"
DATA_MARKER = "<!-- ref:data -->"

LABELS = ("must_fix", "preference", "question", "out_of_scope", "reversal", "approval")
STATUSES = ("open", "accepted", "declined", "deferred", "done", "verified")
ASSET_TYPES = ("copy", "email", "page", "visual")
KINDS = ("client", "internal")
SOURCES = ("email", "slack", "drive", "pasted")
STAGES = ("setup", "request", "intake", "decisions", "fixlist", "revision", "closed")

REQUIRED_KEYS = ("project", "reviewers", "versions", "rounds", "comments",
                 "conflicts", "decisions", "locks", "approvals", "meta")

COMMENT_ID_RE = re.compile(r"^R\d+-\d{2,}$")
_OPEN_FENCE_RE = re.compile(r"^(`{3,})json\s*$")


class ReviewFileError(Exception):
    """The review file could not be read."""


def parse(text):
    """Split a review file into (readable_section, data). Raises ReviewFileError."""
    if text.startswith("﻿"):
        text = text[1:]
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    marker_idx = next((i for i, ln in enumerate(lines) if ln.strip() == DATA_MARKER), None)
    if marker_idx is None:
        raise ReviewFileError("Data block marker %s not found." % DATA_MARKER)

    open_idx, fence = None, None
    for i in range(marker_idx + 1, len(lines)):
        m = _OPEN_FENCE_RE.match(lines[i].rstrip())
        if m:
            open_idx, fence = i, m.group(1)
            break
        if lines[i].strip():
            raise ReviewFileError(
                "Expected a ```json block after the data marker, found text on line %d."
                % (i + 1))
    if open_idx is None:
        raise ReviewFileError("No ```json block found after the data marker (line %d)."
                              % (marker_idx + 1))

    close_idx = next((i for i in range(open_idx + 1, len(lines))
                      if lines[i].rstrip() == fence), None)
    if close_idx is None:
        raise ReviewFileError("The data block opened on line %d is never closed."
                              % (open_idx + 1))

    body = "\n".join(lines[open_idx + 1:close_idx])
    try:
        data = json.loads(body)
    except json.JSONDecodeError as e:
        raise ReviewFileError("Invalid JSON in data block at line %d, column %d: %s"
                              % (open_idx + 1 + e.lineno, e.colno, e.msg)) from None
    if not isinstance(data, dict):
        raise ReviewFileError("Data block must be a JSON object (line %d)." % (open_idx + 2))

    readable = "\n".join(lines[:marker_idx]).rstrip("\n") + "\n"
    return readable, data


def new_data(asset_name, asset_type, created):
    """Return a valid, empty project."""
    slug = re.sub(r"[^a-z0-9]+", "-", asset_name.lower()).strip("-") or "asset"
    return {
        "schema": SCHEMA,
        "project": {
            "id": slug,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "created": created,
            "deadline": None,
            "overall_approver": None,
            "stage": "setup",
            "current_round": 0,
            "round_scope": None,
        },
        "reviewers": [],
        "versions": [],
        "rounds": [],
        "comments": [],
        "conflicts": [],
        "decisions": [],
        "locks": [],
        "approvals": [],
        "meta": {"rendered_hash": "", "ref_version": REF_VERSION, "reconstructed": False},
    }


def _as_list(data, key):
    value = data.get(key)
    return [x for x in value if isinstance(x, dict)] if isinstance(value, list) else []


def validate(data):
    """Return a list of human-readable problems; empty if the data is valid."""
    problems = []
    if not isinstance(data, dict):
        return ["Data is not an object."]

    if data.get("schema") != SCHEMA:
        problems.append("schema is %r, expected %r." % (data.get("schema"), SCHEMA))
    for key in REQUIRED_KEYS:
        if key not in data:
            problems.append("Missing required key: %s." % key)

    def check_enum(value, allowed, where):
        if value not in allowed:
            problems.append("%s has invalid value %r (allowed: %s)."
                            % (where, value, ", ".join(allowed)))

    project = data.get("project") if isinstance(data.get("project"), dict) else {}
    if "project" in data:
        check_enum(project.get("asset_type"), ASSET_TYPES, "project.asset_type")
        check_enum(project.get("stage"), STAGES, "project.stage")

    reviewers = _as_list(data, "reviewers")
    comments = _as_list(data, "comments")
    conflicts = _as_list(data, "conflicts")
    decisions = _as_list(data, "decisions")
    locks = _as_list(data, "locks")

    def ids_of(items, label):
        seen = set()
        for item in items:
            i = item.get("id")
            if i in seen:
                problems.append("Duplicate %s id: %s." % (label, i))
            seen.add(i)
        return seen

    reviewer_ids = ids_of(reviewers, "reviewer")
    comment_ids = ids_of(comments, "comment")
    conflict_ids = ids_of(conflicts, "conflict")
    decision_ids = ids_of(decisions, "decision")
    ids_of(locks, "lock")

    def ref(value, known, where, kind):
        if value not in known:
            problems.append("%s refers to unknown %s %r." % (where, kind, value))

    for r in reviewers:
        check_enum(r.get("kind"), KINDS, "reviewer %s kind" % r.get("id"))

    approver = project.get("overall_approver")
    if approver is not None:
        ref(approver, reviewer_ids, "project.overall_approver", "reviewer")

    for rnd in _as_list(data, "rounds"):
        for part in ("requests", "responses"):
            for item in rnd.get(part, []) or []:
                if isinstance(item, dict):
                    ref(item.get("reviewer_id"), reviewer_ids,
                        "round %s %s" % (rnd.get("n"), part), "reviewer")

    for c in comments:
        cid = c.get("id")
        where = "comment %s" % cid
        if not isinstance(cid, str) or not COMMENT_ID_RE.match(cid):
            problems.append("Comment id %r is not in the form R<round>-<nn>, e.g. R2-07." % cid)
        check_enum(c.get("label"), LABELS, where + " label")
        check_enum(c.get("status"), STATUSES, where + " status")
        check_enum(c.get("source"), SOURCES, where + " source")
        ref(c.get("reviewer_id"), reviewer_ids, where, "reviewer")
        if c.get("duplicate_of") is not None:
            ref(c["duplicate_of"], comment_ids, where + " duplicate_of", "comment")
        if c.get("conflict_id") is not None:
            ref(c["conflict_id"], conflict_ids, where + " conflict_id", "conflict")
        if c.get("decision_id") is not None:
            ref(c["decision_id"], decision_ids, where + " decision_id", "decision")

    for cf in conflicts:
        where = "conflict %s" % cf.get("id")
        for cid in cf.get("comment_ids", []) or []:
            ref(cid, comment_ids, where, "comment")
        if cf.get("authority_holder") is not None:
            ref(cf["authority_holder"], reviewer_ids, where + " authority_holder", "reviewer")
        check_enum(cf.get("status"), ("open", "resolved"), where + " status")

    for d in decisions:
        for cid in d.get("settles", []) or []:
            ref(cid, comment_ids, "decision %s settles" % d.get("id"), "comment")

    for lk in locks:
        ref(lk.get("approved_by"), reviewer_ids, "lock %s approved_by" % lk.get("id"), "reviewer")

    for ap in _as_list(data, "approvals"):
        ref(ap.get("reviewer_id"), reviewer_ids, "approval", "reviewer")

    meta = data.get("meta")
    if isinstance(meta, dict):
        if not isinstance(meta.get("rendered_hash"), str):
            problems.append("meta.rendered_hash must be a string.")
        if not isinstance(meta.get("ref_version"), str):
            problems.append("meta.ref_version must be a string.")
        if not isinstance(meta.get("reconstructed", False), bool):
            problems.append("meta.reconstructed must be true or false.")
    elif "meta" in data:
        problems.append("meta must be an object.")

    return problems


# ---------------------------------------------------------------------------
# Rendering, saving and hand-edit detection
# ---------------------------------------------------------------------------

CREDIT_LINE = "Built by Unfayr · unfayr.com"
RECONSTRUCTED_BANNER = "Reconstructed from partial records. Check before relying on it."

_LABEL_DISPLAY = {
    "must_fix": "must fix",
    "preference": "preference",
    "question": "question",
    "reversal": "reverses an approval",
    "approval": "approval",
}


def _one_line(value):
    """Collapse all whitespace (including newlines) so text stays on one line."""
    if value is None:
        return ""
    return " ".join(str(value).split())


def _cell(value):
    return _one_line(value).replace("|", "\\|")


def _label_text(label, kind):
    if label == "out_of_scope":
        return "possible change order" if kind == "client" else "save for later"
    return _LABEL_DISPLAY.get(label, _one_line(label))


DECIDED_STATUSES = ("accepted", "declined", "deferred", "done", "verified")


def _count(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def _hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render_readable(data):
    """Render the readable section. Ends with one newline and never contains a
    line equal to DATA_MARKER or starting a backtick fence (every line is
    prefixed by Markdown syntax and free text is collapsed to one line)."""
    project = data.get("project") if isinstance(data.get("project"), dict) else {}
    reviewers = {r.get("id"): r for r in _as_list(data, "reviewers")}
    comments = _as_list(data, "comments")
    current = project.get("current_round")
    current = current if isinstance(current, int) else 0

    def name_of(rid):
        r = reviewers.get(rid)
        return _one_line(r.get("name")) if r and r.get("name") else _one_line(rid)

    def comment_line(c):
        r = reviewers.get(c.get("reviewer_id"), {})
        return '- [%s] %s: "%s" — %s' % (
            _one_line(c.get("id")), name_of(c.get("reviewer_id")),
            _one_line(c.get("quote")), _label_text(c.get("label"), r.get("kind")))

    out = ["# %s — review" % _one_line(project.get("asset_name"))]
    if isinstance(data.get("meta"), dict) and data["meta"].get("reconstructed"):
        out += ["", RECONSTRUCTED_BANNER]
    approver = project.get("overall_approver")
    out += ["",
            "Stage: %s · Round: %s · Deadline: %s · Overall approver: %s" % (
                _one_line(project.get("stage")), current,
                _one_line(project.get("deadline")) or "none set",
                name_of(approver) if approver else "none set")]

    out += ["", "## Reviewers", ""]
    if reviewers:
        out += ["| Name | Role | Client or internal | Areas | Final say on |",
                "| --- | --- | --- | --- | --- |"]
        for r in reviewers.values():
            out.append("| %s | %s | %s | %s | %s |" % (
                _cell(r.get("name") or r.get("id")), _cell(r.get("role")),
                _cell(r.get("kind")), _cell(", ".join(map(str, r.get("areas") or []))),
                _cell(", ".join(map(str, r.get("authority") or [])))))
    else:
        out.append("No reviewers yet.")

    out += ["", "## Open items"]
    groups = {}
    for c in comments:
        if c.get("status") == "open":
            section = _one_line((c.get("anchor") or {}).get("section")) or "General"
            groups.setdefault(section, []).append(c)
    if groups:
        for section, items in groups.items():
            out += ["", "### " + section, ""]
            out += [comment_line(c) for c in items]
    else:
        out += ["", "Nothing open."]

    out += ["", "## Decisions to make", ""]
    open_conflicts = [cf for cf in _as_list(data, "conflicts") if cf.get("status") == "open"]
    if open_conflicts:
        by_id = {c.get("id"): c for c in comments}
        for cf in open_conflicts:
            ids = [str(i) for i in cf.get("comment_ids") or []]
            line = "- %s (%s): %s" % (
                _one_line(cf.get("id")), _one_line(cf.get("area")) or "no area",
                ", ".join(ids))
            if cf.get("authority_holder"):
                line += " · final say: " + name_of(cf["authority_holder"])
            if cf.get("recommendation"):
                line += " · suggested: " + _one_line(cf["recommendation"])
            out.append(line)
            for i in ids:
                if i in by_id:
                    out.append("  " + comment_line(by_id[i]))
    else:
        out.append("None.")

    decisions = _as_list(data, "decisions")

    def decision_line(d):
        return "- Decision %s: %s — %s" % (
            _one_line(d.get("id")), _one_line(d.get("topic")), _one_line(d.get("choice")))

    is_closed = project.get("stage") == "closed"
    out += ["", "## Decided this round", ""]
    if is_closed:
        out.append("The review is closed. Every round is under History.")
    else:
        decided = [decision_line(d) for d in decisions if d.get("round") == current]
        decided += [comment_line(c) + " (%s)" % _one_line(c.get("status"))
                    for c in comments
                    if c.get("round") == current and c.get("status") in DECIDED_STATUSES]
        out += decided or ["Nothing decided yet this round."]

    out += ["", "## Locked", ""]
    locks = _as_list(data, "locks")
    if locks:
        for lk in locks:
            section = _one_line((lk.get("anchor") or {}).get("section"))
            out.append("- %s%s: approved by %s, round %s, version %s" % (
                _one_line(lk.get("element")), " (%s)" % section if section else "",
                name_of(lk.get("approved_by")), _one_line(lk.get("round")),
                _one_line(lk.get("version"))))
    else:
        out.append("Nothing locked yet.")

    out += ["", "## Approvals", ""]
    approvals = _as_list(data, "approvals")
    if approvals:
        for ap in approvals:
            line = "- %s approved version %s on %s" % (
                name_of(ap.get("reviewer_id")), _one_line(ap.get("version")),
                _one_line(ap.get("date")))
            if ap.get("conditional"):
                line += " (conditional: %s)" % _one_line(ap["conditional"])
            out.append(line)
    else:
        out.append("No approvals yet.")

    out += ["", "## History"]
    round_nums = {c.get("round") for c in comments} | {r.get("n") for r in _as_list(data, "rounds")}
    closed = sorted(n for n in round_nums if isinstance(n, int) and not isinstance(n, bool)
                    and (n <= current if is_closed else n < current))
    if closed:
        for n in closed:
            rc = [c for c in comments if c.get("round") == n]
            rd = [d for d in decisions if d.get("round") == n]
            out += ["", "<details><summary>Round %d — %s, %s</summary>"
                    % (n, _count(len(rc), "comment"), _count(len(rd), "decision")), ""]
            out += [comment_line(c) + " (%s)" % _one_line(c.get("status")) for c in rc]
            out += [decision_line(d) for d in rd]
            out += ["", "</details>"]
    else:
        out += ["", "No closed rounds yet."]

    out += ["", CREDIT_LINE]
    return "\n".join(out) + "\n"


def dump_file(data):
    """Full file text. Sets data['meta']['rendered_hash'] to the readable hash."""
    readable = render_readable(data)
    meta = data.get("meta")
    if not isinstance(meta, dict):
        meta = data["meta"] = {}
    meta["rendered_hash"] = _hash(readable)
    body = json.dumps(data, indent=2, ensure_ascii=False)
    longest = max((len(m) for m in re.findall(r"`+", body)), default=0)
    fence = "`" * max(3, longest + 1)
    return "%s\n%s\n%sjson\n%s\n%s\n" % (readable, DATA_MARKER, fence, body, fence)


def load_file(path):
    """Return (data, hand_edited)."""
    with open(path, encoding="utf-8", newline="") as f:
        text = f.read()
    readable, data = parse(text)
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    return data, _hash(readable) != meta.get("rendered_hash")


def save_file(path, data):
    """Validate, then write UTF-8 with LF endings atomically (temp file in the
    same directory, then os.replace). Raises ReviewFileError."""
    problems = validate(data)
    if problems:
        raise ReviewFileError("Not saved. " + " ".join(problems))
    text = dump_file(data)
    directory = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=directory, prefix=".ref-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

HAND_EDIT_NOTICE = "HAND-EDITED: readable section changed since last render"


def _build_parser():
    parser = argparse.ArgumentParser(prog="review_file.py",
                                     description="Read and update a Ref review file.")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("new", help="create a new review file")
    p.add_argument("path")
    p.add_argument("--asset", required=True, help="asset name")
    p.add_argument("--type", required=True, choices=ASSET_TYPES, dest="asset_type")
    p.add_argument("--created", default=None, help="YYYY-MM-DD (default: today)")

    for name, helptext in (("validate", "check a review file"),
                           ("dump", "print the data block as JSON"),
                           ("render", "re-render the readable section from the data block")):
        sub.add_parser(name, help=helptext).add_argument("path")

    p = sub.add_parser("save", help="validate, render and write a review file")
    p.add_argument("path")
    p.add_argument("--data", required=True, help="path to a UTF-8 JSON file")
    return parser


def _print_problems(problems):
    for line in problems:
        print(line)
    return 1


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (OSError, ValueError):
            pass
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "new":
            if os.path.exists(args.path):
                return _print_problems(["%s already exists. Not overwritten." % args.path])
            created = args.created or datetime.date.today().isoformat()
            parent = os.path.dirname(os.path.abspath(args.path))
            os.makedirs(parent, exist_ok=True)
            save_file(args.path, new_data(args.asset, args.asset_type, created))
            print("Created %s" % args.path)
            return 0

        if args.command == "save":
            try:
                with open(args.data, encoding="utf-8-sig") as f:
                    data = json.load(f)
            except (OSError, ValueError) as e:
                return _print_problems(["Could not read %s: %s" % (args.data, e)])
            save_file(args.path, data)
            print("Saved %s" % args.path)
            return 0

        data, hand_edited = load_file(args.path)
        if args.command == "dump":
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return 0
        if args.command == "render":
            save_file(args.path, data)
            print("Rendered %s" % args.path)
            return 0
        # validate
        problems = validate(data)
        if problems:
            if hand_edited:
                print(HAND_EDIT_NOTICE)
            return _print_problems(problems)
        print(HAND_EDIT_NOTICE if hand_edited else "OK")
        return 0
    except UnicodeDecodeError as e:
        print("Could not read %s: it is not UTF-8 text (byte %d). Save it as UTF-8 and try again."
              % (args.path, e.start))
        return 1
    except (ReviewFileError, OSError) as e:
        print(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
