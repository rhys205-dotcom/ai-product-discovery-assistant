# AI Product Decisions

This document records the product and technical decisions behind the AI Product Discovery Assistant and how those decisions changed when evaluation exposed new evidence.

## Standing principles

### 1 — AI assists rather than decides
The system may identify patterns, summarise evidence and suggest investigation opportunities. It does not autonomously decide what to build, how to prioritise, or what belongs on a roadmap.

### 2 — Separate evidence, interpretation and recommendation
Customer statements, model interpretation and proposed action are different layers. The interface and exports should keep them distinguishable.

### 3 — Require traceability to source evidence
Findings cite feedback IDs and reviewers can inspect the source text before accepting them.

### 4 — Do not treat model confidence as evidence
No confidence percentage is shown. If a Strong/Moderate/Limited label is retained, the interface should expose observable support such as cited record count, source/persona breadth, suspected duplication and qualification.

### 5 — Keep retrieval infrastructure deferred
RAG/embeddings/vector storage are not presently justified because current datasets are supplied directly to the model. Revisit only if realistic input size, targeted search or measured omission creates a retrieval problem that simpler batching cannot address.

### 6 — Use synthetic data for public work
The public prototype and evaluation data are synthetic so the project can be inspected without exposing former-employer/customer information.

### 7 — Prefer structured output and validate it
Schema-constrained output supports comparison, review and integration, but application-side validation still rejects malformed/incomplete responses.

### 8 — Evaluate repeated behaviour, not polished demos
Individual good-looking outputs are not evidence of reliability. Repeated cases, preserved weak runs and written severity judgements matter more.

### 9 — Human review must include recommendations and omissions
The reviewer should be able to challenge what the model says, its proposed opportunity and—where the product contract allows—what it might otherwise omit.

### 10 — Treat prompts as versioned product components
Material prompt/contract changes are named, documented and rerun against the same cases.

## Evaluation decisions

### 11 — Do not optimise for a predetermined theme count
The original reference's three themes remain a contestable human judgement. Theme separation is useful only where the distinction changes investigation or action. Prompt changes should not simply teach the model the known synthetic answer.

The independent blind reference review remains useful but is a trailing, non-blocking activity. Prompt v2 is evaluated against multiple cases—including separation and fragmentation—rather than against one missing reference theme.

### 12 — Repair scorer blind spots before stronger quantitative claims
Scorer v2:
- checks citations across all findings;
- scores relevance per finding–citation relationship;
- surfaces unmatched findings;
- preserves duplicate mappings; and
- adds qualification precision.

Historical v1 metrics remain published as historical evidence, with their limitations made explicit.

### 13 — Fix deterministic evidence-integrity failures early
Blank/duplicate IDs, stale dataset state and stale reviewer decisions undermine the core promise of evidence traceability. These were captured before repair and then fixed before the behavioural baseline.

### 14 — Keep the red-team suite compact and diagnostic
E01–E15 are a development aid, not an eval platform. Important cases are repeated, failures are recorded by type/severity, and no overall percentage is used as a substitute for judgement.

### 15 — Move practitioner validation into the bounded improvement cycle
The core hypothesis includes usefulness and speed. Approximately three PM/PO/BA sessions should measure time to reviewed output, important omissions, unsupported claims retained, and whether conclusions can be explained and defended.

### 16 — Hold one application configuration fixed for before/after comparisons
The current baseline and prompt-v2 comparison use the Gemini-backed application path with the same model/request approach apart from the intended prompt/contract change.

The earlier Gemini benchmark remains historical because it used a different benchmark runner/request path. Same provider/model family does not make the experiments directly comparable.

### 17 — Preserve a fresh holdout
After the improvement cycle, use a dataset with different language/domain that has not been repeatedly tuned against. Once a holdout is used to change the product, it becomes development data.

### 18 — SQL is supporting analysis, not a portfolio objective
Use SQLite/SQL only if recurring questions across versions/cases/runs become awkward in JSON/CSV. Do not build a standalone SQL project for appearance.

## Decisions from the behavioural baseline

### 19 — Add a separate contract for isolated material signals

**Evidence**

E12 failed in all three baseline observations. Two runs omitted a one-off report of possible cross-account record access because it did not fit recurring-theme logic. One run surfaced it but overstated certainty as a critical vulnerability and jumped to an urgent security audit.

**Decision**

Prompt/contract v2 adds `isolated_signals` separately from recurring themes.

An isolated signal records:
- the observation;
- cited evidence IDs;
- why it may matter;
- what remains uncertain; and
- a verification/investigation next step.

It must not turn one report into a confirmed incident or autonomous roadmap decision.

**Why**

Frequency and importance are different dimensions. A rare potentially material observation should not disappear merely because the main analysis is designed around recurring problems.

### 20 — Detect exact repeated evidence deterministically

**Evidence**

E08 failed in all three observations. Five identical records from the same source/persona were repeatedly presented as Strong independent-looking support, and the model added plausible but unsupported technical causes such as webhook/sync latency.

**Decision**

The application flags exact repetition of feedback text + source + persona before model analysis and passes those possible duplicate groups into the prompt and run metadata.

The UI exposes the groups to the reviewer. Repeated IDs must not be treated as proof of independent customers or stronger consensus merely because there are more rows.

**Why**

This is cheaper, more reliable and more transparent than hoping the model infers duplication from raw text every time. Exact repetition does not prove one respondent, so the product labels it possible duplicate evidence rather than deduplicating or deleting it automatically.

### 21 — Define contradiction narrowly and strengthen groundedness

**Evidence**

E07 misclassified non-use/non-exposure as contradiction in two of three observations. E11 was mostly grounded but one repeat added unsupported consequences. E08 repeatedly invented technical causes.

**Decision**

Prompt v2 states:
- contradiction requires a genuinely opposing experience/preference/claim about the same problem;
- non-use/non-exposure is neutral or non-applicable;
- do not invent technical causes, averages, business impact, causal consequences or implementation details.

Contradictory/qualifying evidence is displayed as readable source material in the review UI.

**Why**

A valid evidence ID can still support the wrong semantic role. The product needs clearer qualification rules, not just valid citations.

### 22 — Make abstention an explicit valid outcome

**Evidence**

E02 and E13 showed a tendency to manufacture broad UI themes from heterogeneous one-off requests. E13 failed in all three reviewed observations.

**Decision**

Prompt v2 explicitly allows `themes: []` and requires a coherent repeated customer problem rather than broad category similarity.

**Why**

The product is more trustworthy when it can say there is no recurring pattern than when it produces a tidy but weak theme for every dataset.

### 23 — Improve reviewability rather than adding architecture

**Decision**

During the same bounded cycle:
- show observable support counts alongside the model's strength label;
- flag possible exact duplicates in cited evidence;
- show contradictory/qualifying evidence as source text;
- make potential opportunities editable;
- allow isolated signals to be reviewed and edited; and
- preserve reviewed isolated signals separately from original model output.

Do not add RAG, agents, another provider, SQL infrastructure or a large eval framework to address failures they do not solve.

**Why**

The measured problems are evidence handling, omission, qualification and reviewer challengeability—not retrieval or infrastructure scale.

## Current architecture principle

Use the simplest architecture capable of testing the product hypothesis:

**Structured feedback**

↓

**Deterministic validation / duplicate-evidence checks**

↓

**LLM analysis**

↓

**Recurring themes + isolated signals**

↓

**Evidence inspection**

↓

**Human review**

Add complexity only where measured product evidence justifies it.

## Current open questions

- Does prompt/contract v2 improve E07/E08/E12/E13 without regressing E03–E06, E09–E11?
- Does the separate isolated-signal lane produce appropriately cautious investigation language?
- Does exposing observable support change reviewer trust in Strong/Moderate/Limited labels?
- Can practitioners reach a reviewed, defensible analysis faster or with fewer unsupported claims?
- Which theme distinctions actually change the next product investigation or decision?
- At what dataset size/task does retrieval add value over direct analysis or batching?

## Current status

| Area | Current position |
|---|---|
| Role of AI | Assist, not decide |
| Evidence traceability | Implemented and smoke-tested |
| Human review | Findings, opportunities and isolated signals reviewable; omission handling still incomplete |
| Evidence strength | Model label retained but observable basis exposed |
| Historical benchmark | Preserved with frozen prompt-v1 runner |
| Human reference | Contestable; blind review trailing |
| Scorer | v2 implemented |
| Behavioural baseline | Step 3 complete |
| Prompt / contract | v2 implemented; before/after verification next |
| Practitioner validation | Next within Step 4 |
| Fresh holdout | Step 5 |
| RAG / embeddings | Deferred |
| SQL | Optional supporting analysis only |
