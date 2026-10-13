"""
Clinical Algorithmic Engine & Guideline Rules for SpepMind: Serum & Urine Protein Electrophoresis M-Spike Quantifier Agent.
Domain: Clinical Chemistry
Standard: IFCC & KDOQI Laboratory Standards
"""
import math
from typing import Dict, Any, List, Optional
from .models import ClinicalCasePayload, AgentAlert, UrgencyLevel, ClinicalIntegrityStatus


class ClinicalDomainEngine:
    GUIDELINE = "Unvalidated demonstration-only thresholds"
    PRIMARY_BASELINE_LIMIT = 20.0
    SECONDARY_ALERT_LIMIT = 10.0

    @classmethod
    def evaluate_primary_index(cls, value: float) -> Optional[Dict[str, Any]]:
        if value > cls.PRIMARY_BASELINE_LIMIT:
            return {
                "title": "Primary Metric Threshold Exceeded",
                "finding": f"Observed value ({value:.2f}) exceeds the demonstration threshold ({cls.PRIMARY_BASELINE_LIMIT:.1f}); units and clinical interpretation are undefined.",
                "recommendation": "Review inputs manually; this demo is not a clinical decision tool.",
            }
        return None

    @classmethod
    def evaluate_secondary_kinetics(cls, value: float, is_stat: bool) -> Optional[Dict[str, Any]]:
        if value > cls.SECONDARY_ALERT_LIMIT or is_stat:
            return {
                "title": "Demonstration Kinetic Flag Triggered",
                "finding": f"Kinetic parameter ({value:.2f}) with STAT={is_stat} requires prioritized supervision.",
                "recommendation": "Review this example flag; it does not establish clinical urgency.",
            }
        return None

    @classmethod
    def evaluate_biomarker_concordance(cls, status_flag: str, biomarkers: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        status_upper = str(status_flag).upper()
        if "DISCORDANT" in status_upper or "EQUIVOCAL" in status_upper or "MUTANT" in status_upper:
            return {
                "title": "Phenotypic / Biomarker Discordance Identified",
                "finding": f"Status flag '{status_flag}' indicates divergence from standard diagnostic concordance.",
                "recommendation": "Review the original source results; no reflex-testing recommendation is validated by this demonstration.",
            }
        return None
