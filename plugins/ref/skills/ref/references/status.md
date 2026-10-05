# Status and nudges

**Purpose:** show who still owes feedback or approval, how long they've had, and draft polite nudges. Ref never sends them.

## Inputs

- The current round's `requests` (`drafted`, `sent`) and `responses`.
- `project.deadline`, `overall_approver`, the reviewers' authority, `approvals`.
- Today's date.

## Steps

1. **Outstanding reviewers:** everyone with a request in the current round and no response. Time since the request: count from `sent`, or from `drafted` if the user never confirmed sending (and say so: "drafted 3 days ago; I don't know if it went out").
2. **Overdue:** compare with the deadline. Show days left, or days overdue.
3. **Missing approvals:** required approvers (the overall approver plus anyone with authority) who haven't approved the current version. Include conditional approvals whose condition isn't verified yet.
4. **Blocking items:** open conflicts, reversals and unanswered questions waiting on a reviewer rather than the user.
5. **Draft nudges** with templates/nudge.md, one per outstanding reviewer, in the right tone (references/voice.md). Short. Mention the deadline and the one or two things you most need from that person, not a full recap.
6. Don't change the stage. A status check changes nothing in the file, unless the user moves the deadline or confirms a request was sent (then record `sent`).

## Output

```
Two people still owe feedback on v2.

- Lee (client, counsel): requested 4 days ago (sent Mon). Deadline Fri, 1 day left. Needed for the hero claim.
- Sam (internal, design): requested 4 days ago. Not blocking anything.

Approvals: Dana approved v2 on the condition that the terms link is added (not verified yet). Lee hasn't approved.
```

Then the nudge drafts, Lee's first (closest to blocking).

## Judgment

- Sort by impact: who blocks approval or a decision first, then by days waiting.
- Don't draft a nudge for someone asked less than a working day ago unless the user asks. Say "it's only been a few hours" instead.
- The deadline already passed: say it plainly, and ask whether to move the deadline (the user decides; update `project.deadline` only when they say so).
- A reviewer who answered only part (comments but no approval): list them under missing approvals, not outstanding feedback.
- If nobody is outstanding, say so in one line and suggest the next step.
