# Evaluation results

## Gemini benchmark — 20 September 2026

Three independent analyses were run against the unchanged 40-record synthetic feedback dataset using `gemini-3.5-flash`, prompt version `v1`.

Each generated theme was manually mapped to the documented human reference before scoring. The stored run files contain the generated findings plus the added `theme_id` annotation used for scoring. All three runs are reported; no run was excluded or selected as the preferred result.

## Results

| Metric | Run 1 | Run 2 | Run 3 | Mean |
|---|---:|---:|---:|---:|
| Theme coverage | 66.7% | 66.7% | 66.7% | 66.7% |
| Evidence precision | 96.4% | 93.5% | 96.7% | 95.5% |
| Reference evidence coverage | 84.4% | 90.6% | 90.6% | 88.5% |
| Citation validity | 100% | 100% | 100% | 100% |
| Contradiction coverage | 83.3% | 83.3% | 100% | 88.9% |

## What the benchmark shows

The model consistently identified:

- `T01` — manual reconciliation and exception handling;
- `T02` — delayed visibility of failed or pending payments.

It missed `T03` — payment communication and audit history — in all three runs. Some evidence belonging to `T03`, particularly `F037`, was absorbed into the broader payment-status theme rather than recognised as a distinct customer problem.

Across all runs:

- every cited feedback ID existed in the source dataset;
- no deliberate distractor was cited as core evidence;
- both identified themes met the minimum evidence threshold;
- evidence precision remained above 93%.

## Human-review findings

The model occasionally treated valid records as contradictory when they were not. For example, `F015` was misclassified as contradictory in runs 2 and 3.

The contradiction-coverage metric measures whether expected qualifying evidence was found, but does not penalise irrelevant items added to the contradictory-evidence list. This remains a limitation of the current scorer and demonstrates why automated scores still require qualitative review.

## Scope and limitations

Three runs provide an initial repeatability check, not statistically robust evidence of general model performance. The benchmark uses one synthetic dataset, one model and one prompt version.

The human reference is contestable, and the current scorer does not measure every qualitative error. In particular, contradiction coverage rewards expected qualifying evidence but does not penalise irrelevant additions.

For future experiments, the unmodified model response should be preserved separately from human mapping and calculated scores.

## Decision

The principal limitation is **theme coverage**, not citation faithfulness or retrieval.

The next experiment should test whether a revised prompt can separate smaller communication and audit-history problems from the dominant operational themes. The existing `v1` results must remain unchanged as the baseline for that comparison.

The results do not currently justify adding embeddings or a RAG architecture. The model already retrieves the relevant records reliably; the issue is how it groups and distinguishes overlapping themes.

## Reproduce the benchmark

Generate three controlled runs:

```bash
python evaluation/run_gemini_benchmark.py
```

After human theme mapping, score a run with:

```bash
python evaluation/evaluate.py evaluation/runs/<benchmark-id>/run-1.json
```

The reference analysis is a documented human judgement rather than objective ground truth. Results should therefore be interpreted as transparent comparative evidence, not as a universal measure of model quality.
