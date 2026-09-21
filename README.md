# AI Product Discovery Assistant

A working product experiment for turning qualitative customer feedback into evidence-linked findings and proposed opportunities while keeping human review explicit.

- **Public review demo:** [dowsall.com/discovery-assistant](https://dowsall.com/discovery-assistant)
- **Benchmark results:** [Three controlled Gemini runs](evaluation/results.md)
- **Product decision log:** [docs/ai-decisions.md](docs/ai-decisions.md)
- **Current backlog:** [backlog.md](backlog.md)

## The product problem

Product teams can collect more interviews, support tickets and survey comments than they can analyse consistently. Summaries alone are not enough: a reviewer needs to see which customer evidence supports a finding, where the model has inferred meaning and what still requires product judgment.

This project tests whether an LLM can accelerate that analysis without hiding the evidence or making autonomous roadmap decisions.

## Current prototype

The Streamlit prototype can:

1. Load the included synthetic dataset or accept an uploaded CSV.
2. Ask an LLM for structured themes, pain points, cited evidence and proposed opportunities.
3. Display the source feedback cited for each finding.
4. Keep evidence, AI interpretation and proposed opportunity visually separate.
5. Let a reviewer accept, edit or reject each finding and add a note.
6. Export the reviewed result as JSON.

The application does **not** automatically prioritise features, make roadmap decisions or treat model confidence as proof.

## Two demonstration modes

### Public review workflow

The [public demo](https://dowsall.com/discovery-assistant) uses 40 synthetic feedback records and a pre-generated sample analysis. It does not call a live model, upload visitor data or send information to a server.

Its purpose is to demonstrate the higher-value product interaction: inspecting evidence, challenging an interpretation and recording a human decision.

### Local LLM prototype

The local Streamlit application sends the supplied feedback to a configurable OpenAI model and returns structured JSON for review. Use synthetic or otherwise authorised data only.

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set `OPENAI_API_KEY` in your environment.
3. Optionally set `OPENAI_MODEL` to override the configured default.
4. Start the application:

   ```bash
   streamlit run app.py
   ```

The CSV must contain:

- `feedback_id`
- `source`
- `persona`
- `feedback`

## Product principles

- **AI assists; people decide.** Findings are proposals for review.
- **Evidence before conclusions.** Every finding should cite source feedback IDs.
- **Separate evidence from inference.** Customer statements, model interpretation and proposed opportunities are different things.
- **No false precision.** Evidence strength is based on observable support, not a model-generated probability.
- **Synthetic public data.** The demonstration exposes no former-employer or customer information.
- **Evaluate repeated performance.** A polished example is not evidence that the product is reliable.

The reasoning behind these choices is recorded in the [AI decision log](docs/ai-decisions.md).

## Current architecture

- Python
- Streamlit review interface
- OpenAI Responses API
- Structured JSON output
- CSV input
- Synthetic 40-record sample dataset
- Human accept/edit/reject workflow
- Reviewed JSON export

RAG, embeddings and vector storage are deliberately excluded from the MVP. They will be considered only if evaluation shows that dataset size or evidence retrieval makes them necessary.

## What is validated—and what is not

### Implemented and evaluated

- Evidence-linked structured findings
- Detection of missing cited feedback IDs in the review interface
- Human review decisions and notes
- Editable interpretation
- Review export
- Public static review workflow
- Human-created reference analysis for the 40-record dataset
- Transparent scoring for theme coverage, citation validity, evidence relevance and contradiction coverage
- Secure Gemini benchmark runner limited to three controlled calls
- Three independently generated, human-mapped and scored benchmark runs

### Benchmark finding

Across three `gemini-3.5-flash` runs, citation validity was 100% and mean evidence precision was 95.5%. The model consistently found the two dominant themes but missed the smaller communication and audit-history theme in every run, producing mean theme coverage of 66.7%.

This identifies **theme coverage** as the next problem to test. It does not support adding RAG: the relevant records were generally retrieved, but overlapping problems were grouped too broadly.

See the [full results and limitations](evaluation/results.md).

### Not yet validated

- Whether a revised prompt improves smaller-theme separation
- Whether performance generalises to other datasets or models
- Time saved for product practitioners
- Performance on larger or commercially realistic datasets

Those gaps are the current focus of the [backlog](backlog.md); they are not presented as completed outcomes.

## Evaluation

The [evaluation workspace](evaluation/README.md) contains the human reference, inspectable scoring rules, generated model outputs with explicit human annotations and per-run scores.

The first controlled benchmark keeps the dataset, prompt and model fixed across three runs. It reports every run rather than selecting the strongest output and records both quantitative scores and qualitative failure modes. The API key is never written to the repository.

## Repository structure

- `app.py` — Streamlit review interface
- `src/analyse_feedback.py` — prompt construction and LLM analysis
- `data/sample-feedback.csv` — synthetic source feedback
- `docs/ai-decisions.md` — product and AI decision record
- `evaluation/` — reference, runner, annotated benchmark outputs and scores
- `examples/` — example outputs
- `backlog.md` — current experiments and deferred scope

## Status

**v0.4 — First controlled benchmark completed**

The next milestone is a separately versioned prompt experiment targeting the consistently missed communication and audit-history theme while retaining `v1` as the baseline.

## About

This is a personal product-management experiment, not production software. Its purpose is to demonstrate product framing, evidence traceability, human oversight and honest evaluation of an AI-assisted workflow.
