# Golden Analysis — v0.2 Reference

## Purpose

This document defines a human-reviewed reference analysis for the synthetic customer feedback dataset.

It provides a baseline against which future AI-generated analyses can be evaluated.

The reference is deliberately created before automated model evaluation so that the expected result is not changed to match whatever the model produces.

---

# Expected Theme 1 — Manual reconciliation and exception handling

**Expected strength:** Strong

## Core customer problem

Finance users spend significant time manually reconciling payment activity and identifying discrepancies.

## Key evidence

`F001` `F002` `F005` `F007` `F012` `F014` `F017` `F019` `F021` `F025` `F026` `F029` `F031` `F035` `F038`

## Important nuance

The evidence supports reducing manual reconciliation effort.

It does **not** support assuming that users want fully autonomous reconciliation.

`F026` explicitly prefers exception highlighting to full automation.

`F033` provides additional evidence that users want human control over financial adjustments.

## Expected interpretation

A strong analysis should identify an opportunity around:

**exception-based reconciliation and discrepancy identification while preserving human oversight.**

---

# Expected Theme 2 — Payment failure and status visibility

**Expected strength:** Strong

## Core customer problem

Operational users do not always know when payments fail, remain pending or require intervention.

## Key evidence

`F003` `F004` `F008` `F010` `F016` `F022` `F023` `F027` `F028` `F034` `F037` `F040`

## Expected interpretation

A strong analysis should identify the underlying need as **payment-state visibility**, rather than simply repeating the requested solution of "send notifications."

Possible opportunities may include:

- proactive exception alerts
- clearer payment states
- failure reasons
- better payment history

The analysis should not assume which solution should be built.

---

# Secondary Signal — Customer contact caused by payment uncertainty

## Relevant evidence

`F008` `F020` `F028` `F032`

There is evidence that unclear payment status can contribute to customer contact.

This may be treated as:

- a consequence of the payment-status theme, or
- a secondary theme

Either interpretation can be acceptable if supported by evidence.

It should not automatically be treated as a separate roadmap opportunity.

---

# Signals that should NOT become major themes

The following requests are deliberately included as noise or isolated preferences:

`F009` — Dark mode  
`F024` — Additional dashboard colours  
`F030` — Receipt logo customisation  
`F039` — Larger font size

A model should not present these as significant recurring customer problems based on this dataset.

---

# Acceptable variation

The AI does not need to reproduce the exact wording or exact grouping used in this document.

A useful analysis may:

- combine closely related themes
- identify legitimate secondary patterns
- use different problem-statement wording
- propose different opportunities

The important requirement is that conclusions remain supported by the source evidence.

---

# Evaluation criteria

Future AI runs will be assessed against five dimensions.

## 1. Theme coverage

Did the model identify the two dominant customer problems?

## 2. Evidence precision

Do the cited feedback records genuinely support the theme?

## 3. Evidence recall

Did the model identify a reasonable proportion of the relevant evidence?

## 4. Unsupported themes

Did the model elevate isolated or weak signals into major findings?

## 5. Nuance

Did the model recognise that reducing manual reconciliation does not necessarily mean removing human control?

---

# Initial scoring approach

Each AI run can be recorded using:

| Measure | Result |
|---|---|
| Reconciliation theme identified | Yes / Partial / No |
| Payment-status theme identified | Yes / Partial / No |
| Evidence references valid | Percentage |
| Major unsupported themes | Count |
| Isolated requests incorrectly promoted | Count |
| Automation/control nuance recognised | Yes / Partial / No |

This scoring approach is intentionally simple for the first experiment.

The objective is to establish a repeatable evaluation baseline before introducing more sophisticated evaluation techniques.
