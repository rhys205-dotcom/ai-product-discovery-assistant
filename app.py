import copy
import csv
import io
import json
import uuid
from datetime import datetime, timezone

import streamlit as st

from src.analyse_feedback import (
    analyse_feedback_with_metadata,
    dataset_fingerprint,
    load_feedback,
    validate_feedback_records,
)


st.set_page_config(page_title="AI Product Discovery Assistant", page_icon="🔎", layout="wide")

st.title("AI Product Discovery Assistant")
st.caption("Evidence-linked customer feedback analysis with human review")


ANALYSIS_STATE_KEYS = (
    "analysis",
    "analysis_original",
    "analysis_raw_output",
    "analysis_metadata",
)


def clear_review_widget_state():
    """Remove reviewer inputs from an earlier analysis run."""
    for key in list(st.session_state.keys()):
        key_text = str(key)
        if key_text.startswith("review:") or key_text.startswith(
            ("interpretation-", "decision-", "note-")
        ):
            del st.session_state[key]


def clear_analysis_state(clear_failure=True):
    """Invalidate analysis and review state without changing the active dataset."""
    for key in ANALYSIS_STATE_KEYS:
        st.session_state.pop(key, None)
    clear_review_widget_state()
    if clear_failure:
        st.session_state.pop("last_analysis_failure", None)


def parse_upload(uploaded_file):
    """Read, validate and normalise an uploaded feedback CSV."""
    text = uploaded_file.getvalue().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    required = {"feedback_id", "source", "persona", "feedback"}
    fieldnames = set(reader.fieldnames or [])
    missing = required.difference(fieldnames)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    return validate_feedback_records(list(reader))


def show_evidence(evidence_ids, feedback_by_id):
    """Render the source feedback cited by a finding."""
    for evidence_id in evidence_ids:
        item = feedback_by_id.get(evidence_id)
        if item:
            st.markdown(
                f"**{evidence_id} · {item['source']} · {item['persona']}**  \n"
                f"> {item['feedback']}"
            )
        else:
            st.warning(f"{evidence_id} was cited but is not present in the active dataset.")


with st.sidebar:
    st.header("Feedback data")
    uploaded = st.file_uploader("Upload a CSV", type="csv")
    st.caption("Required columns: feedback_id, source, persona, feedback")

try:
    if uploaded:
        feedback = parse_upload(uploaded)
        dataset_source = uploaded.name
    else:
        feedback = load_feedback()
        dataset_source = "data/sample-feedback.csv"
except (UnicodeDecodeError, ValueError) as error:
    st.error(str(error))
    st.stop()

dataset_sha256 = dataset_fingerprint(feedback)
previous_dataset_sha256 = st.session_state.get("active_dataset_sha256")
if previous_dataset_sha256 is None:
    st.session_state.active_dataset_sha256 = dataset_sha256
    st.session_state.active_dataset_source = dataset_source
elif previous_dataset_sha256 != dataset_sha256:
    clear_analysis_state()
    st.session_state.active_dataset_sha256 = dataset_sha256
    st.session_state.active_dataset_source = dataset_source

feedback_by_id = {item["feedback_id"]: item for item in feedback}
st.info(f"Ready to analyse {len(feedback)} feedback records.")
st.caption(f"Dataset identity: {dataset_sha256[:12]}…")

if st.button("Analyse feedback", type="primary"):
    # A new attempt invalidates previous findings and reviewer state even if the call fails.
    clear_analysis_state()
    run_id = uuid.uuid4().hex
    attempted_at = datetime.now(timezone.utc).isoformat()

    try:
        with st.spinner("Identifying evidence-linked themes…"):
            result = analyse_feedback_with_metadata(feedback)
    except Exception as error:
        st.session_state.last_analysis_failure = {
            "run_id": run_id,
            "dataset_sha256": dataset_sha256,
            "dataset_source": dataset_source,
            "record_count": len(feedback),
            "attempted_at": attempted_at,
            "error_type": type(error).__name__,
            "error": str(error),
        }
        st.error(f"The analysis could not be completed: {error}")
    else:
        metadata = {
            "run_id": run_id,
            "dataset_sha256": dataset_sha256,
            "dataset_source": dataset_source,
            "record_count": result["record_count"],
            "model": result["model"],
            "prompt_sha256": result["prompt_sha256"],
            "attempted_at": attempted_at,
            "generated_at": result["generated_at"],
        }
        st.session_state.analysis = copy.deepcopy(result["analysis"])
        st.session_state.analysis_original = copy.deepcopy(result["analysis"])
        st.session_state.analysis_raw_output = result["raw_output"]
        st.session_state.analysis_metadata = metadata

analysis = st.session_state.get("analysis")
metadata = st.session_state.get("analysis_metadata")

# Defence in depth: never render analysis against a different active dataset.
if analysis and (
    not metadata or metadata.get("dataset_sha256") != dataset_sha256
):
    clear_analysis_state(clear_failure=False)
    analysis = None
    metadata = None
    st.warning("Previous findings were cleared because they did not belong to the active dataset.")

failure = st.session_state.get("last_analysis_failure")
if not analysis and failure and failure.get("dataset_sha256") == dataset_sha256:
    st.warning(
        "Last analysis attempt failed and no earlier findings were retained. "
        f"Run {failure['run_id'][:8]} · {failure['error_type']}: {failure['error']}"
    )

if analysis:
    themes = analysis.get("themes", [])
    if not themes:
        st.warning("The model returned no themes for review.")

    st.header("Review findings")
    st.caption(
        "AI findings are proposals. Inspect the evidence before accepting them. "
        f"Run {metadata['run_id'][:8]} · dataset {metadata['dataset_sha256'][:12]}…"
    )
    review_export = []

    for index, theme in enumerate(themes):
        title = theme.get("theme") or f"Finding {index + 1}"
        widget_prefix = f"review:{metadata['run_id']}:{index}"

        with st.expander(title, expanded=index == 0):
            strength = theme.get("evidence_strength", "Not stated")
            st.markdown(f"**Evidence strength:** {strength}")
            st.markdown(f"**Pain point:** {theme.get('pain_point', 'Not stated')}")

            st.subheader("Customer evidence")
            show_evidence(theme.get("evidence_ids", []), feedback_by_id)

            st.subheader("AI interpretation")
            interpretation = st.text_area(
                "Edit the interpretation if needed",
                value=theme.get("interpretation", ""),
                key=f"{widget_prefix}:interpretation",
            )
            st.markdown(f"**Potential opportunity:** {theme.get('potential_opportunity', 'Not stated')}")

            contradictions = theme.get("contradictory_evidence", [])
            if contradictions:
                st.markdown("**Contradictory evidence:** " + ", ".join(contradictions))

            decision = st.radio(
                "Human review decision",
                ["Needs review", "Accept", "Edit and accept", "Reject"],
                horizontal=True,
                key=f"{widget_prefix}:decision",
            )
            note = st.text_input("Review note", key=f"{widget_prefix}:note")
            review_export.append(
                {
                    **theme,
                    "interpretation": interpretation,
                    "human_review": {"decision": decision, "note": note},
                }
            )

    export_payload = {
        "export_version": "2.0",
        "provenance": {
            **metadata,
            "exported_at": datetime.now(timezone.utc).isoformat(),
        },
        "original_model_output": {
            "parsed": st.session_state.get("analysis_original", {}),
            "raw_text": st.session_state.get("analysis_raw_output", ""),
        },
        "reviewed_analysis": {"themes": review_export},
    }

    st.download_button(
        "Download reviewed findings",
        data=json.dumps(export_payload, indent=2, ensure_ascii=False),
        file_name=f"reviewed-discovery-findings-{metadata['run_id'][:8]}.json",
        mime="application/json",
    )
