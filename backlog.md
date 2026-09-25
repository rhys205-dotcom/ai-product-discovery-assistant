# Product Backlog

This backlog records the next experiments for the AI Product Discovery Assistant. It separates completed capability from unvalidated assumptions so the repository reflects the real product state.

## Completed — v0.1: Product definition

- Defined the user problem, MVP boundaries and responsible-AI principles.
- Created a 40-record synthetic feedback dataset with multiple personas and research sources.
- Documented why AI assists rather than decides.
- Defined evidence, interpretation and proposed opportunity as separate output layers.
- Deferred RAG and embeddings until evaluation demonstrates a need.

## Completed — v0.2: Evidence-linked review

- Generate structured themes, pain points, evidence IDs and proposed opportunities.
- Load the sample data or accept an uploaded CSV.
- Display cited source feedback beneath each finding.
- Warn when the model cites an ID that is not present in the dataset.
- Allow a reviewer to accept, edit or reject a finding.
- Capture review notes and export the reviewed result as JSON.
- Publish a static public review workflow using pre-generated analysis and synthetic data.

## Completed — v0.3: Evaluation baseline

- Created a human reference analysis covering themes, supporting evidence, qualifying evidence and deliberate distractors.
- Added a dependency-free scoring script with explicit, inspectable rules.
- Separated theme coverage, citation validity, evidence relevance, reference coverage and contradiction coverage.
- Added a deterministic fixture to verify the scorer without presenting it as model performance.
- Defined a controlled protocol for repeated model runs.

## Completed — v0.4: First controlled benchmark

- Ran three Gemini analyses with the 40-record dataset, model and prompt version held constant.
- Recorded the provider, model, prompt hash, prompt version and timestamps.
- Human-mapped every generated theme to the documented reference before scoring.
- Reported every run rather than selecting a preferred result.
- Measured 100% citation validity, 95.5% mean evidence precision and 66.7% mean theme coverage.
- Identified a repeatable result: all three runs omitted the smaller payment communication and audit-history reference theme.
- Kept retrieval infrastructure deferred because all 40 records are supplied directly to the model and no measured retrieval problem currently justifies RAG.

## Completed — broader red-team review

A broader product review found that the first benchmark is useful but too narrow on its own. It also identified two important distinctions:

- reproducing the three-theme human reference is not automatically the same as producing the best product analysis;
- the practical product hypothesis — whether a practitioner can reach a useful, defensible analysis faster — remains untested.

The review also exposed concrete trust and evaluation risks, including duplicate/blank IDs, stale analysis after a dataset change, scorer blind spots around unmatched findings, narrow evidence being presented too strongly, unsupported embellishment, prompt injection, false contradiction and over-merging/over-fragmentation.

This changes the sequence of work. The project will repair the evaluation and trust foundation first, then run a compact behavioural baseline and practitioner validation before investing in more evaluation depth.

# Revised roadmap

## Step 1 — Repair the evaluation foundation — NOW

### Objective

Make sure the project can state precisely what existing results do and do not establish.

### Work

- Review the three-theme human reference with at least one independent product practitioner who has not seen the expected theme structure.
- Treat the human reference as a contestable judgement, not ground truth.
- Fix scorer blind spots so unmatched findings and their citations cannot disappear from headline checks.
- Score citation relevance at the finding–citation relationship level rather than only through aggregated unique IDs.
- Ensure additional or duplicate theme mappings cannot silently escape evaluation.
- Choose the current application configuration as the baseline for future prompt comparisons; retain the historical Gemini benchmark as a separately labelled experiment.
- Align public-demo and repository wording so illustrative sample output is clearly distinguished from measured benchmark output.

### Completion condition

The project can explain exactly what each published metric measures, what it misses and why the human reference is useful without presenting it as objective truth.

## Step 2 — Capture and fix trust failures

### Objective

Protect the core product promise: evidence must not become detached from the dataset or reviewer decision that produced it.

### Work

Record the current failures first, then fix them promptly. Completing every model red-team case is not a prerequisite.

- Reject blank and duplicate feedback IDs before analysis.
- Bind dataset identity, model analysis and review state together.
- Invalidate stale findings and review decisions when the dataset or analysis changes.
- Add basic structured-response validation so malformed or incomplete model output cannot appear as a valid analysis.
- Preserve original model output separately from reviewer edits.
- Include dataset/run provenance in reviewed exports.
- Ensure failed model calls and invalid responses are recorded as outcomes rather than silently leaving stale state.

### Completion condition

Findings and human decisions cannot silently acquire the wrong source evidence, and exported review artefacts preserve where the analysis came from and what the reviewer changed.

## Step 3 — Run the compact behavioural baseline

### Objective

Use the existing red-team suite to establish how the current application behaves across meaningful failure modes without turning the project into an eval platform.

### Work

- Keep the approximately 15-case suite because the datasets and runner already exist.
- Sharpen E06 so it tests genuinely opposing preferences about the same automated action.
- Rewrite E09 so narrow representation is not confounded with exact duplicate wording.
- Define E12 as an **isolated signal requiring investigation**, not a recurring theme.
- Add simple checks for malformed responses, failed calls and export integrity.
- Make acceptance criteria concrete for each case: what must be present, what must not happen, acceptable variation and supporting evidence.
- Keep Pass / Partial / Fail, observed severity and written reasoning. Do not rely on one overall percentage.
- Repeat important model cases, including apparent passes, before drawing stronger conclusions.

### Completion condition

The important behavioural failures have inspectable examples, clear severity and enough repeated evidence to prioritise a bounded improvement cycle.

## Step 4 — One bounded improvement cycle + practitioner validation

### Objective

Improve the most consequential observed weaknesses while testing whether the workflow actually helps the intended user.

### Product improvements

Prioritise observed failures rather than theoretical completeness. Likely interventions include:

- prompt-injection handling;
- evidence-strength presentation based on observable support and source breadth;
- groundedness and contradiction handling;
- theme separation without over-fragmentation;
- making potential opportunities editable/challengeable;
- allowing a reviewer to record a missing observation and inspect uncited records.

Prompt `v2` belongs here. Compare it across the separation and fragmentation cases together rather than tuning it only to recover the known payment theme.

### Practitioner validation

Run approximately three short sessions with PMs, POs or BAs. Use comparable tasks and, where practical, vary task order or dataset to reduce familiarity effects.

Measure directionally:

- time to a reviewed, usable output;
- important problems missed;
- unsupported claims retained;
- whether the participant can explain and defend the resulting conclusions;
- what they corrected, rejected or added.

Acceptance rate alone is not a success measure because high acceptance can represent either useful output or uncritical trust.

### Completion condition

There is evidence about both product behaviour and whether practitioners gain a useful quality or time advantage. If they do not, narrow or stop further feature work rather than adding more evaluation machinery.

## Step 5 — Recheck and publish

### Objective

Close the learning loop and turn the work into a concise product case study.

### Work

- Rerun the same behavioural cases after the bounded improvement cycle.
- Preserve regressions and remaining high-severity failures, not only improvements.
- Use one fresh holdout dataset with different language or subject matter that has not been repeatedly tuned against.
- If the holdout is used to improve the product, treat it as development data and create another holdout before making generalisation claims.
- Summarise practitioner findings without overstating three sessions as general proof.
- Publish a concise before/after account: what changed, why it mattered, whether reviewers benefited and what still failed.

### Completion condition

The portfolio claims match the evidence, remaining weaknesses are visible, and any further work has a clear product reason.

## Evaluation principles from this point

- The current OpenAI-backed application configuration is the baseline for future before/after experiments; the Gemini benchmark remains historical evidence rather than a directly comparable baseline.
- The human reference is useful for repeatability but remains contestable.
- Theme count is not a quality target: useful distinctions may be top-level themes or subthemes depending on the product decision they support.
- RAG remains deferred because retrieval infrastructure is not presently justified; this is not a claim that retrieval has been proven reliable.
- SQL is optional supporting analysis. Introduce SQLite/SQL only when recurring questions across versions, cases and runs become awkward in JSON/CSV.
- Do not build a standalone SQL portfolio project or a large AI-evaluation platform.

## Not building yet

- Autonomous roadmap generation
- Automatic feature prioritisation
- Unsupervised product decisions
- Production-scale infrastructure
- Customer-data integrations
- RAG or vector storage without a demonstrated retrieval problem
- A standalone SQL portfolio project
- A large AI-eval engineering platform

## Current product question

> Can an LLM help a product practitioner reach a useful, defensible analysis of qualitative feedback faster while preserving evidence traceability and human judgement?

The next portfolio milestone is not a larger benchmark. It is a completed learning cycle showing what failed, what changed, whether practitioners benefited and what remains uncertain.