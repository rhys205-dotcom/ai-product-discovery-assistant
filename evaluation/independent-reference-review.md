# Independent reference review

## Purpose

This is a blind review of the 40-record synthetic feedback dataset used in the first benchmark.

The aim is to challenge the existing human reference rather than ask another reviewer to reproduce it. The reviewer should not see `reference-analysis.json`, `golden-analysis.md` or the stored benchmark findings before completing this exercise.

## Reviewer instructions

Please review [`../data/sample-feedback.csv`](../data/sample-feedback.csv) using your normal qualitative-analysis approach.

Do **not** use the existing Discovery Assistant, the existing human reference or the benchmark results while doing the first-pass analysis.

Please identify:

1. The recurring customer problems you think are materially distinct.
2. The feedback IDs that support each problem.
3. Any feedback that qualifies, contradicts or limits each problem.
4. Any comments you regard as isolated requests or noise rather than recurring problems.
5. Where two apparent themes are better treated as one problem, a subtheme or an overlapping problem.
6. Any important signal that is not recurring but that you would still investigate.
7. The product or discovery question you would investigate next for each material problem.

There is no target number of themes.

## Response template

### Reviewer context

- Role / background:
- Approximate time spent:
- Analysis method used:

### Finding 1

- Problem / theme:
- Supporting feedback IDs:
- Qualifying / contradictory IDs:
- Why this is materially distinct:
- Next investigation question:

### Finding 2

- Problem / theme:
- Supporting feedback IDs:
- Qualifying / contradictory IDs:
- Why this is materially distinct:
- Next investigation question:

_Add more findings only where useful._

### Isolated or low-confidence signals

- Feedback IDs and why they should not be treated as recurring themes:

### Overall structure

- Which findings overlap?
- Would any be better represented as a subtheme rather than a top-level theme?
- Did any distinction materially change what you would investigate or decide next?

## Comparison after the blind review

Only after the reviewer has completed the section above should the project owner compare it with the existing reference.

Record the comparison without changing the existing reference in place:

- Areas of agreement:
- Areas of disagreement:
- Existing reference themes the reviewer did not independently identify:
- Reviewer findings absent from the existing reference:
- Theme boundaries that appear too broad or too narrow:
- Whether the communication / audit-history distinction changes the next product investigation:
- Decision: retain reference v1.0 / create a revised reference version / keep both as alternative plausible analyses.

## Interpretation rule

Agreement from one additional practitioner would increase confidence in a theme boundary; disagreement would not automatically make either analysis wrong. The purpose is to test whether the distinctions are useful and defensible, not to manufacture a single objective ground truth.
