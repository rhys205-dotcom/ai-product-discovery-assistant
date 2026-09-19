import csv
import json
import os
from pathlib import Path

from openai import OpenAI


DATA_FILE = Path(__file__).parent.parent / "data" / "sample-feedback.csv"


def load_feedback(data_file=DATA_FILE):
    """Load customer feedback from a CSV dataset."""
    with Path(data_file).open("r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def build_prompt(feedback):
    """Create the product-discovery analysis prompt."""
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


def analyse_feedback(feedback, client=None):
    """Analyse feedback and return a parsed, validated result."""
    if not feedback:
        raise ValueError("At least one feedback record is required.")

    api_key = os.environ.get("OPENAI_API_KEY")
    if client is None and not api_key:
        raise RuntimeError("Set OPENAI_API_KEY before running an analysis.")

    active_client = client or OpenAI(api_key=api_key)
    response = active_client.responses.create(
        model=os.environ.get("OPENAI_MODEL", "gpt-5.6"),
        input=build_prompt(feedback),
    )

    try:
        result = json.loads(response.output_text)
    except json.JSONDecodeError as error:
        raise ValueError("The model returned invalid JSON.") from error

    if not isinstance(result.get("themes"), list):
        raise ValueError("The model response must contain a themes list.")
    return result


def main():
    feedback = load_feedback()
    print(f"Loaded {len(feedback)} feedback records.")
    print("Analysing customer feedback...\n")
    print(json.dumps(analyse_feedback(feedback), indent=2))


if __name__ == "__main__":
    main()
