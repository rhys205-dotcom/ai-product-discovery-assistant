# Human Reference Baseline — v1.0

## Purpose

This document is the readable explanation of the human reference used to evaluate the 40-record synthetic feedback dataset.

The machine-readable [`reference-analysis.json`](reference-analysis.json) is the repeatable scoring baseline created before the controlled Gemini benchmark. It is **not** objective ground truth. Theme boundaries can overlap, and a different practitioner may organise the same evidence differently while still producing a useful analysis.

An independent blind practitioner review is now explicitly required before using this reference to justify further optimisation. See [`independent-reference-review.md`](independent-reference-review.md). The existing v1.0 reference will not be silently rewritten after that review; agreements and disagreements will be recorded first.

---

## T01 — Manual reconciliation and exception handling

**Expected strength:** Strong

### Core customer problem

Finance users spend substantial time reconciling payment data with bank and accounting records, while exceptions, refunds and shared investigations make discrepancies difficult to resolve.

### Required evidence

`F001` `F002` `F005` `F007` `F012` `F014` `F017` `F019` `F021` `F025` `F026` `F029` `F031` `F033` `F035` `F038`

**Minimum support:** Four records

### Qualifying evidence

`F006` `F026` `F029` `F033` `F036`

The evidence supports reducing manual reconciliation effort. It does **not** support assuming that users want fully autonomous reconciliation. A strong analysis should preserve review and approval while helping users identify exceptions.

---

## T02 — Delayed visibility of failed or pending payments

**Expected strength:** Strong

### Core customer problem

Administrators and managers often discover failed or pending payments late, sometimes only after a customer contacts them, and need clearer status, reasons and proactive alerts.

### Required evidence

`F003` `F004` `F008` `F010` `F011` `F016` `F020` `F022` `F023` `F027` `F028` `F032` `F034` `F040`

**Minimum support:** Four records

### Qualifying evidence

`F006` `F023` `F036`

A strong analysis should identify the underlying need as actionable payment-state visibility rather than simply repeat a requested solution such as sending notifications. The evidence does not support claiming that all payment-status information is unclear.

---

## T03 — Payment communication and audit history

**Expected strength:** Secondary but recurring

### Core customer problem

Teams need a clearer record of payment events and customer communications to avoid duplicate reminders and answer disputes or status questions consistently.

### Required evidence

`F008` `F013` `F022` `F032` `F037`

**Minimum support:** Three records

### Qualifying evidence

`F023`

This proposed theme overlaps materially with payment-status visibility. `F013` and `F037` are the clearest evidence for a communication/history need; several other records can plausibly remain inside the broader payment-status problem. The independent review should therefore test whether keeping this distinction separately visible changes a useful product investigation or decision.

---

## Deliberate distractors

The dataset contains isolated requests that should not become major themes solely because they appear in the data:

- `F009` — dark mode
- `F018` — search speed
- `F024` — additional dashboard colours
- `F030` — receipt logo customisation
- `F039` — larger font size

These records may still represent valid individual needs. The reference only says that this dataset does not establish them as recurring problems.

---

## Acceptable variation

The model does not need to reproduce the exact wording or exactly three top-level themes. A useful analysis may use different labels, subthemes or problem-statement wording, provided that it:

- identifies materially useful customer problems;
- cites evidence that genuinely supports the mapped finding;
- does not elevate isolated records into broad claims without qualification;
- preserves important qualifying evidence;
- separates customer evidence from interpretation and proposed action.

Theme count is not itself a quality target.

---

## Evaluation dimensions

| Measure | Question |
|---|---|
| Theme coverage | How many reference theme distinctions were represented? |
| Citation validity | Do cited feedback IDs exist in the dataset? |
| Evidence precision | Does each citation support the finding it is attached to? |
| Reference evidence coverage | How much of the documented reference evidence was represented for the mapped theme? |
| Qualification coverage | Was documented qualifying evidence surfaced? |
| Qualification precision | Were records labelled as qualifying actually relevant to that mapped theme? |
| Unmatched findings | Did the model produce findings that require human assessment outside the current reference? |
| Distractor citations | Were isolated requests incorrectly used as core evidence for a broad finding? |

Human mapping remains explicit because deciding whether differently worded findings represent the same underlying customer problem is a judgement, not an objective string-matching task.
