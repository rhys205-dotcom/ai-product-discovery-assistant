#!/usr/bin/env python3
"""Run exactly three controlled historical Gemini analyses using frozen prompt v1.

This runner is intentionally isolated from the current application prompt so a
future prompt change cannot silently rewrite the historical experiment. The API
key is read from GEMINI_API_KEY and is never written to disk.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from google import genai

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analyse_feedback import load_feedback


RUN_COUNT = 3
PROMPT_VERSION = "v1"
DEFAULT_MODEL = "gemini-3.5-flash"
OUTPUT_ROOT = Path("evaluation/runs")

FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "themes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "theme": {"type": "string"},
                    "pain_point": {"type": "string"},
                    "evidence_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "evidence_strength": {
                        "type": "string",
                        "enum": ["Strong", "Moderate", "Limited"],
                    },
                    "interpretation": {"type": "string"},
                    "potential_opportunity": {"type": "string"},
                    "contradictory_evidence": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "theme",
                    "pain_point",
                    "evidence_ids",
                    "evidence_strength",
                    "interpretation",
                    "potential_opportunity",
                    "contradictory_evidence",
                ],
            },
        }
    },
    "required": ["themes"],
}


def build_historical_prompt_v1(feedback):
    """Frozen copy of the prompt used by the September 2026 benchmark."""
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


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_once(client, model, prompt, run_number, benchmark_id, record_count):
    interaction = client.interactions.create(
        model=model,
        input=prompt,
        store=False,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": FINDINGS_SCHEMA,
        },
    )
    result = json.loads(interaction.output_text)
    if not isinstance(result.get("themes"), list):
        raise ValueError("Gemini returned JSON without a themes list.")

    return {
        "run_metadata": {
            "benchmark_id": benchmark_id,
            "run_id": f"{benchmark_id}-run-{run_number}",
            "run_number": run_number,
            "provider": "Google",
            "model": model,
            "prompt_version": PROMPT_VERSION,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "dataset": "data/sample-feedback.csv",
            "record_count": record_count,
            "generated_at": utc_now(),
            "human_theme_mapping_status": "pending",
        },
        "themes": result["themes"],
    }


def main():
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit(
            "GEMINI_API_KEY is not set. Store it as an environment variable; "
            "never add it to this repository."
        )

    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    feedback = load_feedback()
    prompt = build_historical_prompt_v1(feedback)
    benchmark_id = datetime.now(timezone.utc).strftime("gemini-v1-%Y%m%dT%H%M%SZ")
    output_dir = OUTPUT_ROOT / benchmark_id
    output_dir.mkdir(parents=True, exist_ok=False)

    manifest = {
        "benchmark_id": benchmark_id,
        "provider": "Google",
        "model": model,
        "prompt_version": PROMPT_VERSION,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "dataset": "data/sample-feedback.csv",
        "record_count": len(feedback),
        "planned_runs": RUN_COUNT,
        "created_at": utc_now(),
        "status": "running",
        "runs": [],
        "notes": [
            "Historical runner: prompt v1 is embedded here and does not import the current application prompt.",
            "The API key is not stored in this manifest.",
            "Raw outputs require human theme mapping before scoring.",
            "Synthetic public data only."
        ],
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    for run_number in range(1, RUN_COUNT + 1):
        result = run_once(
            client, model, prompt, run_number, benchmark_id, len(feedback)
        )
        filename = f"run-{run_number}.json"
        (output_dir / filename).write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
        manifest["runs"].append(
            {
                "run_number": run_number,
                "file": filename,
                "theme_count": len(result["themes"]),
                "status": "completed",
            }
        )
        manifest_path.write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Completed run {run_number} of {RUN_COUNT}: {output_dir / filename}")

    manifest["status"] = "awaiting_human_mapping_and_scoring"
    manifest["completed_at"] = utc_now()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Benchmark complete. Review the raw outputs in {output_dir}")


if __name__ == "__main__":
    main()
