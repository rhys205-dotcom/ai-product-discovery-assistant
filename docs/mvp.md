# Minimum Viable Product

## MVP Goal

Build a simple working application that demonstrates how generative AI can help a product professional analyse qualitative customer feedback while maintaining traceability to the original evidence.

The MVP should prove one core idea:

> AI can accelerate customer-feedback analysis without hiding the evidence or replacing human judgement.

## Primary User

The initial user is a Product Manager, Product Owner or Business Analyst who has a collection of qualitative customer feedback and wants to identify meaningful patterns and potential product opportunities.

## Core User Journey

1. The user provides a dataset containing customer feedback.
2. The system analyses the feedback using a Large Language Model.
3. The system identifies recurring themes and customer pain points.
4. Each finding is linked to supporting evidence from the original feedback.
5. The system suggests potential problem statements and product opportunities.
6. The user reviews the findings and decides which insights are useful.

The application should make a clear distinction between:

**Customer evidence → AI interpretation → AI recommendation**

## MVP Inputs

The first version will use a simple structured dataset.

Each feedback item will contain:

- unique feedback ID
- feedback text
- source
- optional customer or persona type

Example:

| ID | Source | Persona | Feedback |
|---|---|---|---|
| F001 | Support | Admin | I have to export the report every Friday and manually fix the totals in Excel. |
| F002 | Interview | Finance | It takes me nearly an hour to reconcile payments at the end of the month. |
| F003 | Survey | Admin | I wish the system told me when a payment had failed instead of finding out later. |

The demonstration dataset will contain synthetic rather than real customer information.

## MVP Outputs

The system should generate structured findings containing:

### Theme

A short description of a recurring pattern in the feedback.

### Pain Point

The underlying customer problem associated with the theme.

### Supporting Evidence

The IDs of the feedback records that support the finding.

Where useful, the application may display short excerpts from those records.

### Evidence Strength

A simple indication of how much evidence supports the finding.

For example:

- Strong
- Moderate
- Limited

This should be based on defined criteria rather than simply asking the model how confident it feels.

### Problem Statement

A draft problem statement based on the evidence.

### Product Opportunity

A possible opportunity for addressing the customer problem.

This is explicitly an AI-generated suggestion rather than a customer requirement.

## Example Output

### Theme: Payment reconciliation is too manual

**Pain point**

Finance users spend significant time reconciling payment information across systems.

**Supporting evidence**

F002, F007, F014, F021

**Evidence strength**

Strong

**Problem statement**

Finance users need a faster way to reconcile payment activity because the existing manual process consumes significant time and increases the opportunity for error.

**Potential opportunity**

Explore automated reconciliation and exception reporting.

The opportunity is a recommendation generated from the evidence. It should not be presented as something customers explicitly requested.

## Human Review

The MVP should allow the user to review the generated findings.

The user should remain responsible for deciding:

- whether a theme is meaningful
- whether the evidence supports the conclusion
- whether the problem is worth solving
- whether a suggested opportunity should be explored
- how any opportunity should be prioritised

AI output should be treated as a starting point for product judgement rather than a final decision.

## Hallucination and Traceability

A central requirement of the MVP is that generated findings must reference identifiable feedback records.

The system should avoid presenting unsupported claims as customer evidence.

Where there is insufficient evidence to support a conclusion, the system should either:

- label the finding as weak or uncertain, or
- avoid generating the finding

This behaviour will form part of the project's evaluation.

## MVP Evaluation

The first evaluation will focus on four questions:

### 1. Faithfulness

Are the generated findings supported by the referenced customer feedback?

### 2. Coverage

Does the system identify the important themes present in the dataset?

### 3. Hallucination

Does the system introduce claims that cannot be supported by the source data?

### 4. Usefulness

Would the generated analysis help a product professional investigate the customer problem?

## Out of Scope

The first version will not include:

- autonomous roadmap creation
- automatic product prioritisation
- production customer data
- integrations with support or CRM platforms
- automated decision-making
- complex user management
- enterprise security features
- model fine-tuning

These capabilities may be explored later but are not required to test the core hypothesis.

## Initial Technical Approach

The MVP is expected to use:

- Python for application logic
- a Large Language Model for analysis
- structured prompts and structured outputs
- synthetic customer feedback stored in CSV format
- a lightweight web interface
- explicit references between generated findings and source feedback

Retrieval-augmented generation (RAG), embeddings and semantic search will be considered as the dataset and use cases become more complex.

They will not be added simply for technical complexity.

## Definition of Done

The MVP will be considered complete when a user can:

1. provide a sample feedback dataset
2. run an AI analysis
3. view recurring themes and pain points
4. see which feedback records support each finding
5. distinguish customer evidence from AI interpretation and recommendation
6. review the generated product opportunities
7. understand the limitations of the analysis

## Next Iteration

Once the basic workflow works reliably, the next iteration will explore:

- improved evidence retrieval
- evaluation against a human-created reference analysis
- user feedback on AI findings
- semantic search
- RAG for larger datasets
- comparison of prompts or models
- richer visualisation of themes and evidence
