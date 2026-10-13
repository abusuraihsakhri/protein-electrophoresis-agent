"""Regression coverage for audit integrity and CSV flag handling."""
import csv
import io

import pytest

from agents.base import AuditTrail
from cli import main as legacy_main
from protein_electrophoresis_agent.cli import main as clinical_main


def test_audit_log_detects_modified_signature():
    trail = AuditTrail(secret_key="test-only-in-memory-signing-key")
    trail.log("test", "test", "EVENT", {"case": "SYNTHETIC"})
    assert trail.verify_integrity()
    trail.logs[0]["current_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_audit_log_detects_modified_signed_metadata():
    trail = AuditTrail(secret_key="test-only-in-memory-signing-key")
    trail.log("test", "test", "EVENT", {"case": "SYNTHETIC"})
    trail.logs[0]["event_type"] = "TAMPERED"
    assert not trail.verify_integrity()


def test_audit_trail_snapshot_is_not_mutable():
    trail = AuditTrail(secret_key="test-only-in-memory-signing-key")
    trail.log("test", "test", "EVENT", {"case": "SYNTHETIC"})
    snapshot = trail.get_trail()
    snapshot[0]["current_hash"] = "malicious"
    assert trail.verify_integrity()


@pytest.mark.parametrize("flag, expected_critical", [
    ("False", 0), ("false", 0), ("0", 0), ("", 0),
    ("True", 1), ("TRUE", 1), ("1", 1), ("yes", 1),
])
def test_legacy_batch_flag_parsing(tmp_path, flag, expected_critical):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    input_path.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        f"T-1,SYN-1,10,2,{flag},NOMINAL\n", encoding="utf-8",
    )
    assert legacy_main(["batch", "-i", str(input_path), "-o", str(output_path)]) == 0
    with output_path.open(newline="", encoding="utf-8") as handle:
        result = next(csv.DictReader(handle))
    assert int(result["total_alerts"]) == expected_critical


@pytest.mark.parametrize("flag, expected_critical", [
    ("False", 0), ("0", 0), ("True", 1), ("yes", 1),
])
def test_clinical_batch_flag_parsing(tmp_path, flag, expected_critical):
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    input_path.write_text(
        "case_id,patient_synthetic_id,metric_primary,metric_secondary,is_stat,status_flag\n"
        f"C-1,SYN-1,10,2,{flag},NORMAL\n", encoding="utf-8",
    )
    assert clinical_main(["batch", "-i", str(input_path), "-o", str(output_path)]) == 0
    with output_path.open(newline="", encoding="utf-8") as handle:
        result = next(csv.DictReader(handle))
    assert int(result["stat_critical_alerts"]) == expected_critical


@pytest.mark.parametrize("entrypoint", [legacy_main, clinical_main])
def test_batch_invalid_boolean_skips_row(tmp_path, entrypoint):
    is_clinical = entrypoint is clinical_main
    headings = (
        "case_id,patient_synthetic_id,metric_primary,metric_secondary,is_stat,status_flag"
        if is_clinical else
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor"
    )
    source = tmp_path / "input.csv"
    target = tmp_path / "out.csv"
    source.write_text(headings + "\n" + "T-1,SYN-1,10,2,maybe,NOMINAL\n", encoding="utf-8")
    assert entrypoint(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 0
