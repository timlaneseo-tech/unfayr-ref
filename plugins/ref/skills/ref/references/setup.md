# Setup

**Purpose:** create the review file for one asset, with everything later stages need: who reviews, who has the final say on what, the deadline, and what this round covers.

## Inputs to collect

1. **The asset:** a file, a paste or a URL. Note the asset type: `copy` (blog posts, page copy, scripts), `email` (subject, preheader, body, CTAs), `page` (landing or web page, URL or HTML), `visual` (ads, social graphics, one-pagers, brochures as images or PDFs). Video is not supported in v1; say so.
2. **Reviewers:** for each, name, role, `client` or `internal`, the areas they review, and the areas where they have the final say. Contact details only if the user offers them.
3. **Deadline** for the review (a date, or none).
4. **Overall approver:** the one person whose approval means the asset is done.
5. **Round scope:** one sentence on what reviewers should look at this round ("Copy and offer only; layout is final").

Ask for what is missing in one message, not one question at a time. If the user gives most of it in their first message, confirm and fill gaps. Don't ask for things you can infer (an email asset is `email`).

## Authority defaults

Propose these, show them in a short table, and let the user edit before saving:

- Legal or Compliance: final say on claims, pricing terms, and disclaimers.
- Brand: final say on logo, color, type and voice.
- The owner of an area (product for product facts, the regional lead for local offers): final say on their area.
- The overall approver: breaks ties and owns anything unassigned.
- **Client mode:** the client's designated approver is the overall approver for client-facing decisions. If the user is an agency or freelancer, the client's approver usually signs off; the user's own team has authority on craft areas only if the user says so.

Areas are short nouns used consistently later: "claims", "disclaimers", "brand", "visual", "messaging", "offer", "product facts", "accessibility". The same word must appear in `areas` or `authority` and in conflicts.

Required approvals at close-out are the overall approver plus anyone with a non-empty `authority` list. Say this at setup so the user can adjust authority if someone shouldn't have to sign off.

## Steps

1. Collect the inputs above.
2. Create the file: in Claude Code, make the `reviews` folder if needed, then `python scripts/review_file.py new reviews/<asset-slug>.review.md --asset "<Asset name>" --type <type>`. In claude.ai, create it in the working folder.
3. `dump`, then fill in: `project.deadline`, `project.overall_approver`, `project.round_scope`, the `reviewers`, version 1 in `versions` (with fingerprint and "First draft" or the user's words), round 1 in `rounds` (`n: 1`, `version: 1`, empty `requests` and `responses`), `current_round: 1`, `stage: "request"`.
4. `save`. Show the user a compact summary: reviewers with their final-say areas, deadline, approver, scope.
5. Offer the next step: "Want me to draft the review requests?"

## Edge cases

- **A review file already exists for this asset:** don't create a second one. Ask whether to continue it or start over; starting over means a new file name (`new` refuses to overwrite).
- **More than six reviewers:** set it up anyway, but say plainly that every extra reviewer adds conflicts, and ask whether some only need to see the final version (they can be left out of round 1 and added later).
- **Two people claim the same area:** ask who has the final say. If the user doesn't know, the overall approver owns it.
- **No overall approver:** ask once. If there truly is none, leave it `null` and note that close-out can't reach `Approved` without one.
- **Asset arrives later:** set up anyway; the version is added when the asset arrives, before requests go out.
- **Several assets at once:** one review file per asset. Offer to set up each separately.

## Example

> **User:** Start a review for the Spring Promo email. Dana (client, VP Marketing) approves. Lee is their counsel. Sam on our side does design. Due Friday.
>
> **Ref:** Set up. Here's who has the final say. Change anything that's wrong.
>
> | Reviewer | Client or internal | Reviews | Final say on |
> |---|---|---|---|
> | Dana, VP Marketing | client | messaging, offer | overall approver |
> | Lee, Counsel | client | claims, disclaimers | claims, disclaimers |
> | Sam, Designer | internal | visual | none |
>
> Deadline Friday 2026-10-09. What should reviewers look at this round: everything, or copy only?
