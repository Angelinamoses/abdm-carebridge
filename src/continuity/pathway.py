"""
pathway.py — implements the decision logic from the hybrid continuity
architecture (see docs/architecture.md, Figure 2):

    ABHA available?
        No  -> privacy-preserving record linkage (PPRL) fallback
        Yes -> standard FHIR-based HIE exchange
    Both -> federated query engine -> continuity of care

This module sits between the journey simulator (src/simulation) and the
evaluation scripts (evaluation/). It does not implement a real PPRL
algorithm -- see docs/limitations.md, Section 3. It models the *effect*
a working fallback pathway would have: some fraction of otherwise-broken
continuity stages become recoverable once a fallback linkage step runs.
"""

import random

PRIMARY_PATHWAY = "fhir_exchange"
FALLBACK_PATHWAY = "pprl_fallback"

BREAK_STATUSES = {"lost", "at_risk", "isolated", "duplicated"}


def decide_pathway(has_abha: bool) -> str:
    """
    Mirrors the 'ABHA available?' decision node in the architecture diagram.
    """
    return PRIMARY_PATHWAY if has_abha else FALLBACK_PATHWAY


def apply_federated_recovery(journey_log: list, pathway: str,
                              recovery_rate: float = 0.5, rng: random.Random = None) -> tuple:
    """
    Simulates the 'federated query engine' step in the architecture diagram.

    For patients on the fallback pathway (no ABHA), this models the PPRL
    fallback partially recovering continuity at stages that would otherwise
    be broken. Patients on the primary pathway are returned unchanged --
    the baseline ABHA-linked exchange is assumed to already work as designed.

    This is a conceptual placeholder for a real record-linkage outcome,
    not an implemented matching algorithm. See docs/limitations.md.

    Returns: (new_journey_log, recovered_count)
    """
    rng = rng or random.Random()
    new_log = []
    recovered = 0

    for entry in journey_log:
        if pathway == FALLBACK_PATHWAY and entry["data_status"] in BREAK_STATUSES:
            if rng.random() < recovery_rate:
                new_entry = dict(entry)
                new_entry["data_status"] = "recovered_via_pprl"
                new_entry["note"] = (
                    entry["note"] + " -- recovered via privacy-preserving "
                    "record linkage through the federated query engine"
                )
                new_log.append(new_entry)
                recovered += 1
                continue
        new_log.append(entry)

    return new_log, recovered


def run_hybrid_pathway(patient_id: str, has_abha: bool, journey_log: list,
                        recovery_rate: float = 0.5, rng: random.Random = None) -> dict:
    """
    Runs the full decision + recovery pipeline for one patient's journey
    and returns a result comparable to the baseline (ABHA-only) simulation.
    """
    pathway = decide_pathway(has_abha)
    new_log, recovered = apply_federated_recovery(journey_log, pathway, recovery_rate, rng)
    remaining_breaks = sum(1 for e in new_log if e["data_status"] in BREAK_STATUSES)

    return {
        "patient_id": patient_id,
        "abha_available": has_abha,
        "pathway": pathway,
        "journey_log": new_log,
        "continuity_breaks": remaining_breaks,
        "breaks_recovered": recovered,
    }
