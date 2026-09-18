# Discovery Experiment — v0.2

## Experiment

Can generative AI turn unstructured customer feedback into useful product discovery insights while preserving traceability to the underlying evidence?

This experiment uses the 40 synthetic feedback records contained in `data/sample-feedback.csv`.

The objective is not to ask AI what should be built.

The objective is to test whether AI can accelerate the analytical work between:

**Customer evidence → Interpretation → Product opportunity → Human judgement**

---

# Finding 1 — Payment status and failure visibility

**Evidence strength:** Strong

Users repeatedly describe difficulty understanding when payments fail, remain pending or have successfully completed.

## Supporting evidence

`F003` `F004` `F008` `F010` `F016` `F022` `F023` `F027` `F028` `F034` `F037` `F040`

Examples include:

- `F003` — Administrator wants the dashboard to surface failed payments.
- `F010` — Finance user discovered a failed payment three days later during reconciliation.
- `F022` — Administrator was unsure what to tell a customer because payment status had not updated.
- `F028` — Team discovered a failed payment only after the customer contacted them.
- `F034` — Administrator wants failed payments to explain the reason for failure.

## Interpretation

The evidence suggests an underlying visibility problem rather than simply demand for a notification feature.

Users need to understand the state of a payment and know when intervention is required.

## Problem statement

Operational users need clearer visibility of payment state because failures and delays can otherwise remain undiscovered until reconciliation or customer contact.

## Potential opportunity

Explore proactive exception notifications and clearer successful, pending and failed payment states.

## Human review

**Accept theme.**

There is repeated evidence across Support, Interview and Survey sources and across several personas.

However, the evidence does not yet establish which solution would provide the greatest value.

---

# Finding 2 — Manual reconciliation and exception handling

**Evidence strength:** Strong

Finance users repeatedly describe manual work associated with reconciling payments and investigating discrepancies.

## Supporting evidence

`F001` `F002` `F005` `F007` `F012` `F014` `F017` `F019` `F021` `F025` `F026` `F029` `F031` `F035` `F038`

Examples include:

- `F001` — Month-end requires exporting and manually reconciling payment reports.
- `F002` — Finance user spends approximately two hours checking payments against bank records.
- `F014` — User compares the platform report with accounting software line by line.
- `F017` — User would prefer to review exceptions rather than every successful transaction.
- `F038` — User believes seeing unmatched transactions in one place would remove much of the manual work.

## Interpretation

The underlying customer problem is not necessarily a lack of automatic reconciliation.

The stronger signal is that users spend too much time manually identifying the transactions that require attention.

## Contradictory evidence

The dataset contains an important tension.

`F021` says:

> "An automatic reconciliation feature would save me a lot of time."

However:

`F026` says:

> "I don't necessarily want full automatic reconciliation. I'd be happier if the system just highlighted the transactions that don't match."

And `F033` states that financial adjustments should remain subject to human checking and approval.

## Product interpretation

It would therefore be inappropriate to conclude:

> Customers want reconciliation to be fully automated.

A more evidence-faithful interpretation is:

> Customers want to reduce manual reconciliation effort while retaining visibility and control over exceptions.

## Potential opportunity

Explore exception-based reconciliation that automatically identifies potentially unmatched transactions while leaving financial decisions with the user.

## Human review

**Accept theme, modify AI interpretation.**

The customer problem is strongly supported.

The proposed solution must preserve human control rather than assuming full automation is desirable.

---

# Candidate Finding 3 — Reporting does not answer user questions

**Initial evidence strength:** Limited

An initial analysis suggested that users struggle to answer operational questions using existing reporting.

## Human evidence review

Reviewing the underlying dataset found insufficient recurring evidence to support this as a distinct customer problem.

Some feedback references reporting, but this does not establish a consistent theme across the dataset.

## Decision

**Reject theme.**

This finding should not progress into a product opportunity without additional evidence.

## Learning

This is an example of a plausible AI-generated interpretation that sounds reasonable but is not sufficiently supported by the source data.

Requiring evidence IDs makes the weakness easier for a human reviewer to identify.

---

# Noise and isolated requests

The dataset also deliberately contains isolated feature requests including:

- `F009` — Dark mode
- `F024` — Additional dashboard colours
- `F030` — Receipt logo customisation
- `F039` — Larger font size

These may be legitimate customer requests.

However, the current dataset does not provide enough evidence to treat them as significant recurring themes.

A useful discovery assistant should avoid turning every individual feature request into a product opportunity.

---

# Evaluation

| Dimension | Result | Observation |
|---|---|---|
| Evidence traceability | Good | Findings can be checked against identifiable feedback records |
| Theme quality | Good | Two strong recurring problems emerge |
| Contradictory evidence | Important | Automation preference is not consistent |
| Unsupported inference | Identified | Reporting theme was rejected during human review |
| Noise handling | Important | Isolated feature requests should not become major themes |
| Human oversight | Required | AI interpretation required modification and rejection |

---

# Key learning

The experiment suggests that the value of generative AI in product discovery is not simply its ability to summarise large amounts of text.

The more important product challenge is making its analysis:

- traceable
- challengeable
- evidence-based
- explicit about uncertainty
- subject to human judgement

The reconciliation example demonstrates why this matters.

An AI system could reasonably observe repeated reconciliation complaints and recommend automation.

Closer inspection of the evidence reveals a more nuanced customer need:

**reduce manual effort without removing human control.**

That distinction can materially change the product that gets built.

---

## Next experiment

v0.3 will explore whether this evidence-linked analysis can be generated consistently from the source dataset rather than manually demonstrated as a worked example.
