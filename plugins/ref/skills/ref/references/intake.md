# Intake

**Purpose:** turn whatever feedback arrived into individual, attributed comments with the reviewer's exact words, ready for anchoring (references/anchoring.md) and triage (references/triage.md).

## Inputs

- Pasted text, uploaded files (email exports, PDFs with comments, screenshots), or connector searches (Gmail, Slack, Google Drive).
- The review file: reviewers, current round and version, earlier comments.

## Connectors

1. **Search only what the user names:** the sources ("my email and Slack") and the timeframe ("since Tuesday"). If they don't give a timeframe, use the date the current round's requests were drafted. Search by reviewer names, the asset name, and reply threads to the request.
2. **Show before using.** Before turning anything into comments, list what was found:
   - counts by reviewer and source ("Lee: 1 email, 3 comments. Dana: 2 Slack messages. Sam: nothing found");
   - anything excluded and why ("Excluded: a thread about the Fall campaign; an out-of-office reply");
   - anything uncertain ("A message from priya@client.com. Priya isn't a reviewer. Include it?").
   Then ask for confirmation. Use only what the user confirms.
3. **Quote verbatim.** Copy the reviewer's words exactly, including typos. Store a short `source_ref` (sender, subject or channel, date, or a link), not the thread. Skip signatures, quoted earlier messages and pleasantries.
4. **Never send, reply or react.** Rule 2 holds even when the connector can. Drafts only, and only if the user asks.
5. **Failures:** if a connector isn't connected, or a search errors or times out, say which source and what failed, then ask the user to paste that feedback. Never skip a source silently and never present partial results as complete.

## Paste or upload

- Split into one comment per distinct request. "Love it, but the CTA is weak and can we lose the stock photo?" is one approval-ish remark plus two requests: decide whether the praise is an approval (triage) and keep the two requests separate.
- Keep the exact wording of each piece. Don't merge reviewers' words.
- Document comments (Google Docs, PDF annotations) usually carry their own anchor. Keep it.

## Attribution

- Every comment needs a reviewer from the file. If the author isn't clear, ask. Don't assign it to the most likely person.
- **Secondhand** ("Sam says...", a forwarded note, "the client mentioned on the call"): set `secondhand: true`, attribute it to the person whose view it is (if that person is a reviewer) and flag it for confirmation. A secondhand comment is never an approval. If it reports an approval ("Dana said it's good to go"), label it `question` and suggest the user confirm with Dana directly.
- **Non-reviewer feedback:** ask whether to add the person as a reviewer. If yes, collect their role, `client` or `internal`, areas and final-say areas (as in references/setup.md), add them to `reviewers`, then record the comment under them. If the user declines, don't record the comment: mention it in chat only, so the user can act on it outside the review. Never invent a reviewer for the user or anyone else. This includes someone other than the user who only forwards or relays another reviewer's words ("Our CFO said in standup that the pricing table is confusing", passed on by a colleague): record the relayed words under the original reviewer as secondhand either way, and ask whether to add the relayer as a reviewer. If the user says no, the relayed words stay recorded under the original reviewer; only the relayer's own comments are left out. When the user relays ("Sam says..."), don't ask whether to add the user. Don't decide any of this for the user.

## Wrong version

If feedback refers to an older version (it quotes text that has since changed, or was sent before the current version went out), flag it and offer three choices: apply it anyway, set it aside (`deferred`), or check whether the current version already covers it (if it does, mark it `verified` with the evidence).

## Recording

For each comment: the next id in the round (`R<round>-<nn>`), `round`, `reviewer_id`, `quote`, `source`, `source_ref`, `secondhand`, then anchor and label from the next two steps, `label_overridden_by_user: false`, `status: "open"`. Add each reviewer's first `responses` entry for the round. Set `stage: "intake"`, and after triage, `"decisions"` if anything needs the user, otherwise `"fixlist"`.

## Output to the user

One short summary, then the work: "14 comments from 3 reviewers. 2 conflicts, 1 reversal, 1 secondhand note to confirm, 1 comment I couldn't place." Then go to decisions (references/conflicts.md). Don't list all 14 comments unless asked.

## Example

> **Ref:** Found in Gmail and Slack since Tuesday:
> - Lee: 1 email, 3 comments.
> - Dana: 2 Slack messages, 2 comments. One says "Sam mentioned the photo feels dated", which is secondhand.
> - Sam: nothing found.
> - Excluded: an auto-reply from Lee, and a Slack thread about the Fall launch.
>
> Use these? And did Sam reply somewhere else, or should I list Sam as outstanding?
