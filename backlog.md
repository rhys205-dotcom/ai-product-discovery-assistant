# Product Backlog

This backlog captures the next experiments for the AI Product Discovery Assistant.

The aim is not to build features for their own sake. Each iteration should test whether AI can make qualitative product discovery faster while keeping the underlying customer evidence visible.

## Now — v0.2: Evidence-linked discovery

### Generate themes from customer feedback
Analyse a small set of qualitative feedback and identify recurring themes.

**Why:** Product teams can spend significant time manually grouping feedback.

**Success looks like:** Themes are useful enough to accelerate analysis without replacing human review.

### Link themes back to evidence
Every generated theme should reference the feedback that supports it.

**Why:** A plausible AI summary is not enough. Product decisions need traceability to customer evidence.

**Success looks like:** A product manager can quickly inspect why the assistant generated a theme.

### Show uncertainty
Include a simple confidence assessment and flag themes where the evidence is weak or ambiguous.

**Why:** AI output should help judgement rather than create false certainty.

---

## Next — v0.3: From themes to opportunities

### Generate problem statements
Turn validated themes into concise customer problem statements.

### Suggest opportunities
Generate possible product opportunities without automatically treating them as recommendations.

### Separate evidence from inference
Clearly distinguish:

- what customers actually said
- what the AI inferred
- what still requires product judgement

### Compare AI and human analysis
Run the same feedback through manual and AI-assisted analysis and document meaningful differences.

---

## Later

### Interactive feedback analysis
Allow a user to paste or upload qualitative feedback and receive structured discovery output.

### Theme consolidation
Identify themes that appear different but may describe the same underlying problem.

### Prioritisation support
Explore combining evidence strength, frequency, customer impact and strategic context.

AI should support prioritisation rather than make the final prioritisation decision.

### Larger datasets
Test whether the approach remains useful as the volume and diversity of feedback increases.

---

## Not building yet

- autonomous roadmap generation
- automatic feature prioritisation
- unsupervised product decisions
- complex integrations
- production-scale infrastructure

These would add complexity before the core assumption has been validated:

> **Can generative AI help a product manager turn messy qualitative feedback into useful, evidence-linked insight without losing human judgement?**

---

## Current status

**v0.1** — Product concept, AI decision principles and sample feedback dataset.

**v0.2** — In progress: evidence-linked discovery output and evaluation.
