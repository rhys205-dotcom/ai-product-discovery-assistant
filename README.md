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
2. Validate feedback identifiers before analysis.
3. Ask an LLM for structured themes, pain points, cited evidence and proposed opportunities.
4. Validate the minimum structure of the model response before rendering it.
5. Display the source feedback cited for each finding.
6. Keep evidence, AI interpretation and proposed opportunity visually separate.
7. Let a reviewer accept, edit or reject each finding and add a note.
8. Export reviewed findings with dataset/run provenance while preserving the original model output separately.

The application does **not** automatically prioritise features, make roadmap decisions or treat model confidence as proof.

## Two demonstration modes

### Public review workflow

The [public demo](https://dowsall.com/discovery-assistant) uses 40 synthetic feedback records and a pre-generated illustrative analysis. It does not call a live model, upload visitor data or send information to a server.

Its purpose is to demonstrate the review/governance interaction: inspecting evidence, challenging an interpretation and recording a human decision. The illustrative sample is not presented as one of the stored benchmark runs.

### Local LLM prototype

The local Streamlit application sends the supplied feedback to Gemini using the Google Gen AI SDK and returns schema-constrained JSON for application-side validation and review. Use synthetic or otherwise authorised data only.

The local workflow fingerprints the active dataset and binds findings and reviewer state to the analysis run that produced them. Changing dataset or starting a new analysis invalidates stale findings/review controls rather than allowing evidence to be silently reattached.

## Run locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the deterministic regression tests:

   ```bash
   python -m unittest discover -s evaluation -p "test_*.py"
   ```

3. Set `GEMINI_API_KEY` in your environment.
4. Optionally set `GEMINI_MODEL` to override the configured default (`gemini-3.5-flash`).
5. Start the application:

   ```bash
   streamlit run app.py
   ```

The CSV must contain:

- `feedback_id`
- `source`
- `persona`
- `feedback`

`feedback_id` values must be non-blank and unique after whitespace is trimmed.

## Product principles

- **AI assists; people decide.** Findings are proposals for review.
- **Evidence before conclusions.** Every finding should cite source feedback IDs.
- **Separate evidence from inference.** Customer statements, model interpretation and proposed opportunities are different things.
- **No false precision.** Evidence strength should be grounded in observable support, not a model-generated probability.
- **Synthetic public data.** The demonstration exposes no former-employer or customer information.
- **Evaluate repeated performance.** A polished example is not evidence that the product is reliable.
- **Validate the product, not only the model.** The workflow should help practitioners produce useful, defensible analysis, not merely score well on synthetic benchmarks.
- **Preserve provenance.** Dataset identity, model output, reviewer changes and run metadata should not be silently mixed.

The reasoning behind these choices is recorded in the [AI decision log](docs/ai-decisions.md).

## Current architecture

- Python
- Streamlit review interface
- Google Gen AI SDK / Gemini Interactions API
- Schema-constrained JSON plus application-side contract validation
- CSV input with identifier validation
- SHA-256 dataset identity
- Synthetic 40-record sample dataset
- Human accept/edit/reject workflow
- Provenance-preserving reviewed JSON export

RAG, embeddings and vector storage are deliberately excluded from the MVP. Retrieval infrastructure is not presently justified because the current datasets are supplied directly to the model; that is not a claim that retrieval has been proven reliable.

## What is validated—and what is not

### Implemented

- Evidence-linked structured findings
- Rejection of blank/duplicate feedback IDs before analysis
- Detection of cited IDs missing from the active dataset
- Dataset fingerprinting and analysis/run binding
- Stale analysis/review-state invalidation on dataset or run change
- Structured model-response validation
- Failed-attempt handling that clears older analysis first
- Preservation of raw/original model output separately from reviewer edits
- Dataset/run/provider/model/prompt provenance in review exports
- Human review decisions and notes
- Editable interpretation
- Public static review workflow
- Human-created reference baseline for the 40-record dataset
- Relationship-aware scorer v2 with explicit unmatched-finding and duplicate-mapping checks
- Regression tests for scorer and trust-foundation failure modes
- Secure historical Gemini benchmark runner limited to three controlled calls
- Three independently generated, human-mapped and scored historical benchmark runs
- Red-team runner that retains failed calls/invalid responses as explicit outcomes

### Historical benchmark finding

Across three `gemini-3.5-flash` runs, citation validity was 100% and mean evidence precision was 95.5%. The model consistently represented the two dominant reference distinctions but omitted the smaller communication and audit-history reference distinction in every run, producing mean theme coverage of 66.7%.

Those runs remain useful historical evidence. Scorer v2 now makes the limits more explicit: it scores evidence at the finding–citation relationship level, checks citations from unmatched findings and prevents duplicate mappings from disappearing. The human reference itself remains contestable; an independent blind practitioner review is retained as a non-blocking trailing activity.

See the [full results and limitations](evaluation/results.md).

### Broader review finding

A wider review identified important product and evaluation risks that the first benchmark does not adequately test: duplicate/blank IDs, stale findings after dataset changes, narrow evidence being presented too strongly, prompt injection, unsupported embellishment, false contradiction, over-merging and over-fragmentation.

The deterministic trust failures were recorded before repair in [`evaluation/red-team/trust-baseline.md`](evaluation/red-team/trust-baseline.md). The repair implementation is now in place. The regression suite and E14 malformed-ID smoke test have passed; E15 stale-state/export smoke verification remains before Step 2 is closed.

It also highlighted a larger gap: the practical product hypothesis — whether practitioners reach a useful, defensible analysis faster — has not yet been tested.

### Not yet validated

- Whether the human reference theme boundaries are shared by another independent practitioner
- Final E15 stale-state/export smoke verification
- Behaviour across the compact model red-team cases using the current Gemini application configuration
- Whether targeted changes improve high-severity model failures without causing regressions
- Whether practitioners gain a useful time or quality advantage
- Whether behaviour generalises to a fresh holdout dataset
- Performance on larger or commercially realistic datasets

Those gaps drive the [revised roadmap](backlog.md); they are not presented as completed outcomes.

## Evaluation

The [evaluation workspace](evaluation/README.md) contains the contestable human reference, scorer v2, scorer regression tests, trust-foundation tests, independent-review instructions, generated model outputs and historical benchmark artefacts.

Future before/after product experiments will use the **current Gemini-backed application request path and configuration** and hold the relevant model/request settings constant. The earlier Gemini benchmark remains separately labelled historical evidence because it used a different benchmark runner/request path and should not be treated as a clean before/after baseline merely because the provider/model family overlaps.

The deterministic trust baseline is recorded separately from the repaired implementation. The next model-evaluation phase is the existing compact behavioural suite; a larger automated eval platform remains out of scope.

## Repository structure

- `app.py` — Streamlit review interface
- `src/analyse_feedback.py` — prompt construction, feedback validation, Gemini call and model-response validation
- `src/review_integrity.py` — dataset/run binding and provenance-preserving export helpers
- `data/sample-feedback.csv` — synthetic source feedback
- `docs/ai-decisions.md` — product and AI decision record
- `evaluation/` — reference, benchmark, scorer v2, trust tests, blind-review pack and red-team cases
- `examples/` — example outputs
- `backlog.md` — current experiments and revised roadmap

## Status

**v0.4 — First controlled benchmark completed**

**Step 1 — Core evaluation foundation repaired**

Scorer blind spots have been fixed and documented, the human reference is explicitly contestable, and the independent reference review is now a trailing activity rather than a development gate.

**Step 2 — Trust-repair implementation complete; final local verification in progress**

The pre-fix failures are recorded. Identifier validation, dataset/run binding, stale-state invalidation, structured response validation, failure-state handling and provenance-preserving exports are implemented with regression coverage. The regression suite and E14 smoke test have passed; E15 and one export inspection remain.

After that short verification, the next roadmap activity is **Step 3 — run the compact behavioural baseline** on the current Gemini-backed application configuration.

Practitioner validation remains in the bounded improvement cycle after the behavioural baseline.

## About

This is a personal product-management experiment, not production software. Its purpose is to demonstrate product framing, evidence traceability, human oversight, evaluation discipline and evidence-led iteration of an AI-assisted workflow.
