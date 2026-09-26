#!/usr/bin/env python3
"""Score a human-mapped analysis run against the documented reference.

Scorer v2 keeps every generated finding visible. It does not treat an unmatched
finding as automatically wrong, but unmatched findings, unknown mappings,
duplicate mappings and all invalid citations are surfaced explicitly.

Evidence precision is calculated at the finding-citation relationship level so
an ID used correctly in one finding cannot hide its incorrect use in another.
"""

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


SCORER_VERSION = "2.0"


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return json.load(file)


def valid_feedback_ids(path):
    with Path(path).open("r", encoding="utf-8") as file:
        return {row["feedback_id"] for row in csv.DictReader(file)}


def ratio(numerator, denominator):
    return round(numerator / denominator, 3) if denominator else 0.0


def _string_ids(value):
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item]


def evaluate(reference, run, valid_ids):
    reference_by_id = {theme["theme_id"]: theme for theme in reference["themes"]}
    reference_ids = set(reference_by_id)
    findings = run.get("themes", [])
    if not isinstance(findings, list):
        findings = []

    mapped_findings = defaultdict(list)
    explicit_unknown_ids = set()
    unmapped_findings = []
    unknown_mapped_findings = []
    all_citation_relationships = []
    invalid_citations = []
    distractor_citations = []
    per_finding = []

    distractors = set(reference.get("deliberate_distractors", []))

    relevant_core_relationships = 0
    valid_core_relationships_on_matched = 0
    relevant_qualification_relationships = 0
    valid_qualification_relationships_on_matched = 0
    reference_core_hits = set()
    reference_qualification_hits = set()

    for index, finding in enumerate(findings):
        finding = finding if isinstance(finding, dict) else {}
        theme_id = finding.get("theme_id")
        theme_name = finding.get("theme")
        evidence_ids = _string_ids(finding.get("evidence_ids", []))
        qualification_ids = _string_ids(finding.get("contradictory_evidence", []))

        if not theme_id:
            mapping_status = "unmapped"
            unmapped_findings.append({"finding_index": index, "theme": theme_name})
        elif theme_id not in reference_ids:
            mapping_status = "unknown"
            explicit_unknown_ids.add(theme_id)
            unknown_mapped_findings.append(
                {"finding_index": index, "theme_id": theme_id, "theme": theme_name}
            )
        else:
            mapping_status = "matched"
            mapped_findings[theme_id].append(index)

        reference_theme = reference_by_id.get(theme_id) if mapping_status == "matched" else None
        expected_core = set(reference_theme["required_evidence_ids"]) if reference_theme else set()
        expected_qualification = (
            set(reference_theme.get("contradictory_or_qualifying_ids", []))
            if reference_theme
            else set()
        )

        relevant_core = []
        irrelevant_core = []
        invalid_core = []
        relevant_qualification = []
        irrelevant_qualification = []
        invalid_qualification = []

        for field, ids in (
            ("evidence_ids", evidence_ids),
            ("contradictory_evidence", qualification_ids),
        ):
            for feedback_id in ids:
                relationship = {
                    "finding_index": index,
                    "theme_id": theme_id,
                    "field": field,
                    "feedback_id": feedback_id,
                }
                all_citation_relationships.append(relationship)
                if feedback_id not in valid_ids:
                    invalid_citations.append(relationship)

        for feedback_id in evidence_ids:
            if feedback_id in distractors:
                distractor_citations.append(
                    {
                        "finding_index": index,
                        "theme_id": theme_id,
                        "feedback_id": feedback_id,
                    }
                )
            if feedback_id not in valid_ids:
                invalid_core.append(feedback_id)
            elif mapping_status == "matched":
                valid_core_relationships_on_matched += 1
                if feedback_id in expected_core:
                    relevant_core_relationships += 1
                    reference_core_hits.add((theme_id, feedback_id))
                    relevant_core.append(feedback_id)
                else:
                    irrelevant_core.append(feedback_id)

        for feedback_id in qualification_ids:
            if feedback_id not in valid_ids:
                invalid_qualification.append(feedback_id)
            elif mapping_status == "matched":
                valid_qualification_relationships_on_matched += 1
                if feedback_id in expected_qualification:
                    relevant_qualification_relationships += 1
                    reference_qualification_hits.add((theme_id, feedback_id))
                    relevant_qualification.append(feedback_id)
                else:
                    irrelevant_qualification.append(feedback_id)

        per_finding.append(
            {
                "finding_index": index,
                "theme_id": theme_id,
                "theme": theme_name,
                "mapping_status": mapping_status,
                "relevant_core_citations": relevant_core,
                "irrelevant_core_citations": irrelevant_core,
                "invalid_core_citations": invalid_core,
                "relevant_qualifying_citations": relevant_qualification,
                "irrelevant_qualifying_citations": irrelevant_qualification,
                "invalid_qualifying_citations": invalid_qualification,
            }
        )

    mapping_counts = Counter(
        finding.get("theme_id")
        for finding in findings
        if isinstance(finding, dict) and finding.get("theme_id") in reference_ids
    )
    duplicate_mapped_theme_ids = sorted(
        theme_id for theme_id, count in mapping_counts.items() if count > 1
    )
    matched_ids = set(mapped_findings)
    missing_theme_ids = sorted(reference_ids - matched_ids)

    expected_core_pairs = {
        (theme["theme_id"], feedback_id)
        for theme in reference["themes"]
        for feedback_id in theme["required_evidence_ids"]
    }
    expected_qualification_pairs = {
        (theme["theme_id"], feedback_id)
        for theme in reference["themes"]
        for feedback_id in theme.get("contradictory_or_qualifying_ids", [])
    }

    valid_citation_relationship_count = sum(
        1
        for relationship in all_citation_relationships
        if relationship["feedback_id"] in valid_ids
    )

    per_reference_theme = []
    for theme_id in sorted(reference_ids):
        reference_theme = reference_by_id[theme_id]
        expected_core = set(reference_theme["required_evidence_ids"])
        expected_qualification = set(
            reference_theme.get("contradictory_or_qualifying_ids", [])
        )
        finding_indexes = mapped_findings.get(theme_id, [])
        theme_core_ids = []
        theme_qualification_ids = []
        for index in finding_indexes:
            finding = findings[index]
            theme_core_ids.extend(_string_ids(finding.get("evidence_ids", [])))
            theme_qualification_ids.extend(
                _string_ids(finding.get("contradictory_evidence", []))
            )

        valid_theme_core = [cid for cid in theme_core_ids if cid in valid_ids]
        relevant_theme_core = [cid for cid in valid_theme_core if cid in expected_core]
        valid_theme_qualification = [
            cid for cid in theme_qualification_ids if cid in valid_ids
        ]
        relevant_theme_qualification = [
            cid for cid in valid_theme_qualification if cid in expected_qualification
        ]

        per_reference_theme.append(
            {
                "theme_id": theme_id,
                "present": bool(finding_indexes),
                "mapped_finding_count": len(finding_indexes),
                "evidence_precision": ratio(
                    len(relevant_theme_core), len(valid_theme_core)
                ),
                "reference_evidence_coverage": ratio(
                    len(set(relevant_theme_core)), len(expected_core)
                ),
                "minimum_support_met": len(set(relevant_theme_core))
                >= reference_theme["minimum_support"],
                "qualification_coverage": ratio(
                    len(set(relevant_theme_qualification)),
                    len(expected_qualification),
                ),
                "qualification_precision": ratio(
                    len(relevant_theme_qualification),
                    len(valid_theme_qualification),
                ),
            }
        )

    return {
        "scorer_version": SCORER_VERSION,
        "run_metadata": run.get("run_metadata", {}),
        "summary": {
            "theme_coverage": ratio(len(matched_ids), len(reference_ids)),
            "evidence_precision": ratio(
                relevant_core_relationships,
                valid_core_relationships_on_matched,
            ),
            "reference_evidence_coverage": ratio(
                len(reference_core_hits), len(expected_core_pairs)
            ),
            "citation_validity": ratio(
                valid_citation_relationship_count,
                len(all_citation_relationships),
            ),
            "qualification_coverage": ratio(
                len(reference_qualification_hits),
                len(expected_qualification_pairs),
            ),
            "qualification_precision": ratio(
                relevant_qualification_relationships,
                valid_qualification_relationships_on_matched,
            ),
            "unmatched_finding_count": len(unmapped_findings)
            + len(unknown_mapped_findings),
            "duplicate_mapped_theme_count": len(duplicate_mapped_theme_ids),
        },
        "missing_theme_ids": missing_theme_ids,
        "unknown_theme_ids": sorted(explicit_unknown_ids),
        "duplicate_mapped_theme_ids": duplicate_mapped_theme_ids,
        "unmapped_findings": unmapped_findings,
        "unknown_mapped_findings": unknown_mapped_findings,
        "invalid_citations": invalid_citations,
        "distractor_citations": distractor_citations,
        "per_finding": per_finding,
        "per_reference_theme": per_reference_theme,
        "interpretation_notes": [
            "Scorer v2 evaluates citation relevance per finding-citation relationship.",
            "Citation validity includes citations from every generated finding, including unmatched findings.",
            "Unmatched findings are surfaced for human review rather than automatically scored as wrong.",
            "Coverage is measured against a contestable human reference, not objective truth.",
            "Qualification precision penalises irrelevant items added to contradictory/qualifying evidence.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", help="Human-mapped analysis-run JSON to evaluate")
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
