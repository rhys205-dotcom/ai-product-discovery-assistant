import csv
import json
import os
from pathlib import Path

from openai import OpenAI


DATA_FILE = Path(__file__).parent.parent / "data" / "sample-feedback.csv"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def load_feedback():
    """Load customer feedback from the sample CSV dataset."""
    with DATA_FILE.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


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

Evidence strength must be one of:

- Strong
- Moderate
- Limited

Base evidence strength on the amount, consistency and diversity of evidence,
not on your own confidence.

CUSTOMER FEEDBACK:

{feedback_text}

Return your response as valid JSON using this structure:

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


def analyse_feedback(feedback):
    """Send the feedback to the language model for analysis."""

    prompt = build_prompt(feedback)

    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text


def main():
    feedback = load_feedback()

    print(f"Loaded {len(feedback)} feedback records.")
    print("Analysing customer feedback...\n")

    result = analyse_feedback(feedback)

    try:
        parsed = json.loads(result)
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError:
        print(result)


if __name__ == "__main__":
    main()
