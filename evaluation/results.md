# Evaluation results

## Current status

The v0.3 evaluation baseline is implemented. The repository now contains a documented human reference, explicit scoring rules and a deterministic fixture that verifies the workflow.

The fixture is not reported as model performance. Three controlled model runs are still required before making claims about repeatability, faithfulness or time saved.

## Scorer fixture

The included fixture exercises all three reference themes and demonstrates how the scorer separates:

- a cited ID that exists from evidence that is actually relevant;
- finding a theme from covering all of its important evidence;
- supporting evidence from contradictory or qualifying evidence;
- deliberate distractors from recurring customer problems.

Run it with:

```bash
python evaluation/evaluate.py evaluation/example-run.json
```

## First benchmark protocol

| Control | Rule |
|---|---|
| Dataset | Use the unchanged 40-record synthetic dataset |
| Prompt | Record and hold the prompt version constant |
| Model | Record and hold the model version constant |
| Runs | Minimum of three independent runs |
| Theme matching | Human-reviewed mapping to `T01`–`T03` |
| Evidence review | Inspect relevance, not only whether IDs exist |
| Reporting | Show every run and variation; do not select the strongest output |

## Decision gate

After the controlled runs, decide whether the main limitation is:

- **faithfulness**, requiring tighter evidence rules or prompt changes;
- **coverage**, requiring prompt or analysis changes;
- **repeatability**, requiring stronger structure or model controls; or
- **retrieval**, which would provide evidence for considering embeddings or RAG.

Until that evidence exists, additional architecture remains deferred.
