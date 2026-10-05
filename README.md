# Ref, by unfayr.

Ref keeps the review fair. You make the calls.

Ref is a free Claude skill that runs the review and approval cycle for one marketing asset: an email, a landing page, a copy doc, an ad or any other visual. It handles the clerical work of collecting feedback, sorting it, spotting disagreements and tracking who approved what. The creative work and every decision stay with you.

## Three rules.

1. Ref never writes or rewrites the creative.
2. Ref never sends anything.
3. Ref shows its work.

Rule 3 means every label, conflict and verification quotes the reviewer's exact words, with a comment id and the spot in the asset. You can check any call in seconds.

## What it does.

Ref follows one asset through eight stages. You never have to name the stage. Say what's happening and Ref works out where you are.

1. **Setup.** You tell Ref who is reviewing, who has the final say on what, the deadline and what reviewers should look at. Ref creates the review file.
2. **Request.** Ref drafts a review request for each reviewer, tailored to what they review. You send them.
3. **Intake.** You say "feedback's in", or point Ref at the email thread, Slack channel or Drive doc. Ref splits feedback into single requests, attributes each one, pins it to a spot in the asset and removes duplicates.
4. **Triage.** Each comment gets a label: must fix, preference, question, out of scope, reversal of an earlier approval, or approval. Ref flags reviewers who disagree and notes who has authority on that area.
5. **Decisions.** Ref lists only what needs your call, with a recommendation for each, and records what you decide. It can draft a message to the reviewers involved. You send it.
6. **Fix-List.** One checklist of changes for whoever edits the asset. It says what to change. It does not write the change.
7. **Revision check.** When v2 arrives, Ref checks each Fix-List item against the new version, flags changes nobody asked for, and warns if an approved element was touched. Then a new round starts, or you close out.
8. **Sign-off.** Ref gives a verdict, `Approved` or `Not approved` with the blockers, and a summary you can keep as the record.

At any point you can ask where things stand, who hasn't replied yet, or whether the asset is approved. Ref can also draft a nudge for anyone who is late.

## Try it in 2 minutes.

There are two downloads on unfayr.com/ref and on the GitHub Releases page: the Ref skill zip and the sample kit zip. Unzip the sample kit (a `ref-sample-kit` folder). It has a made-up spring promo email for Northwind Coffee Co., a review file already set up for it, and feedback from four reviewers to paste in. The feedback includes a legal and brand disagreement, a request that is outside what was scoped, and a plain "looks good". The dates in the sample are illustrative, so Ref may point out that the deadline has passed; that is expected.

**In claude.ai or the Claude desktop app**

1. Install Ref (see [INSTALL.md](INSTALL.md)). Code execution must be on.
2. Start a new chat and attach `spring-promo-email.review.md` and `spring-promo-email.html` from the sample kit.
3. Open `sample-feedback.txt`, copy everything, and paste it into the chat with: "Feedback's in."
4. Read what Ref flags. Then say "What do I need to decide?" and make a call.
5. Ask for the Fix-List.

**In Claude Code**

1. Install Ref (see [INSTALL.md](INSTALL.md)).
2. Make a working folder with a `reviews` folder inside it. Copy `spring-promo-email.review.md` into `reviews`, and `spring-promo-email.html` into the working folder.
3. Start Claude Code in that folder and say: "Feedback's in." Then paste the contents of `sample-feedback.txt`.
4. Ask "What do I need to decide?", make a call, then ask for the Fix-List.

Your decisions are saved into the review file, so you can stop and pick it up later. In claude.ai and the desktop app, download the file at the end of the session and upload it at the start of the next chat.

## Install.

In Claude Code:

```
/plugin marketplace add timlaneseo-tech/unfayr-ref
/plugin install ref@unfayr
```

In claude.ai or the Claude desktop app, upload the skill zip under Settings, Capabilities, Skills. See [INSTALL.md](INSTALL.md) for every route and for the optional Gmail, Slack and Google Drive connectors.

## What it won't do.

- Write or rewrite headlines, copy, subject lines, CTAs or layouts. If you ask, Ref declines and offers the Fix-List instead.
- Send emails, Slack messages or anything else. Every message is a draft for you to send.
- Make your decisions. It recommends, and you decide.
- Review more than one asset in a file. A campaign with five assets is five reviews.
- Work without code execution. Ref uses small Python scripts to keep the review file valid.

## Privacy.

The review file holds reviewers' quotes and links to where they came from, not the full threads or documents. Ref reads only what you paste in or point it at. It never sends anything. The scripts that come with it work only on files on your machine or in your Claude session, use only the Python standard library and make no network calls.

## License.

Free to use, including for client work. No reselling, modifying or rebranding. See [LICENSE](LICENSE).

Built by Unfayr · unfayr.com
