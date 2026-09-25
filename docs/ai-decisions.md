# AI Product Decisions

This document records the key AI-related product and technical decisions made during the development of the AI Product Discovery Assistant.

The purpose is to make the reasoning behind the product visible and to record how decisions evolve as the application is tested.

---

## Decision 1 — AI assists rather than decides

### Decision

The system will use AI to identify patterns, summarise evidence and suggest potential product opportunities.

It will not autonomously decide:

- which problems should be solved
- which features should be built
- how opportunities should be prioritised
- what should appear on a product roadmap

### Why

Product decisions require context that may not exist within a customer-feedback dataset, including strategy, commercial value, technical feasibility, regulation, operations, dependencies, cost and wider evidence.

The AI therefore acts as an analytical assistant rather than a decision-maker.

---

## Decision 2 — Separate evidence, interpretation and recommendation

### Decision

AI output will distinguish between:

1. **Evidence** — what customers actually said
2. **Interpretation** — what the AI believes the evidence indicates
3. **Recommendation** — what the AI suggests could be investigated

### Why

Large Language Models can produce convincing conclusions even when those conclusions are weakly supported. The interface and structured output should preserve this distinction.

---

## Decision 3 — Require traceability to source evidence

### Decision

Generated themes and pain points should reference the feedback records that support them, and users should be able to inspect those records before accepting a finding.

### Why

Traceability increases challengeability, exposes hallucination and supports human review. A plausible answer is not sufficient.

---

## Decision 4 — Do not use model confidence as evidence strength

### Decision

The application will not present model-generated confidence percentages as evidence.

Evidence strength should instead be grounded in observable support such as cited record count, source/persona breadth, consistency, relevance, suspected duplication and important qualifications.

### Why

A model stating that it is highly confident does not calibrate the probability that a finding is correct. Even labels such as Strong/Moderate/Limited can become falsely authoritative if their basis is hidden.

If a strength label is retained, its observable basis should be visible and challengeable.

---

## Decision 5 — Keep retrieval infrastructure deferred

### Decision

Do not add RAG, embeddings or vector storage to the current MVP unless a measured problem shows that retrieval would help.

### Why

The current evaluation datasets are supplied directly to the model. The project therefore has not established a retrieval-stage success or failure. The defensible conclusion is simply that retrieval infrastructure is **not presently justified**.

If realistic input sizes, targeted search needs or measured omissions later create a retrieval problem, compare retrieval with simpler alternatives such as batching before increasing architectural complexity.

---

## Decision 6 — Use synthetic data initially

### Decision

The public demonstration will use synthetic customer feedback.

### Why

Real feedback may contain personal, confidential or commercially sensitive information. Synthetic data enables public demonstration while still allowing realistic contradictions, distractors and failure cases.

---

## Decision 7 — Structured output over unrestricted prose

### Decision

Where possible, the model should return findings using a defined structure rather than unrestricted narrative output.

### Why

Structured output supports validation, consistent display, comparison, evaluation and integration.

The application still needs to validate required fields and failure states rather than treating any object containing a `themes` list as complete.

---

## Decision 8 — Evaluate output rather than relying on demos

### Decision

The project will evaluate AI-generated findings rather than treating a polished demonstration as evidence of reliability.

Initial dimensions include coverage, groundedness, evidence integrity, qualification and behavioural integrity.

### Why

Generative AI can produce impressive individual examples while behaving inconsistently across repeated tasks.

---

## Decision 9 — Maintain human review, including omissions

### Decision

Generated findings will be presented for review rather than automatically accepted.

Human oversight should eventually cover not only shown findings but also omissions and recommendations. A reviewer should be able to challenge the opportunity, record a missing observation and distinguish original output from edits.

### Why

Human review is strongest only when the reviewer can correct what the model said **and** what it failed to say. This is especially important because omission is already a measured failure mode.

---

## Decision 10 — Treat prompts as product components

### Decision

Prompts will be treated as versioned product components. Material prompt changes should be documented and evaluated.

### Why

Prompt changes can alter output quality, evidence selection, structure, hallucination and consistency.

---

## Decision 11 — Do not optimise the prompt to reproduce one known reference

### Evidence

The first controlled Gemini benchmark measured 100% citation validity, 95.5% mean evidence precision, 88.5% mean reference evidence coverage and 66.7% mean theme coverage. All three runs omitted the smaller payment communication and audit-history reference theme.

A later review highlighted that the reference itself is a documented human judgement. Some records assigned to the third theme also plausibly support the broader payment-status problem.

### Decision

Theme separation remains worth testing, but recovering one predetermined top-level theme is not itself the product goal.

Before using prompt `v2` as evidence of improvement:

- challenge the reference with at least one independent practitioner;
- allow useful subthemes as well as top-level themes;
- test separation and fragmentation together;
- avoid explicitly telling the model which known payment theme to find.

### Why

Optimising directly against a known synthetic reference risks overfitting and can reward more themes rather than better analysis.

---

## Decision 12 — Repair evaluation blind spots before expanding quantitative claims

### Evidence

Review of the current scorer found that unmatched generated findings can escape headline scoring, citations attached to unknown themes can escape main citation checks, duplicate mappings can overwrite one another and aggregated unique citation counts can hide incorrect use of an ID in one finding when it is correct elsewhere.

The existing published benchmark numbers still reproduce for the saved runs; these limitations narrow what the numbers establish rather than invalidating the historical experiment.

### Decision

Before making stronger quantitative claims:

- inspect citations across all generated findings;
- evaluate relevance per finding–citation relationship;
- explicitly surface unmatched findings for human review;
- prevent duplicate mappings from silently overwriting one another;
- keep the human reference contestable rather than treating unmatched findings as automatically wrong.

### Why

A metric should not become a product target until its blind spots are understood.

---

## Decision 13 — Capture and fix evidence-integrity failures early

### Evidence

The current upload parser can accept blank or duplicate IDs, and the evidence lookup uses feedback ID as a dictionary key. The current application also retains analysis in session state when the uploaded dataset changes, creating a risk that old findings can be displayed against new records with reused IDs. Review controls use positional keys, which can also allow stale reviewer state to persist.

### Decision

Record these failures as baseline evidence, then repair them promptly rather than waiting for every model red-team case to finish.

Required trust controls include:

- unique, non-blank feedback IDs;
- dataset identity bound to analysis and review state;
- stale result invalidation;
- response validation;
- original-versus-edited output preservation;
- dataset/run provenance in exports;
- explicit handling of failed calls and invalid outputs.

### Why

These are product-integrity failures, not optional model-quality refinements. They undermine the promise that findings remain traceable to the evidence a reviewer actually inspected.

---

## Decision 14 — Keep the red-team suite compact and diagnostic

### Decision

Retain the approximately 15-case red-team suite because it is already built and covers useful failure classes, but treat it as a compact development tool rather than a research programme.

Refine cases where needed:

- E06 should test genuinely opposing preferences about the same automated action.
- E09 should test narrow representation without using exact duplicates as the confounder.
- E12 should expect an **isolated signal requiring investigation**, not a recurring theme.
- Important cases should be repeated even when the first run passes.
- Broken model responses and export integrity should also be checked.

### Why

The aim is to expose consequential product behaviour and prioritise improvements, not to maximise the number of eval artefacts.

---

## Decision 15 — Move practitioner validation forward

### Decision

Do not defer usability/value validation until after multiple additional evaluation releases.

Run approximately three short sessions with PMs, POs or BAs during the next bounded improvement cycle.

Measure directionally:

- time to a reviewed, usable output;
- unsupported claims retained;
- important problems missed;
- whether the participant can explain and defend the conclusion;
- what they correct, reject or add.

### Why

The core product hypothesis includes usefulness and speed. Model behaviour can be well measured while the workflow still provides little practical advantage.

If practitioners do not gain useful time or quality, the product should be narrowed or further feature work stopped rather than justified through more eval sophistication.

---

## Decision 16 — Use one application configuration for future comparisons

### Decision

Future before/after experiments should use the current application configuration and hold the relevant model/request settings constant.

The earlier Gemini benchmark remains a separately labelled historical experiment and should not be treated as a clean baseline for changes to the OpenAI-backed application.

### Why

The historical benchmark and application use different providers and request/validation configurations. A clean product comparison requires the configuration under test to remain stable apart from the intended change.

---

## Decision 17 — Preserve one fresh holdout

### Decision

After the bounded improvement cycle, test behaviour on a fresh dataset with different language or subject matter that has not been repeatedly tuned against.

If that dataset is used to improve the product, it becomes development data and another holdout is required before making stronger generalisation claims.

### Why

The original benchmark and several adversarial cases share payment language and product assumptions. More synthetic cases do not automatically create independent evidence.

---

## Decision 18 — SQL is supporting analysis, not a separate project

### Decision

Do not create a standalone SQL portfolio exercise.

SQLite/SQL may be introduced only when recurring analytical questions across versions, cases and runs are awkward to answer from JSON/CSV.

### Why

SQL adds value when it answers a real product question. Its presence alone adds little portfolio value.

---

# Current Architecture Principle

Use the simplest architecture capable of testing the product hypothesis:

**Structured feedback**

↓

**LLM analysis**

↓

**Structured findings**

↓

**Evidence validation**

↓

**Human review**

Add complexity only where measured product evidence justifies it.

---

# Open Questions

- Can practitioners reach a useful, defensible analysis faster with this workflow?
- Which theme distinctions materially change the next investigation or decision?
- How should evidence strength expose breadth, duplication and qualification?
- How should contradictory, neutral and non-applicable evidence be distinguished?
- How should low-frequency/high-severity signals be surfaced without calling them recurring themes?
- How should human corrections and missing observations be preserved?
- How should the product defend against instructions embedded in untrusted feedback?
- At what dataset size or task does retrieval add value over direct analysis or batching?
- What transparency is genuinely useful to a Product Manager rather than merely impressive in a demo?

---

# Decision Log

| Decision | Current Position | Status |
|---|---|---|
| Role of AI | Assist, not decide | Accepted |
| Evidence traceability | Required | Accepted; trust fixes now prioritised |
| Human review | Include shown findings, omissions and reviewer provenance | Partially implemented |
| Evidence strength | Prefer observable basis over model authority | Improvement planned |
| Synthetic public data | Use for public prototype | Implemented |
| Structured outputs | Preferred and must be validated | Validation improvement planned |
| RAG / embeddings | Not presently justified | Deferred |
| Historical Gemini benchmark | Useful but separately labelled | Completed v0.4 |
| Human reference | Repeatable but contestable | Independent review planned |
| Evaluation scorer | Useful with known blind spots | Repair now |
| Red-team suite | Compact diagnostic baseline | Built; refinement/runs pending |
| Trust failures | Record then fix promptly | Current priority |
| Prompt v2 | One intervention in bounded improvement cycle | Later, after baseline/reference review |
| Practitioner validation | Test practical usefulness during improvement cycle | Moved forward |
| Fresh holdout | Use after improvement cycle | Planned |
| SQL | Use only when analysis requires it | Optional / deferred |

This document will evolve as the product is tested and new evidence becomes available.
