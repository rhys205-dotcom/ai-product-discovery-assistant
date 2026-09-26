import unittest

from evaluate import evaluate


REFERENCE = {
    "themes": [
        {
            "theme_id": "T01",
            "required_evidence_ids": ["F001", "F002"],
            "minimum_support": 1,
            "contradictory_or_qualifying_ids": ["F003"],
        },
        {
            "theme_id": "T02",
            "required_evidence_ids": ["F004"],
            "minimum_support": 1,
            "contradictory_or_qualifying_ids": [],
        },
    ],
    "deliberate_distractors": ["F005"],
}
VALID_IDS = {"F001", "F002", "F003", "F004", "F005"}


class EvaluateV2Tests(unittest.TestCase):
    def test_unmapped_finding_and_bad_citation_are_visible(self):
        run = {
            "themes": [
                {"theme_id": "T01", "theme": "Known", "evidence_ids": ["F001"]},
                {"theme": "Extra", "evidence_ids": ["F999"]},
            ]
        }
        result = evaluate(REFERENCE, run, VALID_IDS)
        self.assertEqual(result["summary"]["unmatched_finding_count"], 1)
        self.assertEqual(result["summary"]["citation_validity"], 0.5)
        self.assertEqual(result["invalid_citations"][0]["feedback_id"], "F999")

    def test_duplicate_mapping_does_not_overwrite_a_finding(self):
        run = {
            "themes": [
                {"theme_id": "T01", "theme": "A", "evidence_ids": ["F001"]},
                {"theme_id": "T01", "theme": "B", "evidence_ids": ["F005"]},
            ]
        }
        result = evaluate(REFERENCE, run, VALID_IDS)
        self.assertEqual(result["duplicate_mapped_theme_ids"], ["T01"])
        self.assertEqual(result["summary"]["evidence_precision"], 0.5)
        t01 = next(
            item for item in result["per_reference_theme"] if item["theme_id"] == "T01"
        )
        self.assertEqual(t01["mapped_finding_count"], 2)

    def test_same_id_is_scored_per_finding_relationship(self):
        reference = {
            "themes": [
                {
                    "theme_id": "T01",
                    "required_evidence_ids": ["F001"],
                    "minimum_support": 1,
                    "contradictory_or_qualifying_ids": [],
                },
                {
                    "theme_id": "T02",
                    "required_evidence_ids": ["F002"],
                    "minimum_support": 1,
                    "contradictory_or_qualifying_ids": [],
                },
            ],
            "deliberate_distractors": [],
        }
        run = {
            "themes": [
                {"theme_id": "T01", "evidence_ids": ["F001"]},
                {"theme_id": "T02", "evidence_ids": ["F001", "F002"]},
            ]
        }
        result = evaluate(reference, run, {"F001", "F002"})
        self.assertEqual(result["summary"]["evidence_precision"], 0.667)

    def test_irrelevant_qualification_reduces_precision(self):
        run = {
            "themes": [
                {
                    "theme_id": "T01",
                    "evidence_ids": ["F001"],
                    "contradictory_evidence": ["F003", "F004"],
                }
            ]
        }
        result = evaluate(REFERENCE, run, VALID_IDS)
        self.assertEqual(result["summary"]["qualification_precision"], 0.5)
        finding = result["per_finding"][0]
        self.assertEqual(finding["irrelevant_qualifying_citations"], ["F004"])


if __name__ == "__main__":
    unittest.main()
