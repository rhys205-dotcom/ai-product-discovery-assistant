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

Product decisions require context that may not exist within a customer-feedback dataset.

This can include:

- business strategy
- commercial value
- technical feasibility
- regulatory constraints
- operational impact
- dependencies
- cost
- wider customer evidence

The AI therefore acts as an analytical assistant rather than a decision-maker.

---

## Decision 2 — Separate evidence, interpretation and recommendation

### Decision

AI output will distinguish between three levels:

1. **Evidence** — what customers actually said
2. **Interpretation** — what the AI believes the evidence indicates
3. **Recommendation** — what the AI suggests could be investigated

### Why

Large Language Models can produce convincing conclusions even when those conclusions are weakly supported.

Presenting all AI output in the same way could cause users to mistake an AI inference for customer evidence.

The interface and structured output should therefore preserve this distinction.

---

## Decision 3 — Require traceability to source evidence

### Decision

Generated themes and pain points should reference the feedback records that support them.

For example:

> Theme: Manual reconciliation creates significant effort  
> Evidence: F002, F007, F014, F021

Users should be able to inspect those records before accepting the finding.

### Why

Traceability:

- increases user trust
- makes findings easier to challenge
- helps identify hallucination
- allows users to understand why a conclusion was generated
- supports human review

A plausible answer is not sufficient. The system should be able to show the evidence behind it.

---

## Decision 4 — Do not use model confidence as evidence strength

### Decision

The application will not simply ask the LLM to assign its own confidence score to a finding.

Evidence strength should instead be based on observable factors such as:

- number of supporting feedback records
- diversity of sources
- consistency of the underlying feedback
- relevance of the supporting evidence

### Why

An LLM stating that it is "95% confident" does not necessarily mean that a finding has a 95% probability of being correct.

Displaying such scores could create false precision.

The product should prefer explainable evidence indicators over apparently precise but poorly calibrated confidence scores.

---

## Decision 5 — Start without RAG

### Decision

The first version will analyse a deliberately small dataset without implementing a Retrieval-Augmented Generation architecture.

### Why

The initial goal is to test the product hypothesis:

> Can AI generate useful, evidence-backed product insights from qualitative feedback?

Adding embeddings, vector databases and retrieval infrastructure before establishing this would increase complexity without necessarily increasing product value.

The MVP will establish a baseline first.

RAG will be considered when:

- datasets become too large for reliable direct analysis
- relevant evidence becomes difficult to retrieve
- context-window limitations become important
- evaluation demonstrates that retrieval would improve output quality

### Principle

Use additional AI architecture to solve demonstrated problems, not simply because the technology is available.

---

## Decision 6 — Use synthetic data initially

### Decision

The public demonstration will use synthetic customer feedback.

### Why

Real customer feedback may contain:

- names
- contact information
- commercially sensitive information
- confidential product information
- personal data

Using synthetic data allows the AI workflow to be demonstrated publicly without exposing real customers or former employers.

The synthetic dataset should still contain realistic patterns, contradictions, edge cases and irrelevant feedback so that the AI analysis can be meaningfully evaluated.

---

## Decision 7 — Structured output over unrestricted prose

### Decision

Where possible, the model should return findings using a defined structure rather than an unrestricted narrative response.

A finding might contain:

- theme
- pain point
- evidence IDs
- evidence strength
- problem statement
- potential opportunity

### Why

Structured output makes it easier to:

- validate model responses
- display findings consistently
- compare different runs
- evaluate output quality
- detect missing information
- integrate AI output into an application

---

## Decision 8 — Evaluate output rather than relying on demos

### Decision

The project will include an evaluation process for AI-generated findings.

The initial evaluation dimensions will be:

### Faithfulness

Is the finding actually supported by the referenced evidence?

### Coverage

Did the system identify the important patterns present in the dataset?

### Hallucination

Did the model introduce claims that are not supported by the source feedback?

### Usefulness

Would the output help a product professional understand or investigate the customer problem?

### Why

Generative AI can produce impressive individual examples while performing inconsistently across repeated tasks.

A successful demonstration is therefore not sufficient evidence of a reliable AI product.

---

## Decision 9 — Maintain human review

### Decision

Generated findings will be presented for review rather than automatically accepted.

The current review prototype allows users to:

- accept, edit or reject a finding
- inspect the cited source evidence
- record a review note
- export the reviewed result

The interface also warns when a cited feedback ID is missing from the supplied dataset. Relevance and faithfulness still require human assessment.

### Why

Human review provides both a product safeguard and a potential source of evaluation data.

Patterns in accepted, edited and rejected findings could eventually help measure the usefulness of the system.

---

## Decision 10 — Treat prompts as product components

### Decision

Prompts used by the application will be treated as versioned product components rather than hidden implementation details.

Changes to important prompts should be documented and tested.

### Why

Prompt changes can materially alter:

- output quality
- hallucination rates
- tone
- structure
- evidence selection
- consistency

Prompt changes should therefore be evaluated in much the same way as other changes to product behaviour.

---

## Decision 11 — Improve theme separation before adding retrieval architecture

### Evidence

The first controlled benchmark held the 40-record dataset, `gemini-3.5-flash` model and prompt version `v1` constant across three runs.

The benchmark measured:

- 100% citation validity
- 95.5% mean evidence precision
- 88.5% mean reference evidence coverage
- 66.7% mean theme coverage

All three runs identified the two dominant themes but missed the smaller payment communication and audit-history theme. Relevant records were generally retrieved but were grouped into a broader payment-status theme.

### Decision

Theme separation remains a valid improvement target, but it will not be optimised in isolation against the known 40-record dataset. The current prompt and benchmark are preserved as the baseline while broader failure modes are evaluated first.

RAG, embeddings and vector storage remain deferred.

### Why

The measured limitation is theme separation rather than missing source retrieval. Adding retrieval architecture would increase complexity without addressing the failure observed in the benchmark.

Optimising directly against the known missed theme also creates a risk of overfitting the prompt to one synthetic dataset. A broader red-team baseline provides a better basis for judging whether a prompt change genuinely improves the product or merely improves one benchmark score.

---

## Decision 12 — Red-team before targeted optimisation

### Evidence

A broader review of the current product found failure modes not adequately covered by the first benchmark, including:

- prompt injection embedded in feedback content;
- duplicate or blank IDs breaking evidence traceability;
- stale findings remaining visible after the source dataset changes;
- duplicated feedback creating false evidence volume;
- evidence-strength labels overstating narrow evidence;
- unsupported statistics or causal claims inside otherwise valid findings;
- neutral evidence being treated as contradiction;
- low-frequency/high-severity signals being hidden by recurring-theme logic;
- related customer problems being over-merged;
- one underlying problem being over-fragmented after attempts to improve separation.

### Decision

Version `v0.5` will create a compact adversarial evaluation suite of roughly 15 cases and run the current behaviour before fixes are introduced.

The first scoring approach will remain deliberately lightweight and human-readable: coverage, groundedness, evidence integrity, qualification, behavioural integrity, Pass/Partial/Fail and failure severity.

Targeted changes—including prompt `v2`—move to `v0.6`. The same suite will then be rerun in `v0.7` to check improvement and regression.

### Why

The project is intended to demonstrate product judgement, not eval-platform engineering. A small set of well-designed failure cases is more useful at this stage than a large automated test framework.

Recording baseline failures before fixing them prevents retrospective test design and creates a clearer before/after product story.

---

## Decision 13 — SQL is supporting analysis, not a separate project

### Decision

Do not create a standalone SQL portfolio exercise for this project.

If the red-team and regression work generates enough structured run data to justify it, SQLite and SQL may be introduced to analyse test results across versions, models, failure categories and severity.

### Why

SQL adds value when it answers a real product question. Using it to analyse accumulated eval runs demonstrates practical data fluency without creating a disconnected technical exercise.

---

# Current Architecture Principle

The initial architecture should be the simplest architecture capable of testing the product hypothesis.

The expected progression is:

**Structured feedback**

↓

**LLM analysis**

↓

**Structured findings**

↓

**Evidence validation**

↓

**Human review**

More sophisticated techniques such as embeddings, semantic search and RAG should be introduced only when evaluation demonstrates that they solve a meaningful limitation.

---

# Open Questions

The project will explore several questions during development:

- How much customer feedback can be analysed reliably in a single context?
- How should evidence strength be calculated?
- How should contradictory customer feedback be represented?
- Can the model reliably distinguish evidence from inference?
- How frequently does the model cite irrelevant evidence?
- Does providing evidence requirements reduce hallucination?
- How should human corrections be captured?
- At what dataset size does retrieval become valuable?
- How should different model or prompt versions be compared?
- What level of AI transparency is genuinely useful to a Product Manager?
- How should low-frequency but high-severity evidence be surfaced without misrepresenting it as a recurring theme?
- How should the product defend against instructions embedded in untrusted feedback?
- How should duplicate and stale evidence states be detected and prevented?

These questions will be revisited as the prototype develops.

---

# Decision Log

| Decision | Current Position | Status |
|---|---|---|
| Role of AI | Assist, not decide | Accepted |
| Evidence traceability | Required | Accepted |
| Human review | Required | Implemented in v0.2 |
| Model confidence scores | Avoid | Accepted |
| Synthetic data | Use for public prototype | Implemented |
| Structured outputs | Preferred | Implemented |
| RAG | Not justified by the v0.4 benchmark | Deferred until a retrieval limitation is measured |
| Embeddings | Not justified by the v0.4 benchmark | Deferred until a retrieval limitation is measured |
| Evaluation framework | Human reference, transparent scorer and repeated runs | First controlled three-run benchmark completed in v0.4 |
| Red-team evaluation | Establish adversarial baseline before fixes | Current v0.5 milestone |
| Prompt iteration | Treat v2 as one targeted intervention after red-team baseline | Planned for v0.6 |
| Regression evaluation | Rerun the same adversarial suite after changes | Planned for v0.7 |
| SQL | Use only if structured eval data makes it useful | Deferred / supporting analysis only |

This document will evolve as the product is tested and new evidence becomes available.
