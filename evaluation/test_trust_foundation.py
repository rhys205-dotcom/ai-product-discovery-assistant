import json
import unittest
from unittest.mock import patch

from src.analyse_feedback import (
    analyse_feedback_with_metadata,
    dataset_fingerprint,
    validate_analysis_result,
    validate_feedback_records,
)


VALID_FEEDBACK = [
    {
        "feedback_id": "F001",
        "source": "Interview",
        "persona": "Finance",
        "feedback": "Month end reconciliation takes too long.",
    },
    {
        "feedback_id": "F002",
        "source": "Support",
        "persona": "Administrator",
        "feedback": "Failed payments are hard to spot.",
    },
]

VALID_ANALYSIS = {
    "themes": [
        {
            "theme": "Payment exceptions are hard to manage",
            "pain_point": "Users struggle to identify and resolve payment exceptions.",
            "evidence_ids": ["F001", "F002"],
            "evidence_strength": "Moderate",
            "interpretation": "The comments suggest exception handling needs clearer visibility.",
            "potential_opportunity": "Investigate an exception-focused review workflow.",
            "contradictory_evidence": [],
        }
    ]
}


class FakeResponse:
    def __init__(self, output_text):
        self.output_text = output_text


class FakeResponses:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error

    def create(self, **kwargs):
        if self.error:
            raise self.error
        return FakeResponse(self.output_text)


class FakeClient:
    def __init__(self, output_text=None, error=None):
        self.responses = FakeResponses(output_text=output_text, error=error)


class FeedbackValidationTests(unittest.TestCase):
    def test_rejects_blank_feedback_id(self):
        feedback = [dict(VALID_FEEDBACK[0], feedback_id="   ")]
        with self.assertRaisesRegex(ValueError, "blank feedback_id"):
            validate_feedback_records(feedback)

    def test_rejects_duplicate_feedback_id_after_whitespace_trim(self):
        feedback = [
            dict(VALID_FEEDBACK[0], feedback_id="F001"),
            dict(VALID_FEEDBACK[1], feedback_id=" F001 "),
        ]
        with self.assertRaisesRegex(ValueError, "Duplicate feedback_id: F001"):
            validate_feedback_records(feedback)

    def test_rejects_blank_feedback_text(self):
        feedback = [dict(VALID_FEEDBACK[0], feedback="   ")]
        with self.assertRaisesRegex(ValueError, "blank feedback text"):
            validate_feedback_records(feedback)

    def test_dataset_fingerprint_changes_when_content_changes(self):
        first = dataset_fingerprint(VALID_FEEDBACK)
        changed = [dict(item) for item in VALID_FEEDBACK]
        changed[1]["feedback"] = "A different statement."
        second = dataset_fingerprint(changed)
        self.assertNotEqual(first, second)

    def test_dataset_fingerprint_is_stable_after_normalisation(self):
        padded = [dict(item) for item in VALID_FEEDBACK]
        padded[0]["feedback_id"] = " F001 "
        padded[0]["feedback"] = "  Month end reconciliation takes too long.  "
        self.assertEqual(dataset_fingerprint(VALID_FEEDBACK), dataset_fingerprint(padded))


class AnalysisContractTests(unittest.TestCase):
    def test_rejects_missing_theme_fields(self):
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_analysis_result({"themes": [{}]})

    def test_rejects_invalid_evidence_strength(self):
        result = json.loads(json.dumps(VALID_ANALYSIS))
        result["themes"][0]["evidence_strength"] = "Very strong"
        with self.assertRaisesRegex(ValueError, "evidence_strength"):
            validate_analysis_result(result)

    def test_rejects_duplicate_evidence_id_in_one_finding(self):
        result = json.loads(json.dumps(VALID_ANALYSIS))
        result["themes"][0]["evidence_ids"] = ["F001", "F001"]
        with self.assertRaisesRegex(ValueError, "duplicate ID F001"):
            validate_analysis_result(result)

    def test_accepts_empty_theme_list_as_valid_abstention(self):
        self.assertEqual(validate_analysis_result({"themes": []}), {"themes": []})


class AnalysisMetadataTests(unittest.TestCase):
    def test_preserves_raw_output_and_provenance(self):
        raw = json.dumps(VALID_ANALYSIS)
        client = FakeClient(output_text=raw)
        with patch.dict("os.environ", {"OPENAI_MODEL": "test-model"}, clear=False):
            result = analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

        self.assertEqual(result["analysis"], VALID_ANALYSIS)
        self.assertEqual(result["raw_output"], raw)
        self.assertEqual(result["model"], "test-model")
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["dataset_sha256"], dataset_fingerprint(VALID_FEEDBACK))
        self.assertEqual(len(result["prompt_sha256"]), 64)
        self.assertTrue(result["generated_at"])

    def test_rejects_invalid_json(self):
        client = FakeClient(output_text="not json")
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

    def test_rejects_structurally_incomplete_json(self):
        client = FakeClient(output_text='{"themes":[{}]}')
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

    def test_propagates_failed_model_call(self):
        client = FakeClient(error=RuntimeError("provider unavailable"))
        with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)


if __name__ == "__main__":
    unittest.main()
