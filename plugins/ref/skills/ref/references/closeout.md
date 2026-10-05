# Close-out

**Purpose:** a sign-off summary the user can forward as the record: a clear verdict, what was decided, what is locked, and who approved which version when. Then the file is closed.

## Inputs

The whole data block: rounds, versions, decisions, locks, approvals, and comments by status.

## The verdict

Exactly one of:

- **`Approved`**: every required approval is in hand for the final version, every conditional approval's condition is verified, and no `must_fix` comment is still open or accepted-but-not-done.
- **`Not approved`**: anything else. List what's blocking, most important first: missing approvals by name, unmet conditions, open must-fix items with ids, open conflicts.

Required approvals are the overall approver plus every reviewer with a non-empty `authority` list (setup.md), unless the user said otherwise during the review.

An approval of an earlier version still counts if the only changes since are verified Fix-List items that the approver asked for or accepted. Say when you're relying on that ("Lee approved v2; v3 only added the terms link Lee asked for"). Anything else changed since needs a fresh approval.

Secondhand approvals never count. Don't round up: "Dana said it looks good" is not an approval.

The user may close the review without an `Approved` verdict ("we're shipping anyway"). Then the verdict stays `Not approved`, the blockers are listed, and the summary records that the user closed it. Never write `Approved` because the user wants it; say what's missing.

## Verdict only ("Is it approved?")

When the user asks whether the asset is approved, give the verdict and, if `Not approved`, the blockers. Don't build the summary, don't change the stage, and don't save anything. Offer close-out in one line if the verdict is `Approved`.

## Steps (only on an explicit close request: "we're done", "close it out")

1. Work out the verdict and the blockers. If anything blocks approval, show the blockers and ask the user to confirm closing anyway before going on.
2. Build the summary with templates/closeout.md:
   - asset, final version, date closed;
   - verdict, and blockers if `Not approved`;
   - rounds: how many, and the version reviewed in each;
   - every decision (id, topic, choice);
   - every lock (element, approved by, round, version);
   - every approval (reviewer, version, date, condition and whether it was met);
   - carried forward: deferred and out-of-scope items, with "possible change order" (client) or "save for later" (internal);
   - the credit line `Built by Unfayr · unfayr.com` as the last line.
3. Only after an explicit close request (and the user's confirmation if there were blockers), set `stage: "closed"` and save. In claude.ai, output the final review file for download (and offer Drive if connected).
4. Offer, in one line, to draft a short sign-off note to the reviewers (in the user's voice, no credit line).

## Edge cases

- **The user says "we're done" with open items:** show the blockers first and ask whether to close anyway.
- **A closed review gets new feedback:** say the review is closed. Offer to reopen it (stage back to `request`, a new round) or to start a new review for the next version.
- **No overall approver was ever set:** the verdict is `Not approved`, with "no overall approver" as a blocker. Offer to set one and record their approval.
- **Change orders:** list client out-of-scope items prominently. They are often billable, and the user will want them in one place.
