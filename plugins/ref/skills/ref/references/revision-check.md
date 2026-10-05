# Revision check

**Purpose:** when a new version arrives, check it against the Fix-List item by item, catch anything that changed without being asked for, and confirm locked elements are untouched. Every finding comes with evidence.

## Inputs

- The new version (file, paste or URL) and the previous version.
- The Fix-List items: comments with status `accepted` (this round and carried over), excluding comments labeled `approval` or `question`.
- `locks`.

## Steps

1. **Record the version.** Add `{ v, date, source, fingerprint, change_summary }`. If the fingerprint matches the previous version, say the file looks identical and ask whether the right file was sent before going further.
2. **Mechanical diff (text and HTML).** Run `python scripts/compare_versions.py <previous> <new>` (add `--kind html` if needed). Read it as raw material: group entries that are one change (a modified sentence plus a stray `[href]` entry is usually one edit), and ignore whitespace-only noise.
3. **Visual comparison (images and PDFs).** Compare the two versions region by region, page by page. Describe each difference by region. State a confidence level for each finding (high, medium, low) and say what limits it ("low: the new export is lower resolution").
4. **Verify each Fix-List item.** One verdict per item:
   - **done:** the change is there. Evidence: before and after excerpts (or a region description). Set `verified`.
   - **partly done:** some of the request is met. Say exactly what's missing. Leave it `accepted`; it carries to the next Fix-List.
   - **not done:** no change at the anchor. Leave it `accepted`.
   - **can't tell:** the evidence is ambiguous (the anchor text is gone, the change is subjective, the image is unclear). Say why and ask the user. If the user says it's done, set `done`, not `verified`.
   Judge against the reviewer's request, not Ref's taste. "Shorter headline" is done if it's shorter.
5. **Unrequested changes.** Every difference not explained by a Fix-List item is an unrequested change. List each with before and after. Not every one is a problem (a typo fix), but the user decides, and reviewers may need to know.
6. **Locks.** Check each locked element at its anchor. If one changed, flag it at the top of the report, before anything else: "Flag on the play: the subject line (L1, approved by Dana in R1) changed." with before and after.
7. **Close the round and offer what's next.** Update statuses, set `stage: "revision"`, then offer:
   - start the next round: `current_round` + 1, a new `rounds` entry with the new version, `stage: "request"`; or
   - close-out (references/closeout.md), if nothing blocks approval.
   The user picks. Save either way.

## Output

```
v2 checked against 9 Fix-List items. 7 done, 1 partly done, 1 not done.

Locks: untouched.   (or the flag, first)

Done
- Hero · terms link added (R2-03). Before: "guaranteed savings this spring" After: "guaranteed savings this spring [terms]"
Partly done
- Pricing · price corrected to $59, but the annual price still says $490 (R2-07 asked for both).
Not done
- Footer · unsubscribe link still missing (R2-09).
Unrequested changes
- CTA · "Get started" became "Start free trial". Nobody asked for this.
```

Then the offer of the next round or close-out.

## Worked example

Fix-List R2 had: (a) add terms link to the hero claim, (b) shorten the subhead, (c) fix the $49 price to $59. `compare_versions.py` shows: hero sentence modified plus a stray `[https://example.com/terms]` entry; subhead modified from 14 to 9 words; the CTA changed from "Get started" to "Start free trial"; the price line unchanged.

Ref's read: (a) done, one change despite two diff entries. (b) done. (c) not done, still $49. CTA: an unrequested change, flagged for the user, who may need to tell Dana since the CTA is client-facing.
