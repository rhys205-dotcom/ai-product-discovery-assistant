# AI Product Discovery Assistant

A working product experiment for turning qualitative customer feedback into evidence-linked findings and proposed opportunities while keeping human review explicit.

- **Public review demo:** [dowsall.com/discovery-assistant](https://dowsall.com/discovery-assistant)
- **Benchmark results:** [Three controlled Gemini runs](evaluation/results.md)
- **Product decision log:** [docs/ai-decisions.md](docs/ai-decisions.md)
- **Current backlog:** [backlog.md](backlog.md)

## The product problem

Product teams can collect more interviews, support tickets and survey comments than they can analyse consistently. Summaries alone are not enough: a reviewer needs to see which customer evidence supports a finding, where the model has inferred meaning and what still requires product judgement.

This project tests whether an LLM can help a product practitioner reach a useful, defensible analysis faster without hiding the evidence or making autonomous roadmap decisions.

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

The [public demo](https://dowsall.com/discovery-assistant) uses 40 synthetic feedback records and a pre-generated illustrative analysis. It does not call a live model, upload visitor data or send information to a server.

Its purpose is to demonstrate the review/governance interaction: inspecting evidence, challenging an interpretation and recording a human decision. The illustrative sample is not presented as one of the stored benchmark runs.

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
- **No false precision.** Evidence strength should be grounded in observable support, not a model-generated probability.
- **Synthetic public data.** The demonstration exposes no former-employer or customer information.
- **Evaluate repeated performance.** A polished example is not evidence that the product is reliable.
- **Validate the product, not only the model.** The workflow should help practitioners produce useful, defensible analysis, not merely score well on synthetic benchmarks.

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

RAG, embeddings and vector storage are deliberately excluded from the MVP. Retrieval infrastructure is not presently justified because the current datasets are supplied directly to the model; that is not a claim that retrieval has been proven reliable.

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
- Three independently generated, human-mapped and scored historical benchmark runs

### Historical benchmark finding

Across three `gemini-3.5-flash` runs, citation validity was 100% and mean evidence precision was 95.5%. The model consistently found the two dominant reference themes but omitted the smaller communication and audit-history reference theme in every run, producing mean theme coverage of 66.7%.

Those numbers reproduce for the stored runs, but they establish only what the scorer measures. The human reference is a documented judgement rather than objective ground truth, and the original scorer has blind spots around unmatched findings and some citation relationships. The benchmark therefore remains useful historical evidence, not a universal measure of analysis quality.

See the [full results and limitations](evaluation/results.md).

### Broader review finding

A wider review identified important product and evaluation risks that the first benchmark does not adequately test: duplicate/blank IDs, stale findings after dataset changes, unmatched hallucinated findings escaping headline metrics, narrow evidence being presented too strongly, prompt injection, unsupported embellishment, false contradiction, over-merging and over-fragmentation.

It also highlighted a larger gap: the practical product hypothesis — whether practitioners reach a useful, defensible analysis faster — has not yet been tested.

### Not yet validated

- Whether the human reference theme boundaries are shared by another independent practitioner
- Behaviour across the compact red-team cases using the current application configuration
- Whether targeted changes improve high-severity failures without causing regressions
- Whether practitioners gain a useful time or quality advantage
- Whether behaviour generalises to a fresh holdout dataset
- Performance on larger or commercially realistic datasets

Those gaps drive the [revised roadmap](backlog.md); they are not presented as completed outcomes.

## Evaluation

The [evaluation workspace](evaluation/README.md) contains the human reference, inspectable scoring rules, generated model outputs with explicit human annotations and per-run scores.

Future before/after product experiments will use one application configuration and hold the relevant model/request settings constant. The earlier Gemini benchmark remains separately labelled historical evidence rather than being treated as directly comparable with the OpenAI-backed application.

The next evaluation phase is deliberately proportionate: repair the evaluation foundation, capture and fix evidence-integrity failures, run the existing compact behavioural cases, then combine one bounded improvement cycle with practitioner validation. A larger automated eval platform is out of scope.

## Repository structure

- `app.py` — Streamlit review interface
- `src/analyse_feedback.py` — prompt construction and LLM analysis
- `data/sample-feedback.csv` — synthetic source feedback
- `docs/ai-decisions.md` — product and AI decision record
- `evaluation/` — reference, benchmark, red-team cases and scoring artefacts
- `examples/` — example outputs
- `backlog.md` — current experiments and revised roadmap

## Status

**v0.4 — First controlled benchmark completed**

**Current focus — repair evaluation and trust foundations**

The next work is to challenge the reference with an independent practitioner, correct scorer blind spots, capture and repair evidence-identity/state failures, and then run the compact behavioural baseline. Prompt `v2` remains a potential intervention during the bounded improvement cycle rather than the immediate goal.

Practitioner validation has been moved forward: the project should test whether the workflow improves the user's task before investing in substantially more evaluation machinery.

## About

This is a personal product-management experiment, not production software. Its purpose is to demonstrate product framing, evidence traceability, human oversight, evaluation discipline and evidence-led iteration of an AI-assisted workflow.