# Evaluation baseline

This folder turns the prototype's evaluation principles into a repeatable workflow.

## What is measured

- **Theme coverage** — proportion of human-reference themes found.
- **Citation validity** — proportion of cited feedback IDs that exist in the dataset.
- **Evidence precision** — proportion of valid citations that support the matched reference theme.
- **Reference evidence coverage** — proportion of the reference evidence cited.
- **Contradiction coverage** — proportion of documented qualifying or contradictory records surfaced.
- **Distractor citations** — isolated or irrelevant requests incorrectly used as core-theme evidence.

The metrics are deliberately separated. A run can cite only valid IDs while still citing irrelevant evidence, or achieve high precision while missing an important theme.

## Files

- `reference-analysis.json` — human-created comparison point for the 40-record synthetic dataset.
- `example-run.json` — deterministic fixture used to verify the scorer; it is **not** claimed as model performance.
- `evaluate.py` — dependency-free scoring script.
- `results.md` — current status and instructions for the first repeated benchmark.

## Run the scorer

From the repository root:

```bash
python evaluation/evaluate.py evaluation/example-run.json
```

To save the score:

```bash
python evaluation/evaluate.py evaluation/example-run.json \
  --output evaluation/example-run-score.json
```

## Run a genuine benchmark

1. Keep the dataset, prompt version and model fixed.
2. Run the analysis at least three times.
3. Add `theme_id` values during human matching; do not use automated name matching as if it were ground truth.
4. Save each raw result with its model, prompt version and run date.
5. Evaluate each run and report both the individual scores and variation between runs.
6. Record reviewer disagreement and qualitative failure modes alongside the numbers.

## Important limitation

The reference analysis is a documented human judgement, not objective truth. The scorer is useful because its rules are inspectable and repeatable, not because the resulting numbers are universally valid.
