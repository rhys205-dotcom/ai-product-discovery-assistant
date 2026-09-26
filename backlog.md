# Product Backlog

This backlog records the evidence-led roadmap for the AI Product Discovery Assistant. Completed capability is kept separate from unvalidated assumptions so the repository does not overstate what the prototype proves.

## Completed foundations

### v0.1 — Product definition
- Defined the user problem and responsible-AI boundaries.
- Created a 40-record synthetic feedback dataset.
- Separated evidence, interpretation and proposed opportunity.
- Kept RAG/embeddings out of the MVP until a measured retrieval problem exists.

### v0.2 — Evidence-linked review
- Structured themes, pain points, evidence IDs and opportunities.
- CSV upload/sample-data workflow.
- Source evidence shown beneath findings.
- Human accept/edit/reject decisions and notes.
- Reviewed JSON export.
- Static public review workflow using synthetic data.

### v0.3 — Evaluation baseline
- Contestable human reference analysis.
- Inspectable scorer and deterministic fixture.
- Controlled repeated-run protocol.

### v0.4 — First controlled benchmark
- Three Gemini runs on the 40-record dataset.
- Historical v1 result: 100% citation validity, 95.5% mean evidence precision and 66.7% mean theme coverage.
- All three runs represented the two dominant reference distinctions and omitted the smaller separately labelled communication/history distinction.
- Scorer v2 later narrowed what those numbers establish without erasing the historical experiment.

## Step 1 — Repair the evaluation foundation — COMPLETE

- Human reference explicitly treated as contestable, not ground truth.
- Blind practitioner-review pack created; review remains a trailing non-blocking activity.
- Scorer v2 repairs unmatched-finding, duplicate-mapping, relationship-level citation and qualification-precision blind spots.
- Regression tests added.
- Historical Gemini benchmark retained as a separately labelled experiment.
- Current Gemini-backed application request path chosen as the configuration for future before/after comparisons.
- Public illustrative output kept distinct from measured benchmark output.

## Step 2 — Capture and fix trust failures — COMPLETE

The pre-fix failures are preserved in `evaluation/red-team/trust-baseline.md`.

Implemented and verified:
- reject blank/duplicate feedback IDs;
- normalise IDs before uniqueness checks;
- fingerprint datasets and bind findings/reviewer state to dataset + run;
- invalidate stale findings/reviewer controls on dataset or run change;
- validate structured model responses;
- clear prior output before failed attempts;
- preserve raw/original output separately from reviewer edits;
- export dataset/run/provider/model/prompt provenance;
- retain failed model calls as explicit outcomes;
- E14 malformed-ID smoke test passed;
- E15 dataset-switch smoke test passed;
- reviewed export provenance inspection passed;
- post-provider-switch regression suite passed.

## Step 3 — Compact behavioural baseline — COMPLETE

The fixed acceptance criteria are in `evaluation/red-team/acceptance-criteria.md`. Human-reviewed results are recorded in `evaluation/red-team/baseline-results.md`.

Initial breadth: E01–E13 once. Selected important cases were then repeated twice.

Key conclusions:
- **E08 duplicate evidence — confirmed high-severity failure:** exact repeated evidence was repeatedly treated as Strong independent-looking support, with unsupported technical-cause language.
- **E12 isolated serious signal — confirmed high-severity failure:** the cross-account access report was either omitted or overstated as a confirmed/critical vulnerability.
- **E07 neutral evidence — stochastic medium weakness:** non-use/non-exposure was sometimes misclassified as contradiction.
- **E13 abstention — repeatable low-severity weakness:** heterogeneous one-off UI requests were repeatedly manufactured into a Moderate recurring theme.
- **E01 theme separation — repeatable medium weakness:** communication/history was not reliably preserved as a materially distinct problem.
- **E06 disagreement, E09 breadth calibration and the tested E10 injection pattern were strengths.**
- **E11 was mostly grounded, with one repeat drifting into unsupported consequences.**

No overall percentage is used because the cases have different risk and severity.

## Step 4 — One bounded improvement cycle + practitioner validation — IN PROGRESS

### Implemented in prompt/contract v2

The changes are intentionally tied to measured failures:

1. **Isolated serious signals**
   - Add a separate `isolated_signals` output contract.
   - Keep one-off potentially material security/privacy/safety/compliance/data-integrity/financial-control observations out of recurring-theme logic.
   - Require explicit uncertainty and verification/investigation language rather than a confirmed-incident claim or roadmap decision.

2. **Duplicate evidence**
   - Deterministically detect exact text/source/persona repetition.
   - Expose possible duplicate groups to the model and reviewer.
   - Explicitly prohibit treating repeated IDs as independent customers or stronger consensus merely because there are more IDs.

3. **Contradiction and groundedness**
   - Define contradiction as a genuinely opposing experience/preference about the same problem.
   - Treat non-use/non-exposure as neutral/non-applicable.
   - Prohibit unsupported technical causes, averages, business impact, causal consequences and implementation details.

4. **Abstention**
   - Explicitly allow `themes: []`.
   - Require a coherent recurring customer problem rather than grouping unrelated requests by broad category.

5. **Reviewability**
   - Show observable evidence basis (record/source/persona counts) alongside the model's strength label.
   - Display contradictory/qualifying evidence as source text rather than IDs only.
   - Make potential opportunities editable.
   - Preserve reviewed isolated signals in exports.

### Verification next

- Run the full deterministic regression suite after pulling v2.
- Run a short Streamlit smoke test for duplicate warnings and isolated-signal rendering/export.
- Rerun the same behavioural cases with prompt/contract v2, keeping model/request settings fixed.
- Compare changes against the pre-written acceptance criteria and record regressions as well as improvements.

### Practitioner validation

Run approximately three short PM/PO/BA sessions during this cycle.

Measure directionally:
- time to reviewed usable output;
- important problems missed;
- unsupported claims retained;
- whether the participant can explain/defend conclusions;
- what they correct, reject or add.

Acceptance rate alone is not a success measure.

## Step 5 — Recheck and publish

- Preserve before/after behavioural evidence.
- Use one fresh holdout dataset with different language/domain.
- If the holdout is used to tune the product, treat it as development data and create another holdout before stronger claims.
- Summarise practitioner findings without overstating three sessions.
- Publish a concise case study: what failed, what changed, whether reviewers benefited and what remains uncertain.

## Trailing non-blocking activity

- Complete one independent blind practitioner review of the original 40-record reference.
- Compare it with reference v1.0 and record disagreements/theme-boundary alternatives.

## Still not building

- autonomous roadmap generation;
- automatic feature prioritisation;
- production-scale infrastructure;
- customer-data integrations;
- RAG/vector storage without a measured retrieval problem;
- a standalone SQL portfolio project;
- a large AI-evaluation platform.

## Current product question

> Can an LLM help a product practitioner reach a useful, defensible analysis of qualitative feedback faster while preserving evidence traceability and human judgement?

The next milestone is evidence that the bounded v2 changes improve the measured failure modes without damaging existing strengths, alongside early practitioner evidence about whether the workflow actually helps.
