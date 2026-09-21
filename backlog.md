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

## Now — v0.5: Controlled prompt comparison

### Hypothesis

A prompt that explicitly asks the model to distinguish related but independently actionable customer problems will improve coverage of the smaller communication and audit-history theme without materially reducing evidence quality.

### Experimental controls

- Preserve prompt `v1` and the v0.4 results unchanged.
- Create a separately versioned prompt `v2`.
- Keep the dataset, model and three-run protocol fixed.
- Preserve the unmodified model response separately from human mapping and calculated scores.
- Report all runs, including weak or failed outputs.

### Success criteria

- Identify `T03` in at least two of three runs.
- Maintain 100% citation validity.
- Keep evidence precision at or above 93%, the lowest v1 run.
- Do not promote a deliberate distractor into a core theme.
- Record qualitative failure modes and any regression, not only the headline averages.

The experiment will provide evidence about prompt behaviour on this fixed dataset. It will not establish general performance across different datasets or models.

## Next — usability and generalisation

- Preserve reviewer edits as structured evaluation data.
- Test whether the workflow saves time for a product practitioner.
- Test a larger and more diverse synthetic dataset.
- Compare model variants only after the prompt experiment is complete.
- Improve error handling for malformed or oversized uploads.
- Add screenshots or a short walkthrough to the repository.

## Later — only if evidence supports it

- Add retrieval or embeddings if direct analysis no longer returns relevant evidence reliably.
- Explore configurable evidence-strength rules.
- Test multi-reviewer agreement.
- Investigate integrations only after the core review workflow proves useful.

## Not building yet

- Autonomous roadmap generation
- Automatic feature prioritisation
- Unsupervised product decisions
- Production-scale infrastructure
- Customer-data integrations
- RAG or vector storage without an evaluated retrieval problem

## Current product question

> Can an LLM help a product practitioner analyse qualitative feedback faster while preserving evidence traceability and human judgment?

The next release will test a diagnosed failure mode through a controlled prompt comparison rather than adding more demo features.
