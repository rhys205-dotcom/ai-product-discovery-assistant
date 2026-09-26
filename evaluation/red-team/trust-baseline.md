# Deterministic trust baseline

This note records the known evidence-integrity failures **before** repairing them, so the project keeps a clear before/after trail rather than designing the failures away retrospectively.

Baseline repository state: `8b79640848fcfbf4adcbbfae555649dfb903935c` (`main`, 26 September 2026).

## E14 — duplicate and blank feedback IDs

**Baseline outcome: FAIL — High severity**

At the baseline commit, `app.py::parse_upload()` checked that required columns existed and that at least one row was present, but did not reject blank or duplicate `feedback_id` values.

The application then created its evidence lookup with:

```python
feedback_by_id = {item["feedback_id"]: item for item in feedback}
```

A duplicate ID therefore overwrote an earlier record in the lookup. A finding could appear to cite a valid ID while displaying a different record from the one intended.

**Repair condition:** uploaded and built-in datasets must have non-blank, unique IDs before analysis begins.

## E15 — stale dataset, analysis and review state

**Baseline outcome: FAIL — High severity**

At the baseline commit, model output was stored as `st.session_state.analysis`, but no dataset identity was stored with it. Changing the uploaded dataset did not invalidate that analysis.

Evidence was resolved against the **currently loaded** dataset, so if Dataset A and Dataset B reused an ID, a finding produced from A could display B's feedback text without triggering the missing-ID warning.

Reviewer widget keys were positional (`interpretation-0`, `decision-0`, `note-0`), so review choices could also carry into replacement findings at the same position.

**Repair condition:** dataset identity, analysis run and reviewer state must be bound together; changing dataset or generating a new analysis must invalidate stale findings and review state.

## Structured-response and failure-state gap

**Baseline outcome: FAIL — High severity**

`analyse_feedback()` rejected invalid JSON and required only that `themes` be a list. An object such as `{"themes":[{}]}` passed validation and could be rendered as an apparently valid finding with fallback labels.

A failed analysis call displayed an error but did not first invalidate a previous successful `st.session_state.analysis`, creating another route for stale output to remain visible.

**Repair condition:** validate the required finding structure and clear stale analysis before each new attempt; failed calls and invalid responses must be explicit outcomes rather than leaving previous output in place.

## Export provenance gap

**Baseline outcome: PARTIAL/FAIL — Medium severity**

The review export replaced the original interpretation with the edited version and exported only a `themes` array. It did not preserve the original model result separately or include dataset/run provenance.

**Repair condition:** export the original analysis separately from reviewed output and include dataset identity, run identity, model/configuration metadata and timestamps.

## Why these fixes come before the full behavioural suite

These failures do not depend on subtle model judgement. They directly undermine the product promise that a reviewer can trace a finding back to the evidence that produced it. They are therefore recorded here and repaired before spending more model calls on the wider behavioural baseline.
