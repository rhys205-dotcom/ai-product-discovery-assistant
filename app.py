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
    find_exact_duplicate_groups,
    load_feedback,
    validate_feedback_records,
)
from src.review_integrity import (
    analysis_matches_dataset,
    bind_dataset,
    build_review_export,
    clear_analysis_state,
)


st.set_page_config(page_title="AI Product Discovery Assistant", page_icon="🔎", layout="wide")

st.title("AI Product Discovery Assistant")
st.caption("Evidence-linked customer feedback analysis with human review")


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


def evidence_basis(evidence_ids, feedback_by_id, duplicate_groups):
    """Summarise observable support without turning it into model confidence."""
    cited = [feedback_by_id[eid] for eid in evidence_ids if eid in feedback_by_id]
    sources = sorted({item["source"] for item in cited})
    personas = sorted({item["persona"] for item in cited})
    cited_set = set(evidence_ids)
    repeated = [
        group
        for group in duplicate_groups
        if len(cited_set.intersection(group["feedback_ids"])) > 1
    ]
    return {
        "records": len(cited),
        "sources": sources,
        "personas": personas,
        "duplicate_groups": repeated,
    }


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
duplicate_groups = find_exact_duplicate_groups(feedback)
bind_dataset(st.session_state, dataset_sha256, dataset_source)

feedback_by_id = {item["feedback_id"]: item for item in feedback}
st.info(f"Ready to analyse {len(feedback)} feedback records.")
st.caption(f"Dataset identity: {dataset_sha256[:12]}…")

if duplicate_groups:
    ids = [" / ".join(group["feedback_ids"]) for group in duplicate_groups]
    st.warning(
        "Possible repeated evidence detected: "
        + "; ".join(ids)
        + ". Exact repetition does not prove a shared respondent, but these records "
        "should not be treated as independent support."
    )

if st.button("Analyse feedback", type="primary"):
    clear_analysis_state(st.session_state)
    run_id = uuid.uuid4().hex
    attempted_at = datetime.now(timezone.utc).isoformat()

    try:
        with st.spinner("Identifying evidence-linked themes and isolated signals…"):
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
            "provider": result["provider"],
            "model": result["model"],
            "prompt_version": result["prompt_version"],
            "prompt_sha256": result["prompt_sha256"],
            "duplicate_evidence_groups": result["duplicate_evidence_groups"],
            "attempted_at": attempted_at,
            "generated_at": result["generated_at"],
        }
        st.session_state.analysis = copy.deepcopy(result["analysis"])
        st.session_state.analysis_original = copy.deepcopy(result["analysis"])
        st.session_state.analysis_raw_output = result["raw_output"]
        st.session_state.analysis_metadata = metadata

analysis = st.session_state.get("analysis")
metadata = st.session_state.get("analysis_metadata")

if analysis and not analysis_matches_dataset(metadata, dataset_sha256):
    clear_analysis_state(st.session_state, clear_failure=False)
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
    isolated_signals = analysis.get("isolated_signals", [])

    if not themes:
        st.info("The model found no recurring themes that met the current contract.")

    st.header("Review recurring findings")
    st.caption(
        "AI findings are proposals. Inspect the evidence before accepting them. "
        f"Run {metadata['run_id'][:8]} · dataset {metadata['dataset_sha256'][:12]}… "
        f"· prompt {metadata.get('prompt_version', 'unknown')}"
    )
    review_export = []

    for index, theme in enumerate(themes):
        title = theme.get("theme") or f"Finding {index + 1}"
        widget_prefix = f"review:{metadata['run_id']}:theme:{index}"

        with st.expander(title, expanded=index == 0):
            strength = theme.get("evidence_strength", "Not stated")
            st.markdown(f"**Model evidence-strength label:** {strength}")
            st.markdown(f"**Pain point:** {theme.get('pain_point', 'Not stated')}")

            basis = evidence_basis(theme.get("evidence_ids", []), feedback_by_id, duplicate_groups)
            st.caption(
                f"Observable support: {basis['records']} cited records · "
                f"{len(basis['sources'])} source type(s) · "
                f"{len(basis['personas'])} persona(s)"
            )
            if basis["duplicate_groups"]:
                group_ids = [
                    ", ".join(group["feedback_ids"])
                    for group in basis["duplicate_groups"]
                ]
                st.warning(
                    "Cited evidence includes possible exact duplicates: "
                    + "; ".join(group_ids)
                )

            st.subheader("Customer evidence")
            show_evidence(theme.get("evidence_ids", []), feedback_by_id)

            st.subheader("AI interpretation")
            interpretation = st.text_area(
                "Edit the interpretation if needed",
                value=theme.get("interpretation", ""),
                key=f"{widget_prefix}:interpretation",
            )
            opportunity = st.text_area(
                "Edit the potential opportunity if needed",
                value=theme.get("potential_opportunity", ""),
                key=f"{widget_prefix}:opportunity",
            )

            contradictions = theme.get("contradictory_evidence", [])
            if contradictions:
                st.subheader("Contradictory / qualifying evidence")
                show_evidence(contradictions, feedback_by_id)

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
                    "potential_opportunity": opportunity,
                    "human_review": {"decision": decision, "note": note},
                }
            )

    reviewed_signals = []
    if isolated_signals:
        st.header("Isolated signals requiring investigation")
        st.caption(
            "These are not recurring themes. They are low-frequency observations "
            "the model judged potentially material enough to investigate separately."
        )

        for index, signal in enumerate(isolated_signals):
            title = signal.get("signal") or f"Signal {index + 1}"
            widget_prefix = f"review:{metadata['run_id']}:signal:{index}"

            with st.expander(title, expanded=True):
                st.markdown(
                    f"**Why it may matter:** {signal.get('why_it_matters', 'Not stated')}"
                )
                st.subheader("Customer evidence")
                show_evidence(signal.get("evidence_ids", []), feedback_by_id)

                uncertainty = st.text_area(
                    "Uncertainty / what is not established",
                    value=signal.get("uncertainty", ""),
                    key=f"{widget_prefix}:uncertainty",
                )
                next_step = st.text_area(
                    "Verification / investigation next step",
                    value=signal.get("recommended_next_step", ""),
                    key=f"{widget_prefix}:next-step",
                )
                decision = st.radio(
                    "Human review decision",
                    ["Needs review", "Accept", "Edit and accept", "Reject"],
                    horizontal=True,
                    key=f"{widget_prefix}:decision",
                )
                note = st.text_input("Review note", key=f"{widget_prefix}:note")
                reviewed_signals.append(
                    {
                        **signal,
                        "uncertainty": uncertainty,
                        "recommended_next_step": next_step,
                        "human_review": {"decision": decision, "note": note},
                    }
                )

    export_payload = build_review_export(
        metadata=metadata,
        original_analysis=st.session_state.get("analysis_original", {}),
        raw_model_output=st.session_state.get("analysis_raw_output", ""),
        reviewed_themes=review_export,
        reviewed_signals=reviewed_signals,
    )

    st.download_button(
        "Download reviewed findings",
        data=json.dumps(export_payload, indent=2, ensure_ascii=False),
        file_name=f"reviewed-discovery-findings-{metadata['run_id'][:8]}.json",
        mime="application/json",
    )
