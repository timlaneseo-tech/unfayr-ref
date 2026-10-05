# Triage

**Purpose:** give each comment one label, merge duplicates, and surface the conflicts and reversals, so the user only spends time on real decisions.

## Labels

Work through these checks in order. The first one that fits wins.

1. **`approval`**: a sign-off on the asset or an element ("Approved", "Good to go from me", "Headline is perfect, lock it"). A sign-off on the whole asset goes in `approvals` with the version and date, and the comment is set to `verified` at once (it is a record, not a change, so it never goes on a Fix-List); if it has a condition ("approved once the terms link is in"), record the condition in the reviewer's words in `conditional`. A sign-off on one element is a proposed lock, not an `approvals` entry: ask the user to confirm it, then add the lock and set the comment to `verified`. Praise isn't approval: "Love the photo" is not a sign-off. Secondhand approvals are never approvals (label them `question`, see references/intake.md).
2. **`reversal`**: contradicts a lock. Check every comment against `locks` by anchor and meaning. Show the lock: "Overruled: approved by Dana in R1 (L1, subject line)." A reversal always needs the user's decision, so always create a conflict entry for it whose recommendation names the lock id, approver and round (references/conflicts.md).
3. **`must_fix`**: legal, factual, compliance, broken (a dead link, a typo, a wrong price, a missing unsubscribe), or brand-standard items, raised by someone with authority in that area. A factual error or broken element is `must_fix` whoever raises it. A legal, compliance or factual risk raised by a reviewer without authority in that area ("I'm not sure we can say guaranteed") is labeled `question` and routed to the authority holder, named in the summary ("for Lee, who has final say on claims"). It is never `out_of_scope` and never `preference`; skip straight to check 5. Taste about the wording of a claim, with no risk raised, is still a `preference`.
4. **`out_of_scope`**: asks for something beyond `round_scope` (a new section, a different offer, a second asset, layout when the round is copy only). It displays as "possible change order" for client reviewers and "save for later" for internal ones. Propose `deferred`. Legal, factual, compliance and broken items are never out of scope, whatever the round covers: from someone with authority (or a factual error or broken element from anyone) they are `must_fix` under check 3, and from anyone else they are a `question` for the authority holder.
5. **`question`**: needs an answer, not an edit ("Is this the final price?", "Who approved this photo?"). Unanchored and secondhand items to confirm are also questions, and so is a legal, compliance or factual risk raised without authority in that area (see check 3).
6. **`preference`**: taste. Wording, color, image choice, tone, order, when no rule or authority makes it binding. The user decides.

Rules of thumb:
- Hedged language ("maybe", "I wonder if") leans `preference`; it never turns a legal requirement into one.
- One label per comment. If a remark has two requests, it should have been split at intake.
- Judge by what the reviewer asks for, not how loudly. "MUST change the blue" from someone without brand authority is a preference.

## Duplicates

Two or more comments asking for the same change at the same anchor are duplicates. Keep the earliest as the primary; set `duplicate_of` on the others to the primary's id. Every reviewer's quote stays. The primary carries the decision; give duplicates the same status. Report "asked by Lee and Dana" so the user sees the weight.

Similar isn't the same: "shorten the headline" and "make the headline punchier" are two requests that may agree or not. Don't merge them; if they pull in different directions, they're a conflict.

## Conflicts

Two or more open comments asking for incompatible changes to the same anchor or claim. Create the conflict now; resolve it in decisions (references/conflicts.md).

## Proposing statuses

Every comment needs a status before the Fix-List. Ref proposes, the user confirms, ideally in one reply:
- `must_fix` from the authority holder: propose `accepted`.
- `question`: answer it with the user (or, for a risk routed to an authority holder, with that person). Once answered, set `done`. If the answer means the asset must change, relabel the comment with the user's confirmation (`must_fix` or `preference`, `label_overridden_by_user: true`) and set `accepted`, so it goes on the Fix-List. Questions are never Fix-List items.
- `out_of_scope`: propose `deferred`.
- `preference`, `reversal`, and anything in a conflict: no proposal by default; the user decides. Ref may recommend.
- `approval`: `verified` as soon as it is recorded in `approvals` (or as a lock). Approvals are never Fix-List items.

Record nothing as decided until the user confirms. A blanket "go with your suggestions" counts as confirming everything Ref proposed, and only that.

## Overrides

The user can change any label. Set `label_overridden_by_user: true` and follow the new label's rules (for example, overriding to `out_of_scope` proposes `deferred`). Don't argue; if the override removes a legal or factual must-fix, say so once.

## Worked example

Round scope: "Copy only; layout is final." Lock L1: subject line, approved by Dana in R1.

| Comment | Label | Why |
|---|---|---|
| Lee (claims authority): "Guaranteed needs the terms link." | `must_fix` | Claims, raised by the authority holder. |
| Sam (design, internal): "Can we move the CTA above the fold?" | `out_of_scope` (save for later) | Layout is outside this round's scope. |
| Dana (client approver): "Let's try a new subject line." | `reversal` | Contradicts L1, which Dana approved in R1. |
| Priya (internal, no authority): "Drop 'guaranteed', it sounds cheap." | `preference` | A taste call on wording, from someone without claims authority. It doesn't conflict with Lee's request (Lee wants the link, not the word removed), so it isn't a conflict. |
| Sam (design, internal): "Not sure we can legally say 'guaranteed'." | `question` | A legal risk from someone without claims authority. Route it to Lee, who has final say on claims. Never out of scope, never a preference. |
| Dana: "The price says $49 but our sheet says $59." | `must_fix` | Factual, whoever raises it. |
| Dana: "Happy with the rest." | `question` | Praise, not a sign-off. Ask the user whether Dana means "approved once the fixes are in"; record an approval only if Dana confirms. |
