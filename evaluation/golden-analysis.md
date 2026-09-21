# Human Reference Analysis — v1.0

## Purpose and source of truth

This document is the readable explanation of the human reference used to evaluate the 40-record synthetic feedback dataset.

The machine-readable [`reference-analysis.json`](reference-analysis.json) is the scoring source of truth. It was created before the controlled Gemini benchmark. This narrative mirrors its three themes, evidence sets, qualifying evidence and deliberate distractors.

The reference is a documented human judgement rather than objective ground truth. Theme boundaries can overlap, and future reviewers should record disagreement rather than silently changing the baseline.

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

This theme overlaps with payment-status visibility but represents a distinct need for history and traceability. A useful analysis may recognise the relationship while keeping the customer problem separately visible.

---

## Deliberate distractors

The dataset contains isolated requests that should not become major themes:

- `F009` — dark mode
- `F018` — isolated preference not part of a recurring problem
- `F024` — additional dashboard colours
- `F030` — receipt logo customisation
- `F039` — larger font size

A model should not present these as significant recurring customer problems based on this dataset.

---

## Acceptable variation

The model does not need to reproduce the exact wording used here. A useful analysis may use different labels or problem-statement wording, provided that it:

- identifies materially distinct customer problems;
- cites evidence that genuinely supports the mapped theme;
- does not elevate isolated distractors;
- preserves important qualifying evidence;
- separates customer evidence from interpretation and proposed action.

---

## Evaluation dimensions

| Measure | Question |
|---|---|
| Theme coverage | How many of the three reference themes were identified? |
| Citation validity | Do cited feedback IDs exist in the dataset? |
| Evidence precision | Do valid citations support the matched theme? |
| Reference evidence coverage | How much of the documented reference evidence was found? |
| Contradiction coverage | Was expected qualifying evidence surfaced? |
| Distractor citations | Were isolated requests incorrectly promoted as core evidence? |

Human mapping remains explicit because deciding whether differently worded themes represent the same underlying customer problem is a judgement, not an objective string-matching task.
