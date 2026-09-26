import copy
from datetime import datetime, timezone


ANALYSIS_STATE_KEYS = (
    "analysis",
    "analysis_original",
    "analysis_raw_output",
    "analysis_metadata",
)
REVIEW_KEY_PREFIXES = ("review:", "interpretation-", "decision-", "note-")


def clear_review_state(state):
    """Remove reviewer inputs belonging to an earlier analysis run."""
    for key in list(state.keys()):
        if str(key).startswith(REVIEW_KEY_PREFIXES):
            state.pop(key, None)


def clear_analysis_state(state, clear_failure=True):
    """Invalidate analysis and review state without changing dataset identity."""
    for key in ANALYSIS_STATE_KEYS:
        state.pop(key, None)
    clear_review_state(state)
    if clear_failure:
        state.pop("last_analysis_failure", None)


def bind_dataset(state, dataset_sha256, dataset_source):
    """Bind the active session to a dataset and clear stale state on change.

    Returns True when an existing dataset was replaced by a different dataset.
    """
    previous = state.get("active_dataset_sha256")
    changed = previous is not None and previous != dataset_sha256
    if changed:
        clear_analysis_state(state)

    state["active_dataset_sha256"] = dataset_sha256
    state["active_dataset_source"] = dataset_source
    return changed


def analysis_matches_dataset(metadata, dataset_sha256):
    """Return True only when analysis provenance matches the active dataset."""
    return bool(metadata) and metadata.get("dataset_sha256") == dataset_sha256


def build_review_export(
    metadata,
    original_analysis,
    raw_model_output,
    reviewed_themes,
    exported_at=None,
):
    """Build a provenance-preserving review export."""
    timestamp = exported_at or datetime.now(timezone.utc).isoformat()
    return {
        "export_version": "2.0",
        "provenance": {**copy.deepcopy(metadata), "exported_at": timestamp},
        "original_model_output": {
            "parsed": copy.deepcopy(original_analysis),
            "raw_text": raw_model_output,
        },
        "reviewed_analysis": {"themes": copy.deepcopy(reviewed_themes)},
    }
