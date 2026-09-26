import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI


DATA_FILE = Path(__file__).parent.parent / "data" / "sample-feedback.csv"
REQUIRED_FEEDBACK_FIELDS = ("feedback_id", "source", "persona", "feedback")
REQUIRED_THEME_FIELDS = (
    "theme",
    "pain_point",
    "evidence_ids",
    "evidence_strength",
    "interpretation",
    "potential_opportunity",
    "contradictory_evidence",
)
EVIDENCE_STRENGTHS = {"Strong", "Moderate", "Limited"}


def validate_feedback_records(feedback):
    """Validate and normalise feedback records used by the application."""
    if not feedback:
        raise ValueError("At least one feedback record is required.")

    normalised = []
    seen_ids = set()

    for index, item in enumerate(feedback, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Feedback record {index} is not a valid object.")

        missing = [field for field in REQUIRED_FEEDBACK_FIELDS if field not in item]
        if missing:
            raise ValueError(
                f"Feedback record {index} is missing required fields: "
                + ", ".join(missing)
            )

        row = dict(item)
        for field in REQUIRED_FEEDBACK_FIELDS:
            value = row.get(field)
            row[field] = "" if value is None else str(value).strip()

        feedback_id = row["feedback_id"]
        if not feedback_id:
            raise ValueError(f"Feedback record {index} has a blank feedback_id.")
        if feedback_id in seen_ids:
            raise ValueError(f"Duplicate feedback_id: {feedback_id}")
        if not row["feedback"]:
            raise ValueError(f"Feedback record {feedback_id} has blank feedback text.")

        seen_ids.add(feedback_id)
        normalised.append(row)

    return normalised


def dataset_fingerprint(feedback):
    """Return a stable SHA-256 fingerprint for the ordered feedback dataset."""
    normalised = validate_feedback_records(feedback)
    canonical = json.dumps(
        [
            {field: item[field] for field in REQUIRED_FEEDBACK_FIELDS}
            for item in normalised
        ],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_feedback(data_file=DATA_FILE):
    """Load and validate customer feedback from a CSV dataset."""
    with Path(data_file).open("r", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    return validate_feedback_records(rows)


def build_prompt(feedback):
    """Create the product-discovery analysis prompt."""
    feedback = validate_feedback_records(feedback)
    feedback_text = "\n".join(
        f"{item['feedback_id']} | {item['source']} | "
        f"{item['persona']} | {item['feedback']}"
        for item in feedback
    )

    return f"""
You are assisting a Product Manager analysing qualitative customer feedback.

Your job is to identify meaningful recurring customer problems while remaining
strictly faithful to the supplied evidence.

IMPORTANT RULES:

1. Do not treat isolated feature requests as major themes.
2. Do not invent customer needs or facts.
3. Distinguish customer evidence from your interpretation.
4. Every theme must reference the feedback IDs that support it.
5. Consider contradictory evidence.
6. Prefer underlying customer problems over requested solutions.
7. Do not make autonomous prioritisation decisions.

For each meaningful theme return:

- theme
- pain_point
- evidence_ids
- evidence_strength
- interpretation
- potential_opportunity
- contradictory_evidence

Evidence strength must be one of Strong, Moderate or Limited. Base it on the
amount, consistency and diversity of evidence, not on your own confidence.

CUSTOMER FEEDBACK:

{feedback_text}

Return only valid JSON using this structure:

{{
  "themes": [
    {{
      "theme": "",
      "pain_point": "",
      "evidence_ids": [],
      "evidence_strength": "",
      "interpretation": "",
      "potential_opportunity": "",
      "contradictory_evidence": []
    }}
  ]
}}
"""


def _validate_string_list(value, field_name, theme_index):
    if not isinstance(value, list):
        raise ValueError(
            f"Theme {theme_index} field '{field_name}' must be a list of feedback IDs."
        )

    cleaned = []
    seen = set()
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"Theme {theme_index} field '{field_name}' contains an invalid feedback ID."
            )
        feedback_id = item.strip()
        if feedback_id in seen:
            raise ValueError(
                f"Theme {theme_index} field '{field_name}' contains duplicate ID {feedback_id}."
            )
        seen.add(feedback_id)
        cleaned.append(feedback_id)
    return cleaned


def validate_analysis_result(result):
    """Validate the minimum structured contract required by the review UI."""
    if not isinstance(result, dict):
        raise ValueError("The model response must be a JSON object.")

    themes = result.get("themes")
    if not isinstance(themes, list):
        raise ValueError("The model response must contain a themes list.")

    validated_themes = []
    for index, theme in enumerate(themes, start=1):
        if not isinstance(theme, dict):
            raise ValueError(f"Theme {index} must be a JSON object.")

        missing = [field for field in REQUIRED_THEME_FIELDS if field not in theme]
        if missing:
            raise ValueError(
                f"Theme {index} is missing required fields: " + ", ".join(missing)
            )

        validated = dict(theme)
        for field in ("theme", "pain_point", "interpretation", "potential_opportunity"):
            value = validated.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Theme {index} field '{field}' must be a non-blank string.")
            validated[field] = value.strip()

        strength = validated.get("evidence_strength")
        if strength not in EVIDENCE_STRENGTHS:
            raise ValueError(
                f"Theme {index} evidence_strength must be one of: "
                + ", ".join(sorted(EVIDENCE_STRENGTHS))
            )

        validated["evidence_ids"] = _validate_string_list(
            validated.get("evidence_ids"), "evidence_ids", index
        )
        validated["contradictory_evidence"] = _validate_string_list(
            validated.get("contradictory_evidence"), "contradictory_evidence", index
        )
        validated_themes.append(validated)

    validated_result = dict(result)
    validated_result["themes"] = validated_themes
    return validated_result


def analyse_feedback_with_metadata(feedback, client=None):
    """Analyse feedback and preserve raw output plus run metadata."""
    feedback = validate_feedback_records(feedback)

    api_key = os.environ.get("OPENAI_API_KEY")
    if client is None and not api_key:
        raise RuntimeError("Set OPENAI_API_KEY before running an analysis.")

    model = os.environ.get("OPENAI_MODEL", "gpt-5.6")
    prompt = build_prompt(feedback)
    active_client = client or OpenAI(api_key=api_key)
    response = active_client.responses.create(model=model, input=prompt)
    raw_output = getattr(response, "output_text", None)

    if not isinstance(raw_output, str) or not raw_output.strip():
        raise ValueError("The model returned no usable text output.")

    try:
        parsed = json.loads(raw_output)
    except json.JSONDecodeError as error:
        raise ValueError("The model returned invalid JSON.") from error

    result = validate_analysis_result(parsed)
    return {
        "analysis": result,
        "raw_output": raw_output,
        "model": model,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "dataset_sha256": dataset_fingerprint(feedback),
        "record_count": len(feedback),
    }


def analyse_feedback(feedback, client=None):
    """Backward-compatible helper returning only the validated analysis."""
    return analyse_feedback_with_metadata(feedback, client=client)["analysis"]


def main():
    feedback = load_feedback()
    print(f"Loaded {len(feedback)} feedback records.")
    print("Analysing customer feedback...\n")
    print(json.dumps(analyse_feedback(feedback), indent=2))


if __name__ == "__main__":
    main()
