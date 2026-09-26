import json
import unittest
from unittest.mock import patch

from src.analyse_feedback import (
    PROMPT_VERSION,
    analyse_feedback_with_metadata,
    build_prompt,
    dataset_fingerprint,
    find_exact_duplicate_groups,
    validate_analysis_result,
    validate_feedback_records,
)
from src.review_integrity import (
    analysis_matches_dataset,
    bind_dataset,
    build_review_export,
    clear_analysis_state,
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
    ],
    "isolated_signals": [],
}

VALID_SIGNAL = {
    "signal": "Possible cross-account record access",
    "evidence_ids": ["F002"],
    "why_it_matters": "If reproducible, the observation could indicate a data-isolation problem.",
    "uncertainty": "This is one report and does not confirm a breach or root cause.",
    "recommended_next_step": "Verify the report and reproduce the access path before deciding on remediation.",
}


class FakeInteraction:
    def __init__(self, output_text):
        self.output_text = output_text


class FakeInteractions:
    def __init__(self, output_text=None, error=None):
        self.output_text = output_text
        self.error = error

    def create(self, **kwargs):
        if self.error:
            raise self.error
        return FakeInteraction(self.output_text)


class FakeClient:
    def __init__(self, output_text=None, error=None):
        self.interactions = FakeInteractions(output_text=output_text, error=error)


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

    def test_exact_duplicate_groups_are_flagged_without_assuming_identity(self):
        feedback = [
            dict(VALID_FEEDBACK[0], feedback_id="D1"),
            dict(VALID_FEEDBACK[0], feedback_id="D2"),
            dict(VALID_FEEDBACK[1], feedback_id="D3"),
        ]
        groups = find_exact_duplicate_groups(feedback)
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0]["feedback_ids"], ["D1", "D2"])
        self.assertEqual(groups[0]["count"], 2)
        self.assertEqual(groups[0]["source"], "Interview")
        self.assertEqual(groups[0]["persona"], "Finance")

    def test_varied_feedback_is_not_marked_duplicate(self):
        self.assertEqual(find_exact_duplicate_groups(VALID_FEEDBACK), [])

    def test_prompt_exposes_duplicate_context_and_abstention_rules(self):
        feedback = [
            dict(VALID_FEEDBACK[0], feedback_id="D1"),
            dict(VALID_FEEDBACK[0], feedback_id="D2"),
        ]
        prompt = build_prompt(feedback)
        self.assertIn("D1, D2 repeat the same text/source/persona", prompt)
        self.assertIn("It is valid to return no themes", prompt)
        self.assertIn("neutral/non-applicable evidence, not contradiction", prompt)
        self.assertIn("isolated_signals", prompt)


class AnalysisContractTests(unittest.TestCase):
    def test_rejects_missing_theme_fields(self):
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_analysis_result({"themes": [{}], "isolated_signals": []})

    def test_requires_isolated_signals_list(self):
        with self.assertRaisesRegex(ValueError, "isolated_signals"):
            validate_analysis_result({"themes": []})

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

    def test_rejects_incomplete_isolated_signal(self):
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            validate_analysis_result(
                {"themes": [], "isolated_signals": [{"signal": "Possible issue"}]}
            )

    def test_accepts_valid_isolated_signal(self):
        result = {"themes": [], "isolated_signals": [dict(VALID_SIGNAL)]}
        self.assertEqual(validate_analysis_result(result), result)

    def test_accepts_empty_theme_and_signal_lists_as_valid_abstention(self):
        result = {"themes": [], "isolated_signals": []}
        self.assertEqual(validate_analysis_result(result), result)


class AnalysisMetadataTests(unittest.TestCase):
    def test_preserves_raw_output_and_provenance(self):
        raw = json.dumps(VALID_ANALYSIS)
        client = FakeClient(output_text=raw)
        with patch.dict("os.environ", {"GEMINI_MODEL": "test-model"}, clear=False):
            result = analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

        self.assertEqual(result["analysis"], VALID_ANALYSIS)
        self.assertEqual(result["raw_output"], raw)
        self.assertEqual(result["provider"], "Google")
        self.assertEqual(result["model"], "test-model")
        self.assertEqual(result["prompt_version"], PROMPT_VERSION)
        self.assertEqual(result["record_count"], 2)
        self.assertEqual(result["dataset_sha256"], dataset_fingerprint(VALID_FEEDBACK))
        self.assertEqual(result["duplicate_evidence_groups"], [])
        self.assertEqual(len(result["prompt_sha256"]), 64)
        self.assertTrue(result["generated_at"])

    def test_metadata_includes_duplicate_groups(self):
        feedback = [
            dict(VALID_FEEDBACK[0], feedback_id="D1"),
            dict(VALID_FEEDBACK[0], feedback_id="D2"),
        ]
        raw = json.dumps({"themes": [], "isolated_signals": []})
        result = analyse_feedback_with_metadata(feedback, client=FakeClient(output_text=raw))
        self.assertEqual(result["duplicate_evidence_groups"][0]["feedback_ids"], ["D1", "D2"])

    def test_rejects_invalid_json(self):
        client = FakeClient(output_text="not json")
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

    def test_rejects_structurally_incomplete_json(self):
        client = FakeClient(output_text='{"themes":[{}],"isolated_signals":[]}')
        with self.assertRaisesRegex(ValueError, "missing required fields"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)

    def test_propagates_failed_model_call(self):
        client = FakeClient(error=RuntimeError("provider unavailable"))
        with self.assertRaisesRegex(RuntimeError, "provider unavailable"):
            analyse_feedback_with_metadata(VALID_FEEDBACK, client=client)


class ReviewIntegrityTests(unittest.TestCase):
    def test_dataset_change_clears_analysis_failure_and_review_state(self):
        state = {
            "active_dataset_sha256": "dataset-a",
            "active_dataset_source": "a.csv",
            "analysis": {"themes": [], "isolated_signals": []},
            "analysis_original": {"themes": [], "isolated_signals": []},
            "analysis_raw_output": "{}",
            "analysis_metadata": {"dataset_sha256": "dataset-a"},
            "last_analysis_failure": {"error": "old failure"},
            "review:run-a:0:decision": "Accept",
            "decision-0": "Reject",
            "unrelated": "keep me",
        }

        changed = bind_dataset(state, "dataset-b", "b.csv")

        self.assertTrue(changed)
        self.assertEqual(state["active_dataset_sha256"], "dataset-b")
        self.assertEqual(state["active_dataset_source"], "b.csv")
        self.assertEqual(state["unrelated"], "keep me")
        self.assertNotIn("analysis", state)
        self.assertNotIn("analysis_original", state)
        self.assertNotIn("analysis_raw_output", state)
        self.assertNotIn("analysis_metadata", state)
        self.assertNotIn("last_analysis_failure", state)
        self.assertNotIn("review:run-a:0:decision", state)
        self.assertNotIn("decision-0", state)

    def test_same_dataset_keeps_bound_analysis(self):
        state = {
            "active_dataset_sha256": "dataset-a",
            "analysis": {"themes": [], "isolated_signals": []},
            "analysis_metadata": {"dataset_sha256": "dataset-a"},
        }
        changed = bind_dataset(state, "dataset-a", "renamed.csv")
        self.assertFalse(changed)
        self.assertIn("analysis", state)
        self.assertEqual(state["active_dataset_source"], "renamed.csv")

    def test_new_analysis_attempt_clears_review_state(self):
        state = {
            "analysis": {"themes": [], "isolated_signals": []},
            "review:run-a:0:note": "old note",
            "note-0": "legacy note",
            "last_analysis_failure": {"error": "old"},
        }
        clear_analysis_state(state)
        self.assertEqual(state, {})

    def test_analysis_must_match_active_dataset(self):
        self.assertTrue(
            analysis_matches_dataset({"dataset_sha256": "dataset-a"}, "dataset-a")
        )
        self.assertFalse(
            analysis_matches_dataset({"dataset_sha256": "dataset-a"}, "dataset-b")
        )
        self.assertFalse(analysis_matches_dataset(None, "dataset-a"))

    def test_export_preserves_original_reviewed_output_signals_and_provenance(self):
        metadata = {
            "run_id": "run-123",
            "dataset_sha256": "dataset-a",
            "dataset_source": "feedback.csv",
            "provider": "Google",
            "model": "test-model",
            "prompt_version": "v2",
        }
        original = json.loads(json.dumps(VALID_ANALYSIS))
        original["isolated_signals"] = [dict(VALID_SIGNAL)]
        reviewed = json.loads(json.dumps(VALID_ANALYSIS["themes"]))
        reviewed[0]["interpretation"] = "Human-edited interpretation."
        reviewed[0]["human_review"] = {
            "decision": "Edit and accept",
            "note": "Tightened claim.",
        }
        reviewed_signals = [dict(VALID_SIGNAL)]
        reviewed_signals[0]["uncertainty"] = "Human-edited uncertainty."
        reviewed_signals[0]["human_review"] = {
            "decision": "Edit and accept",
            "note": "Keep investigation cautious.",
        }

        export = build_review_export(
            metadata,
            original,
            json.dumps(original),
            reviewed,
            reviewed_signals=reviewed_signals,
            exported_at="2026-09-26T14:30:00+00:00",
        )

        self.assertEqual(export["export_version"], "2.1")
        self.assertEqual(export["provenance"]["run_id"], "run-123")
        self.assertEqual(export["provenance"]["dataset_sha256"], "dataset-a")
        self.assertEqual(export["provenance"]["provider"], "Google")
        self.assertEqual(
            export["provenance"]["exported_at"], "2026-09-26T14:30:00+00:00"
        )
        self.assertEqual(
            export["original_model_output"]["parsed"]["themes"][0]["interpretation"],
            VALID_ANALYSIS["themes"][0]["interpretation"],
        )
        self.assertEqual(
            export["reviewed_analysis"]["themes"][0]["interpretation"],
            "Human-edited interpretation.",
        )
        self.assertEqual(
            export["reviewed_analysis"]["isolated_signals"][0]["uncertainty"],
            "Human-edited uncertainty.",
        )


if __name__ == "__main__":
    unittest.main()
