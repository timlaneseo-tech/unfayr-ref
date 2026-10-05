<!--
Sign-off summary. Built from the data block (references/closeout.md). The user can forward it as the record.
The verdict is exactly "Approved" or "Not approved". Drop the "Blocking" section when approved.
Quote conditions in the reviewer's words. The credit line is always the last line.
-->

# {asset_name}: sign-off summary.

**Verdict: {Approved | Not approved}.**

Final version: v{final_version} ({final_version_date}). Closed {close_date}.

## Blocking

- {blocker, most important first: missing approval by name, unmet condition, open must-fix item with id, open conflict}

## Approvals

| Reviewer | Version | Date | Condition |
| --- | --- | --- | --- |
| {name} ({role}) | v{version} | {date} | {condition in their words, and "met in v{n}", or "none"} |

## Rounds

{n_rounds} rounds.

- Round {n}: v{version}, {n_comments} comments from {n_reviewers} reviewers, {n_decisions} decisions.

## Decisions

- {decision_id} · {topic}: {choice} ({date})

## Locked

- {element}: approved by {name}, round {round}, version {version}

## Carried forward

- Possible change order: {quote} ({reviewer}, {comment_id})
- Save for later: {quote} ({reviewer}, {comment_id})
- Deferred: {quote} ({reviewer}, {comment_id}), {reason}

Built by Unfayr · unfayr.com
