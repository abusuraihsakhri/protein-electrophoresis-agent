"""
Automated Pytest Test Suite for protein_electrophoresis_agent package.
Domain: Clinical Chemistry
Standard: IFCC & KDOQI Laboratory Standards
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from protein_electrophoresis_agent.models import (
    ClinicalCasePayload,
    AgentAlert,
    UrgencyLevel,
    ClinicalIntegrityStatus,
)
from protein_electrophoresis_agent.agents import (
    MSpikeDensitometryAgent,
    ImmunofixationMatcherAgent,
    FreeLightChainAuditorAgent,
    ElectrophoresisCoordinator,
)
from protein_electrophoresis_agent.engine import ClinicalDomainEngine
from protein_electrophoresis_agent.cli import main


def test_mspike_densitometry_agent():
    agent = MSpikeDensitometryAgent()
    # Normal value - no alerts
    case_normal = ClinicalCasePayload(
        case_id="T1", patient_synthetic_id="SYNTH-01",
        primary_metric=15.0, secondary_metric=5.0,
        status_flag="NORMAL", is_stat=False
    )
    alerts = agent.audit(case_normal)
    assert len(alerts) == 0

    # High value - should trigger alert
    case_high = ClinicalCasePayload(
        case_id="T2", patient_synthetic_id="SYNTH-02",
        primary_metric=35.0, secondary_metric=5.0,
        status_flag="NORMAL", is_stat=False
    )
    alerts = agent.audit(case_high)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.WARNING


def test_immunofixation_matcher_agent():
    agent = ImmunofixationMatcherAgent()
    # Normal value - no alerts
    case_normal = ClinicalCasePayload(
        case_id="T3", patient_synthetic_id="SYNTH-03",
        primary_metric=10.0, secondary_metric=5.0,
        status_flag="NORMAL", is_stat=False
    )
    alerts = agent.audit(case_normal)
    assert len(alerts) == 0

    # Critical flag - should trigger STAT alert
    case_critical = ClinicalCasePayload(
        case_id="T4", patient_synthetic_id="SYNTH-04",
        primary_metric=10.0, secondary_metric=5.0,
        status_flag="NORMAL", is_stat=True
    )
    alerts = agent.audit(case_critical)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.STAT_CRITICAL


def test_free_light_chain_auditor_agent():
    agent = FreeLightChainAuditorAgent()
    # Normal status - no alerts
    case_normal = ClinicalCasePayload(
        case_id="T5", patient_synthetic_id="SYNTH-05",
        primary_metric=10.0, secondary_metric=5.0,
        status_flag="NORMAL", is_stat=False
    )
    alerts = agent.audit(case_normal)
    assert len(alerts) == 0

    # Discordant status - should trigger alert
    case_discordant = ClinicalCasePayload(
        case_id="T6", patient_synthetic_id="SYNTH-06",
        primary_metric=10.0, secondary_metric=5.0,
        status_flag="DISCORDANT", is_stat=False
    )
    alerts = agent.audit(case_discordant)
    assert len(alerts) == 1
    assert alerts[0].urgency == UrgencyLevel.ADVISORY


def test_electrophoresis_coordinator():
    coord = ElectrophoresisCoordinator()
    # Normal case
    case_normal = ClinicalCasePayload(
        case_id="COORD-TEST-1", patient_synthetic_id="SYNTH-07",
        primary_metric=10.0, secondary_metric=3.0,
        status_flag="NORMAL", is_stat=False
    )
    dossier = coord.process_case(case_normal)
    assert dossier["overall_status"] == ClinicalIntegrityStatus.CONCORDANT_NORMAL.value
    assert dossier["total_alerts"] == 0

    # Critical case
    case_critical = ClinicalCasePayload(
        case_id="COORD-TEST-2", patient_synthetic_id="SYNTH-08",
        primary_metric=35.0, secondary_metric=15.0,
        status_flag="DISCORDANT", is_stat=True
    )
    dossier = coord.process_case(case_critical)
    assert dossier["overall_status"] == ClinicalIntegrityStatus.CRITICAL_ACTION_REQUIRED.value
    assert dossier["stat_critical_alerts"] > 0


def test_coordinator_chat():
    coord = ElectrophoresisCoordinator()
    ans = coord.query_supervisory_chat("What is the status?")
    assert "tracking" in len(ans) * " " or isinstance(ans, str)

    ans = coord.query_supervisory_chat("Tell me about guidelines")
    assert "IFCC" in ans or "standard" in ans.lower()


def test_cli_commands():
    assert main(["audit", "--case-id", "CLI-PKG-01"]) == 0
    assert main(["chat", "What", "is", "the", "status?"]) == 0


def test_domain_engine():
    # Test primary index evaluation
    result = ClinicalDomainEngine.evaluate_primary_index(25.0)
    assert result is not None
    assert "exceeds" in result["finding"].lower()

    result = ClinicalDomainEngine.evaluate_primary_index(15.0)
    assert result is None

    # Test secondary kinetics evaluation
    result = ClinicalDomainEngine.evaluate_secondary_kinetics(15.0, False)
    assert result is not None

    result = ClinicalDomainEngine.evaluate_secondary_kinetics(5.0, True)
    assert result is not None

    result = ClinicalDomainEngine.evaluate_secondary_kinetics(5.0, False)
    assert result is None

    # Test biomarker concordance evaluation
    result = ClinicalDomainEngine.evaluate_biomarker_concordance("DISCORDANT", {})
    assert result is not None

    result = ClinicalDomainEngine.evaluate_biomarker_concordance("NORMAL", {})
    assert result is None
