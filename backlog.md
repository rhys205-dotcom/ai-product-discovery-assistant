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
- Identified a repeatable failure: all three runs missed the smaller payment communication and audit-history theme.
- Deferred RAG because the evidence indicates a theme-separation problem rather than a retrieval problem.

## Completed — product red-team

A broader product red-team was carried out after the first benchmark. It found that the original benchmark is useful but too narrow to assess several important failure modes.

Priority risks identified include:

- prompt injection embedded inside customer feedback;
- duplicate or blank feedback IDs breaking traceability;
- stale analysis remaining visible after the underlying dataset changes;
- duplicate feedback manufacturing false consensus;
- evidence-strength labels overstating weak or narrow evidence;
- unsupported embellishment inside otherwise valid themes;
- neutral evidence being misclassified as contradictory;
- low-frequency but high-severity signals being hidden by frequency-based theme detection;
- related problems being over-merged;
- one problem being over-fragmented into several artificial themes.

This changed the next milestone. The project will establish behaviour across these failure modes before optimising the prompt against the known 40-record benchmark.

## Now — v0.5: Red-team evaluation suite

### Objective

Create a compact adversarial evaluation suite that tests whether the current product remains evidence-faithful and safe enough for human-assisted discovery when the inputs are ambiguous, conflicting, duplicated, malformed or adversarial.

### Baseline rule

Freeze the current prompt and behaviour as the baseline. Run the suite before fixing the diagnosed weaknesses so failures are recorded rather than designed away retrospectively.

### Planned cases

The first suite will contain roughly 15 deliberately small test cases covering:

1. the existing 40-record benchmark;
2. no meaningful recurring pattern;
3. a smaller recurring theme at risk of being swamped;
4. two similar but independently actionable problems;
5. one underlying problem expressed through several requested solutions;
6. genuine disagreement about automation;
7. neutral or non-applicable evidence that should not be treated as contradiction;
8. duplicated feedback that should not manufacture consensus;
9. evidence dominated by one persona or source;
10. prompt injection embedded in a feedback record;
11. a correct theme with tempting unsupported statistics or causal claims;
12. a low-frequency but high-severity signal;
13. isolated cosmetic requests that should remain noise;
14. duplicate or blank feedback IDs that break traceability;
15. an analysis generated from dataset A remaining visible after switching to dataset B.

### Initial scoring

Keep the first red-team framework deliberately lightweight. For each case record:

- **Coverage** — did the analysis identify what mattered?
- **Groundedness** — are substantive claims supported by the supplied evidence?
- **Evidence integrity** — are citations relevant and traceable?
- **Qualification** — are disagreement, uncertainty and important limits preserved?
- **Behavioural integrity** — does the product resist injection, duplication, stale state and malformed inputs?
- **Outcome** — Pass / Partial / Fail.
- **Failure severity** — Low / Medium / High.

Manual review is acceptable at this stage. The objective is to expose product failure modes, not to build a large automated eval platform.

## Next — v0.6: Targeted improvements

Prioritise changes using the observed baseline failures rather than fixing every theoretical weakness.

Likely areas include:

- dataset validation and unique-ID enforcement;
- binding an analysis to the dataset that produced it and invalidating stale results;
- stronger separation of instructions from untrusted feedback content;
- revised treatment of evidence strength and source diversity;
- improved theme separation without creating over-fragmentation;
- stronger handling of unsupported claims and false contradictions;
- clearer treatment of low-frequency/high-severity signals;
- making the proposed opportunity as reviewable as the interpretation.

The previously planned `v2` prompt comparison remains useful, but it becomes one targeted intervention inside this milestone rather than the whole milestone.

## Then — v0.7: Regression evaluation

Rerun the same red-team suite after the targeted changes.

Compare before and after behaviour, including regressions. Do not report only aggregate improvements: preserve high-severity failures and qualitative differences between versions.

If the number of runs becomes large enough to justify it, store structured results in SQLite and use SQL to answer practical product questions such as:

- Which failure modes improved or regressed?
- Which high-severity failures remain?
- Does improved theme separation create more fragmentation?
- Are failures consistent or intermittent across repeated runs?

SQL is supporting analysis here, not a separate portfolio project.

## Later — usability and generalisation

- Preserve reviewer edits as structured evaluation data.
- Test whether the workflow saves time for a product practitioner.
- Test larger and more diverse synthetic datasets.
- Compare model variants after behaviour is better understood.
- Test multi-reviewer agreement.
- Add retrieval or embeddings only if direct analysis no longer returns relevant evidence reliably.
- Investigate integrations only after the core review workflow proves useful.

## Not building yet

- Autonomous roadmap generation
- Automatic feature prioritisation
- Unsupervised product decisions
- Production-scale infrastructure
- Customer-data integrations
- RAG or vector storage without an evaluated retrieval problem
- A standalone SQL portfolio project
- A large AI-eval engineering platform

## Current product question

> Can an LLM help a product practitioner analyse qualitative feedback faster while preserving evidence traceability, calibrated interpretation and human judgement across realistic failure modes?

The next release will establish a red-team baseline before making targeted improvements.