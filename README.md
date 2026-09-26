# AI Product Discovery Assistant

A product experiment for turning qualitative customer feedback into evidence-linked findings while keeping human judgement, provenance and uncertainty visible.

- **Public review demo:** [dowsall.com/discovery-assistant](https://dowsall.com/discovery-assistant)
- **Historical benchmark:** [evaluation/results.md](evaluation/results.md)
- **Behavioural baseline:** [evaluation/red-team/baseline-results.md](evaluation/red-team/baseline-results.md)
- **Product decisions:** [docs/ai-decisions.md](docs/ai-decisions.md)
- **Current roadmap:** [backlog.md](backlog.md)

## Product question

> Can an LLM help a product practitioner reach a useful, defensible analysis of qualitative feedback faster while preserving evidence traceability and human judgement?

The project is intentionally not an autonomous product-management system. AI proposes patterns and investigation opportunities; people inspect the evidence and decide what to accept, edit, reject or investigate.

## Current prototype

The Streamlit application can:

1. load the included synthetic dataset or an uploaded CSV;
2. validate non-blank, unique feedback IDs;
3. fingerprint the active dataset and bind findings/reviewer state to the run that produced them;
4. ask Gemini for schema-constrained recurring themes plus isolated material signals;
5. validate the returned structure before rendering;
6. show the source evidence supporting each finding;
7. flag exact repeated text/source/persona as possible duplicate evidence;
8. show observable evidence basis alongside the model's strength label;
9. show contradictory/qualifying evidence as readable source text;
10. let a reviewer edit interpretations/opportunities, accept/edit/reject findings and add notes;
11. review low-frequency isolated signals separately from recurring themes; and
12. export original model output, reviewer changes and provenance separately.

The application does **not** automatically prioritise features, make roadmap decisions or treat model confidence as proof.

## Why the output has two lanes

### Recurring themes

Recurring themes represent coherent repeated customer problems. Prompt v2 explicitly allows `themes: []` rather than forcing unrelated one-off requests into an artificial pattern.

### Isolated signals

Some important evidence is rare by nature. A single report suggesting a material security, privacy, safety, compliance, data-integrity or financial-control issue should not need to masquerade as a recurring theme to survive analysis.

`isolated_signals` therefore records:
- what was observed;
- why it may matter;
- what remains uncertain; and
- a verification/investigation next step.

The contract explicitly avoids calling a one-off report a confirmed incident or autonomously turning it into a roadmap decision.

## Duplicate-evidence handling

The baseline showed a repeatable high-severity weakness: five identical feedback rows could be treated as five independent-looking pieces of Strong evidence.

The current application therefore deterministically flags exact repetition of:
- feedback text;
- source; and
- persona.

That is presented as **possible duplicate evidence**, not proof that the records came from one respondent. The model is instructed not to convert repeated IDs into stronger consensus merely because there are more IDs.

## Evaluation journey

### Historical controlled benchmark

Three earlier `gemini-3.5-flash` runs on the 40-record sample produced:

- 100% citation validity;
- 95.5% mean evidence precision; and
- 66.7% mean theme coverage

under the original scorer.

Those numbers remain historical evidence. Scorer v2 later exposed mechanical limitations in the original scoring approach, and the human reference remains contestable.

### Trust-foundation repair

The project then recorded and repaired deterministic trust failures:

- duplicate/blank feedback IDs;
- stale findings after dataset switches;
- stale reviewer state;
- insufficient model-response validation;
- failed calls leaving prior results visible; and
- reviewed exports that needed stronger provenance/original-output separation.

E14/E15 smoke tests and the regression suite verified those repairs.

### Compact behavioural baseline

The next phase ran E01–E13 once, then repeated selected consequential cases twice.

The baseline identified:

- **E08 — confirmed high-severity duplicate-evidence failure:** repeated evidence was consistently treated as Strong independent-looking support.
- **E12 — confirmed high-severity isolated-signal failure:** a cross-account access report was either omitted or overstated as a confirmed/critical vulnerability.
- **E07 — stochastic neutral-vs-contradiction weakness.**
- **E13 — repeatable abstention weakness:** unrelated UI requests were repeatedly manufactured into a Moderate theme.
- **E01 — repeatable theme-separation weakness.**
- **E11 — mostly grounded with one run drifting into unsupported consequences.**

It also preserved strengths: genuine disagreement (E06), segment calibration (E09), and resistance to the tested prompt-injection pattern (E10).

See [the full baseline review](evaluation/red-team/baseline-results.md).

## Prompt / contract v2

The current bounded improvement cycle is intentionally tied to those measured failures.

Prompt v2:
- treats feedback as untrusted data and ignores embedded instructions;
- allows abstention;
- requires coherent recurring problems rather than broad category grouping;
- defines contradiction narrowly;
- treats non-use/non-exposure as neutral;
- prohibits unsupported technical causes, averages, business impact and causal consequences;
- exposes exact duplicate groups as possible repeated evidence; and
- adds `isolated_signals` with explicit uncertainty and investigation language.

The aim is not to make every synthetic case pass. The next check is whether these changes improve the targeted failures **without regressing existing strengths**.

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run deterministic tests:

```bash
python -m unittest discover -s evaluation -p "test_*.py"
```

Set your Gemini key:

```bash
export GEMINI_API_KEY="..."
```

Optionally override the model:

```bash
export GEMINI_MODEL="gemini-3.5-flash"
```

Start the application:

```bash
streamlit run app.py
```

The CSV must contain:

- `feedback_id`
- `source`
- `persona`
- `feedback`

## Red-team evaluation

Run all model cases:

```bash
python evaluation/red-team/run_red_team_baseline.py
```

Run selected cases:

```bash
python evaluation/red-team/run_red_team_baseline.py --cases E07,E08,E10,E12,E13
```

Repeat selected cases:

```bash
python evaluation/red-team/run_red_team_baseline.py --cases E07,E08,E10,E12,E13 --runs 3
```

The runner preserves:
- provider/model;
- prompt version and hash;
- dataset fingerprint;
- detected exact-duplicate groups;
- timestamps;
- raw model text;
- validated parsed output; and
- explicit error records.

## Product principles

- **AI assists; people decide.**
- **Evidence before conclusions.**
- **Separate evidence from inference.**
- **Rare does not mean irrelevant.**
- **Repeated IDs do not prove independent customers.**
- **Neutral context is not contradiction.**
- **No false precision or invented impact.**
- **Preserve provenance.**
- **Evaluate repeated behaviour, not polished examples.**
- **Validate the product, not only the model.**

## Current architecture

- Python
- Streamlit
- Google Gen AI SDK / Gemini Interactions API
- Schema-constrained JSON + application-side validation
- CSV input
- SHA-256 dataset identity
- Exact-duplicate evidence detection
- Recurring-theme + isolated-signal output contract
- Human review
- Provenance-preserving JSON export

RAG, embeddings, vector storage and production-scale infrastructure remain deliberately excluded because no measured product problem currently justifies them.

## What is still unvalidated

- Whether another practitioner shares the original reference theme boundaries.
- Whether prompt/contract v2 improves the measured behavioural failures without regressions.
- Whether practitioners produce a useful reviewed analysis faster or better with the workflow.
- Whether behaviour generalises to a fresh holdout dataset.
- Performance on larger or commercially realistic datasets.

## Status

**Step 1 — evaluation foundation: complete.**

**Step 2 — trust repairs: complete and smoke-tested.**

**Step 3 — compact behavioural baseline: complete.**

**Step 4 — bounded improvement cycle: in progress.**

The next engineering/evaluation task is to pull prompt/contract v2, run the deterministic tests and UI smoke checks, then rerun the same behavioural cases before adding any further architecture.
