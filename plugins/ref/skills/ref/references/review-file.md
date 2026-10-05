# The review file format

One file per asset, named `<asset-slug>.review.md`. Two layers:

1. **The readable section** at the top, for people: reviewers, open items, decisions to make, what was decided this round (decisions plus comments now accepted, declined, deferred, done or verified), locked items, approvals, and a collapsed history of closed rounds. Once the review is closed, every round, including the last, is in the history. It ends with the credit line. The user can forward it as the record.
2. **The data block** at the bottom: the line `<!-- ref:data -->` followed by a fenced `json` block. This is the source of truth. `scripts/review_file.py` validates it and regenerates the readable section from it on every `save`.

Change the file only with `dump` → edit the JSON → `save` (see SKILL.md, "How to update the file"). `validate` is the authority on what is allowed; this page describes the same rules.

## Data model (schema `ref/1`)

```
schema: "ref/1"
project:   { id, asset_name, asset_type: copy|email|page|visual, created, deadline,
             overall_approver: reviewer_id, stage, current_round, round_scope }
reviewers: [{ id, name, role, kind: client|internal, areas: [string],
             authority: [area], contact? }]
versions:  [{ v, date, source, fingerprint, change_summary }]
rounds:    [{ n, version, requests: [{ reviewer_id, drafted, sent? }],
             responses: [{ reviewer_id, received }] }]
comments:  [{ id: "R2-07", round, reviewer_id, quote, source: email|slack|drive|pasted,
             source_ref?, secondhand: bool, anchor: { section, excerpt?, region?, page? },
             label: must_fix|preference|question|out_of_scope|reversal|approval,
             label_overridden_by_user: bool, duplicate_of?, conflict_id?,
             status: open|accepted|declined|deferred|done|verified, decision_id? }]
conflicts: [{ id, comment_ids, area, authority_holder?, recommendation, status: open|resolved }]
decisions: [{ id, round, topic, choice, rationale?, date, settles: [comment_id] }]
locks:     [{ id, element, anchor, approved_by, round, version }]
approvals: [{ reviewer_id, version, date, conditional?: string }]
meta:      { rendered_hash, ref_version }
```

`meta` also holds `reconstructed: true|false` (see below). `?` marks an optional field; leave it out or set it to `null`.

## Field rules

**Dates** are `YYYY-MM-DD`. Use today's date unless the user or the source gives another.

**IDs.** Reviewers: a short lowercase slug of the name (`dana`, `lee`). Comments: `R<round>-<two-digit seq>`, for example `R2-07`, numbered in the order they arrive within the round and never reused. Conflicts `C1`, `C2`; decisions `D1`, `D2`; locks `L1`, `L2`, numbered across the whole review.

**project**
- `id` is the asset slug; `new` sets it. `stage` is one of `setup`, `request`, `intake`, `decisions`, `fixlist`, `revision`, `closed`.
- `current_round` starts at 0 and becomes 1 when setup ends. Rounds lower than it count as closed and are collapsed in the readable section. When `stage` is `closed`, the current round is collapsed into the history too.
- `round_scope` is one sentence: what reviewers are asked to look at this round. Out-of-scope labels are judged against it.
- `overall_approver` is a reviewer id or `null`.

**reviewers**: `kind` is `client` or `internal`. `areas` are what they review ("claims", "visual", "messaging"). `authority` lists the areas where they have the final say (can be empty). `contact` is optional; store it only if the user gives it.

**versions**: `v` is an integer starting at 1. `source` says where it came from ("pasted", a file name or a URL). `fingerprint` is the first 12 hex characters of the SHA-256 of the file or pasted text, so an identical re-send is recognizable. `change_summary` is one line ("First draft", "Fix-List R1 applied; hero image swapped").

**rounds**: one entry per round. `version` is the version under review. `requests` gets an entry when Ref drafts a request (`drafted`); add `sent` only when the user says they sent it. `responses` gets an entry the first time feedback from that reviewer arrives in the round.

**comments**
- `quote` is the reviewer's exact words, never paraphrased. One comment per distinct request.
- `source` is `email`, `slack`, `drive` or `pasted`. `source_ref` is a link or message reference, not the thread.
- `secondhand` is `true` for forwarded or reported feedback ("Sam says...").
- `anchor.section` is required (a heading, an email part, or a named region). `excerpt` is a short verbatim excerpt from the asset; `region` and `page` are for visuals. Unanchored comments use `"section": "Unanchored"` until the user clarifies.
- `label_overridden_by_user` is `true` when the user changed Ref's label.
- `duplicate_of` points to the earliest comment asking for the same thing. `conflict_id` and `decision_id` link to those entries.
- Status meanings: `open` (no call yet), `accepted` (will be changed, goes on the Fix-List; never used for `approval` or `question` comments), `declined` (won't be changed), `deferred` (later, or a change order), `done` (the user says it is done but Ref couldn't verify it, or a `question` that has been answered), `verified` (Ref saw it in a new version, with evidence; or an `approval` comment, set at once when it is recorded in `approvals` or as a lock).

**conflicts**: `comment_ids` lists every comment involved, and each of those comments carries the `conflict_id`. `authority_holder` is the reviewer with the final say, if any. `recommendation` is Ref's suggestion in one sentence. `status` is `open` or `resolved`.

**decisions**: only what the user decided, in their terms. `settles` lists the comment ids it closes. `rationale` is optional, in the user's words.

**locks**: an element approved and closed to further change. `anchor` uses the same shape as a comment anchor. `approved_by` is a reviewer id. To reopen a lock, the user must decide it: remove the lock and record a decision that names it ("Reopened L1, headline").

**approvals**: one entry per sign-off. `conditional` holds the condition in the reviewer's words. Secondhand approvals are never recorded here.

**meta**: `rendered_hash` is set by `save`; never edit it. `ref_version` is set by `new`. `reconstructed` is `true` when the file was rebuilt from partial records; the readable section then says so.

## Example: one comment and one lock

```json
{
  "id": "R2-03",
  "round": 2,
  "reviewer_id": "lee",
  "quote": "We can't say 'guaranteed savings' without the terms link.",
  "source": "email",
  "source_ref": "Gmail: Re: Spring Promo v2, 2026-10-08",
  "secondhand": false,
  "anchor": { "section": "Hero", "excerpt": "guaranteed savings this spring" },
  "label": "must_fix",
  "label_overridden_by_user": false,
  "conflict_id": "C1",
  "status": "open"
}
```

```json
{
  "id": "L1",
  "element": "Subject line",
  "anchor": { "section": "Subject", "excerpt": "Spring is here. So are the savings." },
  "approved_by": "dana",
  "round": 1,
  "version": 1
}
```

## What `validate` checks

The schema id; every required key; the allowed values for asset type, stage, reviewer kind, label, status, source and conflict status; the comment id format; duplicate ids; and that every reference points at something that exists (reviewer ids, `duplicate_of`, `conflict_id`, `decision_id`, conflict comments, decision `settles`, lock `approved_by`, approval reviewer, overall approver). It does not judge whether a label is right. That is Ref's job.
