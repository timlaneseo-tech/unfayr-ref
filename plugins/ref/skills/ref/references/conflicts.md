# Conflicts and decisions

**Purpose:** show the user only what needs their call, with everything needed to make it in seconds, and record what they decide. Ref recommends; it never decides.

## What counts as a conflict

Two or more open comments that ask for incompatible changes to the same anchor or claim: "make it shorter" vs "add the terms", "keep 'guaranteed'" vs "remove 'guaranteed'", "blue CTA" vs "brand says green". Comments that can both be done are not a conflict, even if they touch the same line. Say so if the user thinks they are.

A reversal (a comment that contradicts a lock) is handled the same way: the lock's approver is one side, the reversing reviewer is the other. Always create a conflict entry for it, even when the same person approved the lock and now reverses it: `comment_ids` holds the reversal comment and, if there is one, the comment that approved the lock; `recommendation` names the lock by id, approver and round ("L1, headline, approved by Jordan in R1: ..."). An open reversal with no conflict entry would not show under "Decisions to make".

## Finding the authority holder

1. Name the area the conflict is about (claims, brand, messaging, visual...), using the setup areas.
2. The reviewer with that area in `authority` is the authority holder.
3. If nobody has it, or two people do, the overall approver is.
4. Client vs internal: the client's approver holds client-facing decisions (setup.md). Always flag a client-vs-internal conflict as a client conversation and draft the message diplomatically.

## Steps

1. Create `{ id: "C<n>", comment_ids, area, authority_holder, recommendation, status: "open" }` and set `conflict_id` on each comment.
2. Recommend following the authority holder, in one sentence. Recommend something else only for a stated reason (a factual error, a legal risk, the lock was approved by someone with more authority), and give the reason.
3. Draft a short resolution message with templates/conflict-message.md, addressed to whoever's request is not being followed (or to both, if the user wants them to align first). Tone per references/voice.md.
4. Wait for the user's call.
5. Record the decision: `{ id: "D<n>", round, topic, choice, rationale?, date, settles }`. Set the settled comments' `decision_id` and status (`accepted` for the side being followed, `declined` for the other; `deferred` if the user parks it). Set the conflict to `resolved`.
6. If the decision approves an element ("the headline is final"), create a lock: element, anchor, `approved_by` (the reviewer whose approval it is; ask if unclear), round, version.
7. If the decision reopens a lock, remove the lock and name it in the decision ("Reopened L1, subject line").
8. When no conflicts, reversals or status-less comments are left, set `stage: "fixlist"` and offer the Fix-List.

## Output: the decisions list

Lead with the count as a headline ending in a full stop: "Three calls for you." Then, per item:

```
C1 · Hero claim · claims
Lee (R2-03): "We can't say 'guaranteed savings' without the terms link."
Dana (R2-05): "Keep it clean, no links in the hero."
Final say: Lee (claims).
Ref's call: follow Lee (claims). Where the link goes is your writer's call; Dana's concern is clutter in the hero.
Draft to Dana: [resolution message]
```

Referee phrases sparingly: one or two per reply at most. Then the other open items that need a call (preferences, questions), grouped, with the quote and a one-line recommendation each. Batch-confirmable items last: "Accept the 4 must-fix items as proposed?"

Never present an item without both quotes verbatim and the comment ids.

## Worked example

Lock L1: headline "Spring into savings", approved by Dana (client approver) in R1. In R3, Marcus (internal VP, no authority set) writes: "Headline is weak. Let's go with something about speed."

- Label: `reversal`. Area: messaging. Authority: Dana is the overall approver and approved the lock; Marcus has no authority listed.
- Ref says: "Flag on the play: R3-02 (Marcus: "Headline is weak. Let's go with something about speed.") reverses L1, the headline Dana approved in R1. Ref's call: keep the lock unless you want to take this to Dana. Marcus is internal, so talk to Marcus first, not the client."
- If the user keeps it: decision D4 "Keep R1 headline", settles R3-02 (`declined`), draft a direct note to Marcus. If the user reopens it: remove L1, decision D4 "Reopened L1, headline", R3-02 `accepted`, and the next client request explains the change diplomatically.
