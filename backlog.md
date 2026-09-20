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

## Now — v0.3: Controlled benchmark

### Run repeated analyses

Run the unchanged dataset and prompt at least three times, recording the model and prompt version with every raw result.

**Why:** One convincing output does not demonstrate repeatability.

**Success looks like:** Variation in themes, citations, missed evidence and unsupported claims is visible rather than anecdotal.

### Review and report the scores

Map generated themes to the human reference through explicit human review, run the scorer and inspect qualitative failure modes alongside the numbers.

**Why:** Automated scores cannot determine whether a finding is useful or whether the human reference itself is contestable.

**Success looks like:** Every run is reported, including weak outputs, with a documented decision about the next experiment.

## Next — v0.4: Comparison and usability

- Record prompt and model version with every analysis.
- Compare prompt variants against the same reference dataset.
- Preserve reviewer edits as structured evaluation data.
- Test whether the workflow saves time for a product practitioner.
- Improve error handling for malformed or oversized uploads.
- Add screenshots or a short walkthrough to the repository.

## Later — only if evidence supports it

- Test larger and more diverse datasets.
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

The next release should answer part of that question with measured results, not additional demo features.
