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
| RAG | Not required for MVP | Deferred pending evidence |
| Embeddings | Not required for MVP | Deferred pending evidence |
| Evaluation framework | Human reference and transparent scorer | Baseline implemented; controlled runs pending |

This document will evolve as the product is tested and new evidence becomes available.
