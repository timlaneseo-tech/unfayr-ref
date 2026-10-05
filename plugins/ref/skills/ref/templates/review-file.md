<!--
Reference skeleton only. Never copy this file or write a review file by hand.
The script (scripts/review_file.py) is the source of truth: create files with "new" and change them only
with "dump", then "save" (or "render" after a hand edit). This example shows what the script
produces for an email in round 2 with one open conflict, one lock and a closed round 1.
Everything above the data marker is rendered from the data block on every save.
-->
# Spring Promo — review

Stage: decisions · Round: 2 · Deadline: 2026-10-09 · Overall approver: Dana

## Reviewers

| Name | Role | Client or internal | Areas | Final say on |
| --- | --- | --- | --- | --- |
| Dana | VP Marketing | client | messaging, offer | messaging |
| Lee | Counsel | client | claims, disclaimers | claims, disclaimers |
| Sam | Designer | internal | visual |  |

## Open items

### Hero

- [R2-01] Lee: "We can't say 'guaranteed savings' without the terms link." — must fix
- [R2-02] Dana: "Keep the hero clean, no links up there." — preference

### Body

- [R2-03] Dana: "Could we add a pricing table?" — possible change order

## Decisions to make

- C1 (claims): R2-01, R2-02 · final say: Lee · suggested: Follow Lee: claims need the terms link.
  - [R2-01] Lee: "We can't say 'guaranteed savings' without the terms link." — must fix
  - [R2-02] Dana: "Keep the hero clean, no links up there." — preference

## Decided this round

Nothing decided yet this round.

## Locked

- Subject line (Subject): approved by Dana, round 1, version 1

## Approvals

No approvals yet.

## History

<details><summary>Round 1 — 2 comments, 1 decision</summary>

- [R1-01] Dana: "Subject line is great. Lock it." — approval (verified)
- [R1-02] Lee: "The price says $49 but the rate card says $59." — must fix (verified)
- Decision D1: Price — Correct to $59

</details>

Built by Unfayr · unfayr.com

<!-- ref:data -->
```json
{
  "schema": "ref/1",
  "project": {
    "id": "spring-promo",
    "asset_name": "Spring Promo",
    "asset_type": "email",
    "created": "2026-10-01",
    "deadline": "2026-10-09",
    "overall_approver": "dana",
    "stage": "decisions",
    "current_round": 2,
    "round_scope": "Copy and offer only; layout is final."
  },
  "reviewers": [
    {
      "id": "dana",
      "name": "Dana",
      "role": "VP Marketing",
      "kind": "client",
      "areas": [
        "messaging",
        "offer"
      ],
      "authority": [
        "messaging"
      ]
    },
    {
      "id": "lee",
      "name": "Lee",
      "role": "Counsel",
      "kind": "client",
      "areas": [
        "claims",
        "disclaimers"
      ],
      "authority": [
        "claims",
        "disclaimers"
      ]
    },
    {
      "id": "sam",
      "name": "Sam",
      "role": "Designer",
      "kind": "internal",
      "areas": [
        "visual"
      ],
      "authority": []
    }
  ],
  "versions": [
    {
      "v": 1,
      "date": "2026-10-01",
      "source": "spring-promo-v1.html",
      "fingerprint": "3f9a1c0b7d2e",
      "change_summary": "First draft"
    },
    {
      "v": 2,
      "date": "2026-10-05",
      "source": "spring-promo-v2.html",
      "fingerprint": "a71e44c9d018",
      "change_summary": "Fix-List R1 applied"
    }
  ],
  "rounds": [
    {
      "n": 1,
      "version": 1,
      "requests": [
        {
          "reviewer_id": "dana",
          "drafted": "2026-10-01",
          "sent": "2026-10-01"
        },
        {
          "reviewer_id": "lee",
          "drafted": "2026-10-01",
          "sent": "2026-10-01"
        }
      ],
      "responses": [
        {
          "reviewer_id": "dana",
          "received": "2026-10-02"
        },
        {
          "reviewer_id": "lee",
          "received": "2026-10-02"
        }
      ]
    },
    {
      "n": 2,
      "version": 2,
      "requests": [
        {
          "reviewer_id": "dana",
          "drafted": "2026-10-05",
          "sent": "2026-10-05"
        },
        {
          "reviewer_id": "lee",
          "drafted": "2026-10-05",
          "sent": "2026-10-05"
        },
        {
          "reviewer_id": "sam",
          "drafted": "2026-10-05"
        }
      ],
      "responses": [
        {
          "reviewer_id": "dana",
          "received": "2026-10-06"
        },
        {
          "reviewer_id": "lee",
          "received": "2026-10-06"
        }
      ]
    }
  ],
  "comments": [
    {
      "id": "R1-01",
      "round": 1,
      "reviewer_id": "dana",
      "quote": "Subject line is great. Lock it.",
      "source": "email",
      "secondhand": false,
      "anchor": {
        "section": "Subject",
        "excerpt": "Spring is here. So are the savings."
      },
      "label": "approval",
      "label_overridden_by_user": false,
      "status": "verified"
    },
    {
      "id": "R1-02",
      "round": 1,
      "reviewer_id": "lee",
      "quote": "The price says $49 but the rate card says $59.",
      "source": "email",
      "secondhand": false,
      "anchor": {
        "section": "Body",
        "excerpt": "Plans from $49"
      },
      "label": "must_fix",
      "label_overridden_by_user": false,
      "status": "verified",
      "decision_id": "D1"
    },
    {
      "id": "R2-01",
      "round": 2,
      "reviewer_id": "lee",
      "quote": "We can't say 'guaranteed savings' without the terms link.",
      "source": "email",
      "source_ref": "Gmail: Re: Spring Promo v2, 2026-10-06",
      "secondhand": false,
      "anchor": {
        "section": "Hero",
        "excerpt": "guaranteed savings this spring"
      },
      "label": "must_fix",
      "label_overridden_by_user": false,
      "conflict_id": "C1",
      "status": "open"
    },
    {
      "id": "R2-02",
      "round": 2,
      "reviewer_id": "dana",
      "quote": "Keep the hero clean, no links up there.",
      "source": "slack",
      "secondhand": false,
      "anchor": {
        "section": "Hero",
        "excerpt": "guaranteed savings this spring"
      },
      "label": "preference",
      "label_overridden_by_user": false,
      "conflict_id": "C1",
      "status": "open"
    },
    {
      "id": "R2-03",
      "round": 2,
      "reviewer_id": "dana",
      "quote": "Could we add a pricing table?",
      "source": "slack",
      "secondhand": false,
      "anchor": {
        "section": "Body"
      },
      "label": "out_of_scope",
      "label_overridden_by_user": false,
      "status": "open"
    }
  ],
  "conflicts": [
    {
      "id": "C1",
      "comment_ids": [
        "R2-01",
        "R2-02"
      ],
      "area": "claims",
      "authority_holder": "lee",
      "recommendation": "Follow Lee: claims need the terms link.",
      "status": "open"
    }
  ],
  "decisions": [
    {
      "id": "D1",
      "round": 1,
      "topic": "Price",
      "choice": "Correct to $59",
      "date": "2026-10-02",
      "settles": [
        "R1-02"
      ]
    }
  ],
  "locks": [
    {
      "id": "L1",
      "element": "Subject line",
      "anchor": {
        "section": "Subject",
        "excerpt": "Spring is here. So are the savings."
      },
      "approved_by": "dana",
      "round": 1,
      "version": 1
    }
  ],
  "approvals": [],
  "meta": {
    "rendered_hash": "493c9e624e24fc55f5240ae5ade26e2f1dd3708366510b5b817fd31d1a228113",
    "ref_version": "1.0.0",
    "reconstructed": false
  }
}
```
