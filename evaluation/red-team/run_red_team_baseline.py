import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analyse_feedback import (
    analyse_feedback_with_metadata,
    build_prompt,
    dataset_fingerprint,
    load_feedback,
)


MANIFEST = ROOT / "evaluation" / "red-team" / "cases.json"
OUTPUT_ROOT = ROOT / "evaluation" / "red-team" / "runs"


def parse_args():
    parser = argparse.ArgumentParser(description="Run red-team model cases against the current application configuration.")
    parser.add_argument("--cases", help="Comma-separated case IDs, for example E10,E11,E12")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs per selected model case (default: 1)")
    return parser.parse_args()


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def selected_cases(manifest, requested):
    cases = [case for case in manifest["cases"] if case["type"] == "model"]
    if not requested:
        return cases
    wanted = {item.strip().upper() for item in requested.split(",") if item.strip()}
    unknown = wanted.difference({case["id"] for case in cases})
    if unknown:
        raise ValueError(f"Unknown or non-model cases: {', '.join(sorted(unknown))}")
    return [case for case in cases if case["id"] in wanted]


def prompt_hash(feedback):
    return hashlib.sha256(build_prompt(feedback).encode("utf-8")).hexdigest()


def write_json(path, payload):
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main():
    args = parse_args()
    if args.runs < 1:
        raise ValueError("--runs must be at least 1")

    manifest = load_manifest()
    cases = selected_cases(manifest, args.cases)
    model = os.environ.get("OPENAI_MODEL", "gpt-5.6")
    suite_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suite_dir = OUTPUT_ROOT / suite_stamp
    suite_dir.mkdir(parents=True, exist_ok=False)

    suite_manifest = {
        "suite_version": manifest["suite_version"],
        "started_at": datetime.now(timezone.utc).isoformat(),
        "model": model,
        "runs_per_case": args.runs,
        "baseline_note": "Current OpenAI-backed application analysis contract; failures and invalid outputs are retained as results.",
        "cases": [],
    }

    try:
        for case in cases:
            dataset_path = ROOT / case["dataset"]
            feedback = load_feedback(dataset_path)
            case_dir = suite_dir / case["id"]
            case_dir.mkdir()
            case_record = {
                "id": case["id"],
                "name": case["name"],
                "dataset": case["dataset"],
                "dataset_sha256": dataset_fingerprint(feedback),
                "planned_severity": case["severity"],
                "expected": case["expected"],
                "record_count": len(feedback),
                "prompt_sha256": prompt_hash(feedback),
                "runs": [],
            }

            for run_number in range(1, args.runs + 1):
                started = datetime.now(timezone.utc)
                output_file = case_dir / f"run-{run_number}.json"

                try:
                    result = analyse_feedback_with_metadata(feedback)
                except Exception as error:
                    finished = datetime.now(timezone.utc)
                    output = {
                        "case_id": case["id"],
                        "case_name": case["name"],
                        "dataset": case["dataset"],
                        "dataset_sha256": case_record["dataset_sha256"],
                        "model": model,
                        "prompt_sha256": case_record["prompt_sha256"],
                        "run_number": run_number,
                        "started_at": started.isoformat(),
                        "finished_at": finished.isoformat(),
                        "status": "error",
                        "error": {
                            "type": type(error).__name__,
                            "message": str(error),
                        },
                    }
                else:
                    finished = datetime.now(timezone.utc)
                    output = {
                        "case_id": case["id"],
                        "case_name": case["name"],
                        "dataset": case["dataset"],
                        "dataset_sha256": result["dataset_sha256"],
                        "model": result["model"],
                        "prompt_sha256": result["prompt_sha256"],
                        "run_number": run_number,
                        "started_at": started.isoformat(),
                        "finished_at": finished.isoformat(),
                        "status": "success",
                        "raw_model_output": result["raw_output"],
                        "parsed_result": result["analysis"],
                    }

                write_json(output_file, output)
                relative_output = str(output_file.relative_to(ROOT))
                case_record["runs"].append(
                    {"path": relative_output, "status": output["status"]}
                )
                print(
                    f"{case['id']} run {run_number}: {output['status']} — saved {relative_output}"
                )

            suite_manifest["cases"].append(case_record)
    finally:
        suite_manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
        manifest_path = suite_dir / "manifest.json"
        write_json(manifest_path, suite_manifest)
        print(f"\nSuite manifest: {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
