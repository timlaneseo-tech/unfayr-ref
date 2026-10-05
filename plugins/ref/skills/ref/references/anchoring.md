# Anchoring

**Purpose:** pin every comment to the exact spot in the asset it is about, so the user and the writer can find it in seconds, and so later versions can be checked against it.

## Inputs

- The comment's exact words and any location the source gives (a Doc comment's highlighted text, a PDF annotation's page).
- The version the comment refers to.

## Text, email and pages

- `section`: the nearest heading, or the email part (`Subject`, `Preheader`, `Body`, `CTA`, `Footer`), or the page section (`Hero`, `Pricing`, `FAQ`). Use the asset's own heading text where there is one.
- `excerpt`: a short verbatim excerpt from the asset, 3 to 12 words, copied exactly. Choose words that will still be recognizable after edits. Excerpts survive edits better than line numbers, so never use line numbers.
- If the comment quotes the asset ("change 'act now'"), that quote is the excerpt.
- A comment about the whole asset ("too long overall", "tone feels off") gets `section: "General"` and no excerpt.

## Visuals (images and PDFs)

- `section`: a named region. Use these names when they fit: Headline, Subhead, Hero image, CTA, Logo, Body, Footer, Disclaimer. Use the asset's own visible label for anything else ("Price badge", "QR code").
- `page`: the page number for PDFs (1-based). Leave it out for single images.
- `region`: position words ("top left, over the photo") only as a fallback, when no named region fits or two elements share a name.
- `excerpt`: any visible text in that region, verbatim, if there is some.

Look at the image to check that the named region exists and holds what the comment describes. If it doesn't (a comment about "the blue button" when the CTA is green), say so and ask.

## When a comment can't be anchored

"The thing we discussed", "fix that bit", "same as last time": Ref says it can't place the comment and asks the user where it points. Never guess. Record it with `section: "Unanchored"`, label `question`, status `open`. Re-anchor it when the user answers.

Partial anchors are fine: "the second paragraph" is anchorable if the asset has a clear second paragraph. Quote its first words as the excerpt.

## Example

Asset (email body): "Spring is here. Save 20% on every plan until April 30. Guaranteed savings or your money back."

| Comment | Anchor |
|---|---|
| Lee: "Guaranteed needs the terms link." | section `Body`, excerpt `Guaranteed savings or your money back` |
| Dana: "Subject feels flat." | section `Subject`, excerpt = the subject line |
| Sam: "Can we do the thing we talked about with the footer?" | section `Footer` is clear, but "the thing we talked about" isn't. Anchor to `Footer`, label `question`, and ask the user what the change is. |
| Priya (PDF, p2): "Logo too small" | section `Logo`, page `2` |
