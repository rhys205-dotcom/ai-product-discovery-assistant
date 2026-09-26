# Evaluation workspace

This folder keeps the AI Product Discovery Assistant's evaluation evidence inspectable and separates historical benchmark results, deterministic trust controls, behavioural red-team cases and human judgement.

## Current evaluation position

The project now has four distinct layers of evidence:

1. **Historical controlled benchmark** — three `gemini-3.5-flash` runs using frozen prompt v1.
2. **Scorer v2** — a repaired relationship-aware scorer for the original human-mapped benchmark.
3. **Deterministic trust controls** — dataset identity, stale-state invalidation, response validation and provenance-preserving export.
4. **Behavioural red-team baseline** — E01–E13 with repeat evidence on important cases, followed by a bounded prompt/contract v2 improvement cycle.

The human reference remains **contestable**, not objective ground truth. An independent blind practitioner review is a trailing non-blocking activity.

## Historical benchmark

The 20 September 2026 experiment used:
- the 40-record synthetic dataset;
- `gemini-3.5-flash`;
- prompt v1;
- schema-constrained output; and
- explicit human theme mapping before scoring.

Historical v1 headline results:
- 100% citation validity;
- 95.5% mean evidence precision;
- 66.7% mean theme coverage.

These results remain useful historical evidence, but they are not a universal product-quality score.

`run_gemini_benchmark.py` now embeds the historical v1 prompt locally so future changes to the application prompt cannot silently alter a reproduction of that experiment.

## Scorer v2

`evaluate.py` repairs several blind spots in the original scorer:

- unmatched findings remain visible;
- citations in unmatched findings contribute to citation validity;
- relevance is checked per finding–citation relationship;
- duplicate mappings are preserved rather than overwritten;
- qualification precision penalises irrelevant contradictory/qualifying additions.

Metrics remain separated because a valid citation can still be irrelevant and an unmatched finding can expose a limitation in the human reference rather than a model error.

Run scorer tests:

```bash
python -m unittest discover -s evaluation -p "test_evaluate.py"
```

## Deterministic trust controls

The pre-fix failures are preserved in [`red-team/trust-baseline.md`](red-team/trust-baseline.md).

The repaired application:
- rejects blank/duplicate IDs;
- fingerprints the ordered dataset;
- binds analysis/reviewer state to dataset + run;
- invalidates stale state on dataset/run changes;
- validates structured responses;
- clears earlier output before a new model attempt;
- records failed calls;
- preserves raw/original output separately from reviewer edits; and
- exports provenance.

E14 and E15 smoke tests have passed.

Prompt/contract v2 adds deterministic detection of exact text/source/persona repetition as **possible duplicate evidence** and preserves those groups in run metadata.

Run trust tests:

```bash
python -m unittest discover -s evaluation -p "test_trust_foundation.py"
```

Run the full deterministic suite:

```bash
python -m unittest discover -s evaluation -p "test_*.py"
```

## Behavioural red-team baseline

See:
- [`red-team/acceptance-criteria.md`](red-team/acceptance-criteria.md) — fixed before output review;
- [`red-team/baseline-results.md`](red-team/baseline-results.md) — reviewed v1 baseline/repeat findings;
- [`red-team/README.md`](red-team/README.md) — execution and scoring discipline.

The baseline found confirmed high-priority weaknesses around:
- duplicate evidence manufacturing confidence (E08);
- low-frequency serious signals being omitted or overstated (E12).

It also found:
- stochastic neutral-vs-contradiction errors (E07);
- repeatable abstention weakness (E13);
- repeatable theme-separation weakness (E01);
- mostly grounded behaviour with occasional unsupported consequence drift (E11).

Strengths included E06 disagreement handling, E09 breadth calibration and the tested E10 injection pattern.

No overall percentage is used because severity differs materially between cases.

## Prompt / contract v2

The current bounded improvement cycle targets the measured failures without adding unrelated architecture.

Changes include:
- explicit `isolated_signals` output with uncertainty + investigation next step;
- exact duplicate-evidence detection and exposure;
- narrower contradiction rules;
- explicit abstention;
- stronger groundedness instructions;
- observable evidence-basis display;
- readable contradictory/qualifying evidence;
- editable opportunities;
- reviewed isolated signals preserved in exports.

The next evidence step is a before/after rerun of the same behavioural cases with model/request settings held constant.

## Files

- `reference-analysis.json` — machine-readable human reference; contestable.
- `golden-analysis.md` — readable explanation of the reference.
- `independent-reference-review.md` — blind review pack.
- `example-run.json` — deterministic fixture, not model performance.
- `evaluate.py` — scorer v2.
- `test_evaluate.py` — scorer regression tests.
- `test_trust_foundation.py` — trust/prompt-contract regression tests.
- `run_gemini_benchmark.py` — frozen historical v1 benchmark runner.
- `results.md` — historical benchmark results and limitations.
- `red-team/` — behavioural cases, acceptance criteria, trust baseline and current results.

## Evaluation rules

1. Preserve unmodified model output separately from human review.
2. Hold model/request configuration fixed inside a before/after experiment.
3. Treat reference mapping as human judgement and record disagreement.
4. Do not hide unmatched findings or failed calls.
5. Report failures and severity, not only aggregate percentages.
6. Keep dataset/run/prompt provenance attached to outputs.
7. Do not count repeated IDs as proof of independent customers.
8. Keep holdout data genuinely fresh; once used for tuning, it becomes development data.
9. Practitioner validation is required to test whether the workflow actually improves the user's task.

## Important limitation

Even the repaired scorer, deterministic trust controls and red-team suite do not establish commercial usefulness or prove that a Product Manager makes better decisions with the tool. That requires practitioner validation and a fresh holdout check.
