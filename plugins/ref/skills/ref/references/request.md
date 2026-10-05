# Review requests

**Purpose:** draft one review request per reviewer, tailored to their areas, so each person answers the questions that matter and nothing more. Ref drafts; the user sends.

## Inputs

- The review file: reviewers, their areas and authority, `round_scope`, deadline, locks, the current round and version.
- The current version of the asset, and for round 2 onward the previous version.
- templates/request.md for the shape, and references/voice.md for tone.

## Steps

1. **What changed (round 2 onward only).** For text and HTML, run `python scripts/compare_versions.py <previous> <current>` and turn the output into two to five plain bullets a reviewer would care about ("Headline now names the offer", "Terms link added under the price"). For images and PDFs, compare the two visually and summarize the same way. Point out which changes came from that reviewer's own comments: it shows they were heard. Round 1 has no "what changed" section.
2. **Questions for their areas.** Write two or three specific questions per reviewer, from their `areas` and the open items in their areas. Good: "Lee, does the savings claim in the hero need the terms link right next to it, or is the footer enough?" Weak: "Any thoughts on legal?"
3. **Scope and locks.** State the round scope in one sentence. List what is locked and who approved it ("The subject line was approved by Dana in round 1"), so no one reopens it by accident.
4. **Deadline.** A specific date, and the time if the user gave one.
5. **Tone** from the reviewer's kind: client is diplomatic, internal is direct (references/voice.md).
6. **Record it.** For each draft, add `{ "reviewer_id", "drafted": <today> }` to the current round's `requests`. When the user says it went out, add `sent`. Keep `stage: "request"` until feedback arrives.

## Output

One draft per reviewer, each under a plain label ("For Lee (client, counsel)"), ready to copy. Subject line first if it's an email. After the drafts, one line: "Tell me when they've gone out, and I'll start the clock." Nothing else.

Don't attach or paste the asset into the draft body unless the user asks; leave a placeholder like `[link to v2]`.

## Edge cases

- **Reviewer with no areas set:** ask what they should look at, or draft a general request limited to the round scope.
- **Same message to everyone:** if the user asks for one group message, draft it with a short section per reviewer, so each person still sees their own questions.
- **Late-added reviewer in round 2+:** treat as a round 1 request for them (no "what changed"), plus the locks.
- **Only one reviewer left to approve:** the request is short: what changed, what they're asked to approve, deadline.
- **User asks Ref to send it:** rule 2. Say Ref only drafts; offer to create an email draft if a Gmail connector is available and the user wants that.
