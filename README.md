# AI Product Discovery Assistant

An experimental AI-powered product discovery tool that turns unstructured customer feedback into evidence-backed themes, problems, opportunities and product recommendations.

## Why this project exists

Product teams often have large volumes of qualitative feedback from customer interviews, support tickets, surveys and research sessions.

The challenge is not collecting feedback. It is turning that feedback into useful product insight without losing the evidence behind it.

This project explores how generative AI can support product discovery by helping teams:

- identify recurring customer themes
- surface customer pain points
- group similar feedback
- generate problem statements
- suggest product opportunities
- produce draft user stories and acceptance criteria
- retain traceability back to the original customer evidence

The goal is to support product judgement, not replace it.

## The problem

Traditional analysis of qualitative customer feedback can be:

- time-consuming
- inconsistent
- difficult to scale
- vulnerable to confirmation bias
- hard to trace back to original evidence

Large Language Models can help accelerate this work, but they introduce their own risks including hallucination, over-generalisation and loss of context.

This project explores how those risks can be reduced through evidence-backed outputs and human review.

## MVP

The first version will allow a user to provide a collection of customer feedback and receive:

1. Key themes
2. Customer pain points
3. Supporting evidence
4. Suggested problem statements
5. Potential product opportunities
6. Draft user stories
7. Confidence or evidence indicators

The system should clearly distinguish between:

- what customers actually said
- what the AI inferred
- what the AI recommends

## Example workflow

Customer feedback

↓

AI analysis

↓

Themes and pain points

↓

Evidence from original feedback

↓

Product opportunities

↓

Human review and prioritisation

## Responsible AI principles

This project is being designed around several principles:

### Evidence before conclusions

Important findings should be traceable back to the original customer feedback.

### Human-in-the-loop

AI recommendations should support product decision-making rather than make decisions autonomously.

### Transparency

The application should clearly separate source evidence from AI-generated interpretation.

### Privacy

The demonstration version will use synthetic customer data rather than real customer information.

### Evaluation

AI-generated insights should be assessed for usefulness, accuracy and faithfulness to the source material.

## How success could be measured

Possible product metrics include:

- percentage of generated themes supported by source evidence
- number of unsupported or hallucinated claims
- agreement between AI-generated themes and human analysis
- time saved during qualitative research analysis
- usefulness rating from product users
- percentage of AI recommendations accepted or edited by users

## Planned development

### Phase 1 — Product definition
Define the problem, users, MVP and success measures.

### Phase 2 — Basic AI analysis
Analyse synthetic customer feedback and generate structured themes and pain points.

### Phase 3 — Evidence and traceability
Link generated insights back to the source feedback.

### Phase 4 — Product recommendations
Generate problem statements, opportunities and draft user stories.

### Phase 5 — Evaluation
Create a lightweight evaluation framework to measure output quality and hallucination risk.

### Phase 6 — User experience
Build a simple interface for uploading feedback and reviewing the analysis.

## Technology

The exact technical architecture will evolve as the project develops.

Likely components include:

- Python
- Large Language Model API
- structured prompting
- embeddings and semantic search
- retrieval-augmented generation (RAG)
- lightweight web interface
- automated evaluation

## Project status

🚧 Early development

The current focus is defining the product problem, MVP and responsible AI approach before expanding the technical implementation.

## About this project

This is a personal learning project exploring the practical use of generative AI in product management, business analysis and customer discovery.

The aim is not simply to demonstrate an AI API integration, but to explore how AI-enabled products can be designed, evaluated and governed responsibly.
