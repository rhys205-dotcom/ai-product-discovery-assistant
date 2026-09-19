import csv
import io
import json

import streamlit as st

from src.analyse_feedback import analyse_feedback, load_feedback


st.set_page_config(page_title="AI Product Discovery Assistant", page_icon="🔎", layout="wide")

st.title("AI Product Discovery Assistant")
st.caption("Evidence-linked customer feedback analysis with human review")


def parse_upload(uploaded_file):
    """Read and validate an uploaded feedback CSV."""
    text = uploaded_file.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    required = {"feedback_id", "source", "persona", "feedback"}
    missing = required.difference(rows[0].keys() if rows else set())
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if not rows:
        raise ValueError("The uploaded CSV contains no feedback records.")
    return rows


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
            st.warning(f"{evidence_id} was cited but is not present in the uploaded dataset.")


with st.sidebar:
    st.header("Feedback data")
    uploaded = st.file_uploader("Upload a CSV", type="csv")
    st.caption("Required columns: feedback_id, source, persona, feedback")

try:
    feedback = parse_upload(uploaded) if uploaded else load_feedback()
except (UnicodeDecodeError, ValueError) as error:
    st.error(str(error))
    st.stop()

feedback_by_id = {item["feedback_id"]: item for item in feedback}
st.info(f"Ready to analyse {len(feedback)} feedback records.")

if st.button("Analyse feedback", type="primary"):
    try:
        with st.spinner("Identifying evidence-linked themes…"):
            st.session_state.analysis = analyse_feedback(feedback)
    except Exception as error:
        st.error(f"The analysis could not be completed: {error}")

analysis = st.session_state.get("analysis")
if analysis:
    themes = analysis.get("themes", [])
    if not themes:
        st.warning("The model returned no themes for review.")

    st.header("Review findings")
    st.caption("AI findings are proposals. Inspect the evidence before accepting them.")
    review_export = []

    for index, theme in enumerate(themes):
        title = theme.get("theme") or f"Finding {index + 1}"
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
                key=f"interpretation-{index}",
            )
            st.markdown(f"**Potential opportunity:** {theme.get('potential_opportunity', 'Not stated')}")

            contradictions = theme.get("contradictory_evidence", [])
            if contradictions:
                st.markdown("**Contradictory evidence:** " + ", ".join(contradictions))

            decision = st.radio(
                "Human review decision",
                ["Needs review", "Accept", "Edit and accept", "Reject"],
                horizontal=True,
                key=f"decision-{index}",
            )
            note = st.text_input("Review note", key=f"note-{index}")
            review_export.append(
                {
                    **theme,
                    "interpretation": interpretation,
                    "human_review": {"decision": decision, "note": note},
                }
            )

    st.download_button(
        "Download reviewed findings",
        data=json.dumps({"themes": review_export}, indent=2),
        file_name="reviewed-discovery-findings.json",
        mime="application/json",
    )
