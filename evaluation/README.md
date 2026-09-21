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

- `reference-analysis.json` — machine-readable scoring source of truth for the 40-record synthetic dataset.
- `golden-analysis.md` — readable explanation of the same three-theme reference.
- `example-run.json` — deterministic fixture used to verify the scorer; it is **not** claimed as model performance.
- `evaluate.py` — dependency-free scoring script.
- `run_gemini_benchmark.py` — secure runner for exactly three controlled Gemini analyses.
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

## Generate three controlled Gemini runs

Create a key in [Google AI Studio](https://aistudio.google.com/apikey). Keep it out of the repository and set it only as an environment variable.

PowerShell:

```powershell
$env:GEMINI_API_KEY="your-key"
python evaluation/run_gemini_benchmark.py
```

macOS, Linux or GitHub Codespaces:

```bash
export GEMINI_API_KEY="your-key"
python evaluation/run_gemini_benchmark.py
```

The runner:

- makes exactly three API calls;
- uses `gemini-3.5-flash` unless `GEMINI_MODEL` is explicitly set;
- sends only the synthetic public dataset;
- requests schema-constrained JSON;
- disables server-side interaction storage for each call;
- writes model, prompt hash, prompt version and timestamps to the run manifest;
- never writes the API key to disk.

Generated outputs are saved under `evaluation/runs/<benchmark-id>/`. In the first benchmark, the run files contain the generated findings plus human-added `theme_id` mappings. Human mapping is deliberately required before scoring so the benchmark does not disguise subjective matching as an automated fact.

For subsequent benchmarks, preserve the unmodified model response separately from the human mapping and calculated score.

## Run a genuine benchmark

1. Keep the dataset, prompt version and model fixed.
2. Run the analysis at least three times.
3. Add `theme_id` values during human matching; do not use automated name matching as if it were ground truth.
4. Save each unmodified model response with its model, prompt version and run date.
5. Store human mappings and calculated scores separately from that response.
6. Evaluate each run and report both the individual scores and variation between runs.
7. Record reviewer disagreement and qualitative failure modes alongside the numbers.

## Important limitation

The reference analysis is a documented human judgement, not objective truth. The scorer is useful because its rules are inspectable and repeatable, not because the resulting numbers are universally valid.

Three repeated runs provide an initial consistency check, not statistically robust evidence of performance across different datasets, prompts or models.
