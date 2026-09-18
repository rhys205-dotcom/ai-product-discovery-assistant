# Discovery Experiment — Sample Output

## Experiment

Can generative AI turn a small set of unstructured customer feedback into useful product discovery insights while preserving the evidence behind them?

This experiment uses the synthetic feedback in `sample-feedback.csv`.

The objective is not to ask AI what feature should be built. It is to test whether AI can accelerate the analytical work between raw customer feedback and product judgement.

---

## Proposed analysis flow

Customer feedback

↓  

Identify recurring themes

↓

Link themes to supporting evidence

↓

Generate problem statements

↓

Identify possible opportunities

↓

Human product review

---

# Example analysis

## Theme 1 — Payment status uncertainty

**Signal:** Strong

Several feedback items indicate uncertainty about whether a payment has completed, failed or is still processing.

### Evidence

Example customer feedback includes concerns such as:

- uncertainty after submitting a payment
- difficulty determining whether payment completed successfully
- lack of visibility while a payment is processing

### Problem statement

Customers need clearer confirmation of payment state because uncertainty can lead to repeated attempts, support contact and reduced confidence in the payment experience.

### Possible opportunity

Explore clearer payment-state messaging and proactive confirmation for successful, pending and failed transactions.

### AI confidence

**High**

Multiple feedback items appear to describe closely related behaviour.

### Human review

The theme appears credible, but frequency alone does not establish priority.

Product review would still need to consider factors such as transaction data, support volume, customer impact, strategic importance and implementation cost.

---

## Theme 2 — Reconciliation requires manual investigation

**Signal:** Moderate–Strong

Feedback suggests that users spend time reconciling transactions and investigating discrepancies across systems.

### Evidence

Examples include:

- difficulty matching payments with financial records
- manual investigation when amounts do not reconcile
- switching between systems to understand discrepancies

### Problem statement

Finance users need an efficient way to understand discrepancies because manual reconciliation increases operational effort and makes errors harder to diagnose.

### Possible opportunity

Explore better transaction matching, discrepancy explanations and links between payment activity and accounting records.

### AI confidence

**Medium–High**

The underlying problem appears consistent, although individual feedback may describe different parts of the reconciliation workflow.

### Human review

Further discovery would be required to determine whether these are manifestations of one problem or several related problems.

---

## Theme 3 — Reporting does not answer the user's immediate question

**Signal:** Moderate

Some feedback suggests that users can access data but still struggle to answer operational questions quickly.

### Problem statement

Users need reporting that reflects the decisions they are trying to make rather than simply presenting available data.

### Possible opportunity

Investigate the most common questions users are trying to answer and design reporting around those jobs rather than existing data structures.

### AI confidence

**Medium**

The evidence may represent several different reporting needs.

### Human review

Do not consolidate these into a single product requirement without additional research.

---

# What the AI should NOT conclude

The analysis above does **not** establish that:

- payment status should be the next roadmap priority
- reconciliation requires a new feature
- reporting needs a redesign
- the most frequently mentioned problem has the highest business value
- an AI-generated opportunity is necessarily the correct solution

Those decisions require additional evidence and product judgement.

---

# Evaluation

A useful AI discovery assistant should be judged on more than whether its output sounds convincing.

| Dimension | Question |
|---|---|
| Evidence traceability | Can every theme be traced back to customer evidence? |
| Theme quality | Does the grouping represent genuinely related problems? |
| Unsupported inference | Has the AI introduced claims not supported by the feedback? |
| Usefulness | Does the output reduce the PM's analytical workload? |
| Uncertainty | Does the system identify weak or ambiguous evidence? |
| Human control | Is it clear where AI analysis ends and product judgement begins? |

---

# Initial learning

Generative AI appears useful for accelerating the first pass through qualitative feedback, particularly theme identification and summarisation.

The larger product risk is not whether AI can generate plausible insights.

It is whether those insights remain **traceable, challengeable and useful for human decision-making**.

That becomes the central design principle for the next iteration.
