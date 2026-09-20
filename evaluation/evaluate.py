#!/usr/bin/env python3
"""Score an analysis run against the documented human reference.

This is a transparent baseline, not a semantic judge. Theme matching uses stable
theme IDs and evidence scoring uses explicit feedback IDs so the calculation is
repeatable and easy to challenge.
"""

import argparse
import csv
import json
from pathlib import Path


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def valid_feedback_ids(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return {row["feedback_id"] for row in csv.DictReader(file)}


def ratio(numerator, denominator):
    return round(numerator / denominator, 3) if denominator else 0.0


def evaluate(reference, run, valid_ids):
    reference_by_id = {theme["theme_id"]: theme for theme in reference["themes"]}
    generated_by_id = {
        theme.get("theme_id"): theme
        for theme in run.get("themes", [])
        if theme.get("theme_id")
    }

    generated_ids = set(generated_by_id)
    reference_ids = set(reference_by_id)
    matched_ids = generated_ids & reference_ids
    unknown_theme_ids = sorted(generated_ids - reference_ids)
    missing_theme_ids = sorted(reference_ids - generated_ids)

    cited = set()
    relevant = set()
    expected = set()
    contradiction_hits = set()
    expected_contradictions = set()
    per_theme = []

    for theme_id in sorted(reference_ids):
        reference_theme = reference_by_id[theme_id]
        expected_ids = set(reference_theme["required_evidence_ids"])
        expected |= expected_ids
        expected_contradictions |= set(
            reference_theme.get("contradictory_or_qualifying_ids", [])
        )
        generated_theme = generated_by_id.get(theme_id, {})
        theme_citations = set(generated_theme.get("evidence_ids", []))
        theme_contradictions = set(generated_theme.get("contradictory_evidence", []))
        cited |= theme_citations
        relevant |= theme_citations & expected_ids
        contradiction_hits |= theme_contradictions & set(
            reference_theme.get("contradictory_or_qualifying_ids", [])
        )
        per_theme.append(
            {
                "theme_id": theme_id,
                "present": theme_id in generated_by_id,
                "evidence_precision": ratio(
                    len(theme_citations & expected_ids), len(theme_citations)
                ),
                "reference_evidence_coverage": ratio(
                    len(theme_citations & expected_ids), len(expected_ids)
                ),
                "minimum_support_met": len(theme_citations & expected_ids)
                >= reference_theme["minimum_support"],
            }
        )

    invalid_citations = sorted(cited - valid_ids)
    distractor_citations = sorted(cited & set(reference.get("deliberate_distractors", [])))
    valid_citations = cited & valid_ids

    return {
        "run_metadata": run.get("run_metadata", {}),
        "summary": {
            "theme_coverage": ratio(len(matched_ids), len(reference_ids)),
            "evidence_precision": ratio(len(relevant), len(valid_citations)),
            "reference_evidence_coverage": ratio(len(relevant), len(expected)),
            "citation_validity": ratio(len(valid_citations), len(cited)),
            "contradiction_coverage": ratio(
                len(contradiction_hits), len(expected_contradictions)
            ),
        },
        "missing_theme_ids": missing_theme_ids,
        "unknown_theme_ids": unknown_theme_ids,
        "invalid_citations": invalid_citations,
        "distractor_citations": distractor_citations,
        "per_theme": per_theme,
        "interpretation_notes": [
            "A valid feedback ID may still be irrelevant; inspect per-theme evidence precision.",
            "Coverage is measured against a contestable human reference, not absolute truth.",
            "Usefulness and factual nuance still require human review."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", help="Analysis-run JSON to evaluate")
    parser.add_argument(
        "--reference",
        default="evaluation/reference-analysis.json",
        help="Human reference JSON",
    )
    parser.add_argument(
        "--data",
        default="data/sample-feedback.csv",
        help="Source feedback CSV",
    )
    parser.add_argument("--output", help="Optional path for the score JSON")
    args = parser.parse_args()

    result = evaluate(
        load_json(args.reference), load_json(args.run), valid_feedback_ids(args.data)
    )
    rendered = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
