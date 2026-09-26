# Evaluation results

## Historical Gemini benchmark — 20 September 2026

Three independent analyses were run against the unchanged 40-record synthetic feedback dataset using `gemini-3.5-flash`, prompt version `v1`.

Each generated theme was manually mapped to the documented human reference before scoring. The stored run files contain the generated findings plus the added `theme_id` annotation used for scoring. All three runs are reported; no run was excluded or selected as the preferred result.

This experiment predates the current OpenAI-backed application configuration. It is retained as historical evidence rather than used as the direct baseline for future prompt comparisons.

## Original published scores — scorer v1

These numbers are preserved because they were the scores published at the time of the experiment.

| Metric | Run 1 | Run 2 | Run 3 | Mean |
|---|---:|---:|---:|---:|
| Theme coverage | 66.7% | 66.7% | 66.7% | 66.7% |
| Evidence precision | 96.4% | 93.5% | 96.7% | 95.5% |
| Reference evidence coverage | 84.4% | 90.6% | 90.6% | 88.5% |
| Citation validity | 100% | 100% | 100% | 100% |
| Contradiction coverage | 83.3% | 83.3% | 100% | 88.9% |

Those figures reproduce for the stored runs under scorer v1. They are not withdrawn, but later review identified mechanical blind spots in what the scorer counted.

## Relationship-aware re-score — scorer v2

Scorer v2 evaluates evidence at the `(finding, citation)` relationship level, keeps unmatched findings visible, checks citations from every generated finding, preserves duplicate mappings rather than overwriting them, and adds qualification precision.

Using the same stored human mappings, the v2 re-score is:

| Metric | Run 1 | Run 2 | Run 3 | Mean |
|---|---:|---:|---:|---:|
| Theme coverage | 66.7% | 66.7% | 66.7% | 66.7% |
| Evidence precision | 96.4% | 93.5% | 96.7% | 95.5% |
| Reference evidence coverage | 77.1% | 82.9% | 82.9% | 81.0% |
| Citation validity | 100% | 100% | 100% | 100% |
| Qualification coverage | 66.7% | 55.6% | 88.9% | 70.4% |
| Qualification precision | 85.7% | 83.3% | 88.9% | 86.0% |
| Unmatched findings | 0 | 0 | 0 | — |
| Duplicate mapped themes | 0 | 0 | 0 | — |

The lower relationship-aware coverage figures are not evidence that the model changed; the model outputs are identical. The denominator now preserves theme-specific evidence relationships instead of flattening overlapping IDs across reference themes.

## What the benchmark establishes

All three runs represented the two dominant reference distinctions:

- `T01` — manual reconciliation and exception handling;
- `T02` — delayed visibility of failed or pending payments.

None was mapped to `T03` — payment communication and audit history. Some records associated with that reference distinction, particularly `F037`, were included inside the broader payment-status finding instead.

Across the stored runs:

- every cited feedback ID existed in the source dataset;
- no deliberate distractor was cited as core evidence;
- both represented reference themes met the minimum support threshold;
- core evidence precision remained above 93%.

## What the benchmark does **not** establish

The three-theme reference is a documented human analysis, not objective ground truth. The fact that the model did not produce a separately mapped `T03` finding does **not** by itself prove that a two-theme analysis is worse for a product practitioner.

`F013` and `F037` provide relatively direct evidence for communication/history concerns. Other records used in `T03`, including `F008`, `F022` and `F032`, can also plausibly remain inside the broader payment-status problem. An independent blind practitioner review is therefore required before optimising the model specifically to reproduce this theme boundary.

The benchmark also does not establish general reliability, time saving, usefulness on real customer data, or performance on larger datasets.

## Qualitative findings

The model sometimes labelled valid records as contradictory or qualifying when the relationship was weak. For example, `F015` — a manager saying they do not use the finance reports — was included as contradictory evidence in runs 2 and 3.

Scorer v2 now exposes this through **qualification precision**, rather than rewarding expected qualifying records without penalising irrelevant additions.

## Scorer limitation found after publication

A later red-team review demonstrated that scorer v1 could ignore an additional unmatched finding and citations attached to it. It could also overwrite multiple findings mapped to the same reference theme and aggregate unique evidence IDs in a way that hid incorrect use of an ID in one theme when the same ID was used correctly elsewhere.

Scorer v2 repairs these mechanical blind spots. It still does not determine whether an unmatched finding is semantically wrong; unmatched findings are surfaced for human review because the reference itself may be incomplete.

## Current decision

The historical experiment identifies a **reference-coverage question** worth investigating, but theme count is not a product-quality target.

The next sequence is:

1. independently challenge the human reference;
2. use the repaired scorer and current OpenAI-backed application configuration for future experiments;
3. capture and fix deterministic evidence-integrity failures;
4. run the compact behavioural baseline;
5. test bounded improvements alongside practitioner validation.

RAG remains deferred because all 40 records are supplied directly to the model and no measured retrieval problem currently justifies retrieval infrastructure. This is not a claim that retrieval has been proven reliable.

## Reproduce the scores

The original v1 score files remain stored with the benchmark artefacts.

To score a stored human-mapped run with scorer v2:

```bash
python evaluation/evaluate.py evaluation/runs/gemini-20260920T195039Z/run-1.json
```

The independent reference-review instructions are in [`independent-reference-review.md`](independent-reference-review.md).
