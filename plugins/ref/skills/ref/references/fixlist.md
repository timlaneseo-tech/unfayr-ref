# Fix-List

**Purpose:** one checklist of changes for whoever edits the asset (the user, a writer, a designer). It says what to change and why, in the reviewers' own words. It never says how the new version should read: rule 1.

## Inputs

- All comments with status `accepted`, from this round and carried over from earlier rounds (partly done or not done items). Never include comments labeled `approval` or `question`: approvals are records, and questions get answers, not edits.
- Decisions and their notes, locks, and declined and deferred comments.

## Before building it

- Every comment in the round has a status other than `open`. If some are still open, list them and ask (or propose, per references/triage.md). Don't silently leave them out.
- No open conflicts. If there are, say which and offer to settle them first. If the user insists, build the list and mark the affected items "waiting on C2".

## Format

A headline with the count, ending in a full stop. Then items grouped by anchor, in document order (top of the asset to bottom; for PDFs, by page then region). Each item:

```
- [ ] Hero · "guaranteed savings this spring"
      Add the terms link next to the savings claim.
      Lee (R2-03): "We can't say 'guaranteed savings' without the terms link."
      Decision D2: link under the hero, not in it.
```

- Line 1: a checkbox, the anchor section, and the excerpt (so the editor can search for it).
- Line 2: the change needed, as a plain instruction derived from the request, never new wording. "Add the terms link next to the claim", not "Change to: Save 20%*". If the reviewer supplied exact replacement text, quote it as theirs: `Use Dana's wording: "..."`.
- Line 3: every reviewer's quote with comment ids, including duplicates ("Lee (R2-03), Dana (R2-06)").
- Line 4: decision notes, if any.

After the checklist:
- **Locked, don't touch:** each lock with element and who approved it.
- **Considered, not changing:** declined items with quote and the decision or reason.
- **Later:** deferred items, with out-of-scope ones shown as "possible change order" (client) or "save for later" (internal).

## After delivering

Set `stage: "fixlist"`. Offer to hand it over as a file (Markdown, or a `.docx` if the user wants one) and say: "Send me the next version when it's ready and I'll check it against this list."

The Fix-List is the answer to every "just rewrite it" request. When declining under rule 1, offer this list or the single item in question.

## Edge cases

- **Nothing accepted:** say so: "No changes this round." Offer close-out if approvals are in.
- **A requested change conflicts with a lock:** don't list it as a change. Raise it as a reversal first.
- **Visual items:** use region and page in line 1 ("Page 2 · Logo"), and describe the requested change ("logo larger, per brand minimum size").
- **Very long lists (30+ items):** keep the format; add a two-line summary by section at the top.
