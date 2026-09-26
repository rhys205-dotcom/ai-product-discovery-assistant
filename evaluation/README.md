# Evaluation workspace

This folder turns the prototype's evaluation principles into a repeatable, inspectable workflow.

## Current evaluation position

The first controlled Gemini benchmark remains useful historical evidence, but it is not treated as a universal measure of product quality. The project now uses:

- a **contestable human reference baseline**, not objective ground truth;
- **scorer v2**, which keeps unmatched findings visible and scores evidence at the finding–citation relationship level;
- the **current OpenAI-backed application configuration** as the baseline for future before/after product experiments;
- the Gemini benchmark as a separately labelled historical experiment.

An independent practitioner review of the three-theme reference is still pending. It is now a **trailing, non-blocking evidence-strengthening activity** rather than a gate for continued development. See [`independent-reference-review.md`](independent-reference-review.md).

## What scorer v2 measures

- **Theme coverage** — proportion of reference theme distinctions represented by the human mapping.
- **Citation validity** — proportion of all cited feedback relationships that point to an ID present in the dataset, including citations in unmatched findings.
- **Evidence precision** — proportion of valid core citations on matched findings that support the specific reference theme they are attached to.
- **Reference evidence coverage** — proportion of expected `(theme, feedback ID)` relationships represented.
- **Qualification coverage** — proportion of expected qualifying relationships represented.
- **Qualification precision** — proportion of valid qualifying citations on matched findings that actually belong to the expected qualifying set.
- **Unmatched findings** — generated findings not mapped to the current reference; these are surfaced for human review rather than automatically marked wrong.
- **Duplicate mappings** — multiple generated findings mapped to one reference theme; these are retained and flagged rather than overwritten.
- **Distractor citations** — isolated records used as core evidence for a broader finding.

The metrics are deliberately separated. A valid citation can still be irrelevant to the finding it supports, and a plausible unmatched finding may expose a limitation in the human reference rather than a model error.

## Why scorer v2 was introduced

The original scorer had several blind spots:

- an unmatched generated finding could escape the headline metrics;
- citations inside unmatched findings could escape citation-validity checks;
- multiple findings mapped to one reference theme could overwrite one another;
- aggregating unique feedback IDs could hide an ID used correctly in one theme but incorrectly in another;
- qualification coverage rewarded expected evidence without penalising irrelevant additions.

Scorer v2 repairs those mechanical issues without pretending that semantic judgement can be fully automated.

## Verify the scorer

From the repository root:

```bash
python -m unittest discover -s evaluation -p "test_evaluate.py"
```

Score a human-mapped run with:

```bash
python evaluation/evaluate.py evaluation/runs/<benchmark-id>/run-1.json
```

To save the result:

```bash
python evaluation/evaluate.py evaluation/runs/<benchmark-id>/run-1.json \
  --output evaluation/runs/<benchmark-id>/run-1-score-v2.json
```

## Historical Gemini benchmark

The 20 September 2026 experiment used three independent calls with:

- the same 40-record synthetic dataset;
- `gemini-3.5-flash`;
- prompt version `v1`;
- schema-constrained output;
- explicit human theme mapping before scoring.

The stored v1 score files are preserved as historical artefacts. [`results.md`](results.md) distinguishes those original published metrics from the relationship-aware v2 re-score.

This benchmark is **not** the future application baseline because the current application uses a different provider and response path. Future prompt comparisons should hold the current application configuration, dataset and model/request settings constant.

## v0.5 red-team suite

The current adversarial suite covers prompt injection, duplicated evidence, source dominance, unsupported embellishment, low-frequency/high-severity signals, identifier integrity and stale application state.

See [`red-team/README.md`](red-team/README.md) for the case specification, datasets, baseline runner and manual scorecard.

Known deterministic trust failures such as identifier and stale-state problems should be **recorded and then fixed promptly**; they do not need to wait for every model case to be completed.

## Files

- `reference-analysis.json` — machine-readable human reference baseline; independent review pending as a trailing activity.
- `golden-analysis.md` — readable explanation of the same reference and its contestability.
- `independent-reference-review.md` — blind review instructions for another PM/PO/BA.
- `example-run.json` — deterministic fixture; not claimed as model performance.
- `evaluate.py` — relationship-aware scorer v2.
- `test_evaluate.py` — regression tests for scorer blind spots.
- `run_gemini_benchmark.py` — historical three-run Gemini benchmark runner.
- `results.md` — historical results, revised interpretation and scorer-v2 re-score.
- `red-team/` — adversarial evaluation suite and baseline workspace.

## Evaluation rules from this point

1. Preserve unmodified model output separately from human mappings and scores.
2. Keep the model/request configuration fixed inside a before/after experiment.
3. Treat reference mapping as human judgement and record disagreement.
4. Surface unmatched findings rather than assuming the reference is exhaustive.
5. Report individual failures and severity, not only aggregate percentages.
6. Keep holdout data genuinely fresh; once it is used to tune the product, it is no longer a holdout.

## Important limitation

Even scorer v2 does not determine whether an interpretation is commercially useful, whether a proposed opportunity is sensible, or whether a human reviewer makes a better product decision. Those require qualitative review and practitioner validation.
