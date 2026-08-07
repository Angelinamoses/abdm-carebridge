"""
journey_simulator.py

Simulates a synthetic interstate migrant worker's care journey across
9 stages, logging what data is generated, lost, duplicated, or
inaccessible at each stage under two scenarios:

  1. ABHA-only pathway (current ABDM design assumption)
  2. Hybrid pathway (ABHA + privacy-preserving record linkage fallback)

This is a conceptual demonstrator, not a validated simulation model.
All data is synthetic.
"""

import json
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "synthetic"

JOURNEY_STAGES = [
    "home_state_baseline",
    "migration",
    "destination_registration",
    "abha_usage",
    "clinical_consultation",
    "laboratory",
    "pharmacy",
    "referral",
    "discharge_and_return",
]


def simulate_stage(stage: str, has_abha: bool) -> dict:
    """
    Simulate what happens to patient data at a single journey stage.
    Returns a dict describing data continuity status at this stage.
    """
    if stage == "home_state_baseline":
        return {"stage": stage, "data_status": "generated", "note": "baseline record created in home state, if any"}

    if stage == "migration":
        return {"stage": stage, "data_status": "at_risk", "note": "no automatic record transfer across state lines"}

    if stage == "destination_registration":
        if has_abha:
            return {"stage": stage, "data_status": "linked", "note": "registration linked via ABHA"}
        return {"stage": stage, "data_status": "duplicated", "note": "new local record created, not linked to prior history"}

    if stage == "abha_usage":
        if has_abha:
            return {"stage": stage, "data_status": "available", "note": "ABHA successfully used for record pull"}
        return {"stage": stage, "data_status": "lost", "note": "no ABHA -- continuity depends entirely on fallback pathway"}

    if stage in ("clinical_consultation", "laboratory", "pharmacy"):
        if has_abha or random.random() < 0.3:
            return {"stage": stage, "data_status": "recorded", "note": "data captured, linkage depends on earlier stages"}
        return {"stage": stage, "data_status": "isolated", "note": "recorded locally, not connected to longitudinal record"}

    if stage == "referral":
        return {"stage": stage, "data_status": "at_risk", "note": "referral summary transfer not guaranteed cross-facility"}

    if stage == "discharge_and_return":
        return {"stage": stage, "data_status": "at_risk", "note": "no guaranteed mechanism to sync destination-state record back to home state"}

    return {"stage": stage, "data_status": "unknown", "note": ""}


def simulate_journey(patient_id: str, has_abha: bool) -> dict:
    """Run the full 9-stage journey for one synthetic patient."""
    log = [simulate_stage(stage, has_abha) for stage in JOURNEY_STAGES]
    breaks = [entry for entry in log if entry["data_status"] in ("lost", "at_risk", "isolated", "duplicated")]
    return {
        "patient_id": patient_id,
        "abha_available": has_abha,
        "journey_log": log,
        "continuity_breaks": len(breaks),
    }


def main():
    bundle_path = DATA_DIR / "synthetic_patient_bundles.json"
    if not bundle_path.exists():
        print("No synthetic bundles found. Run src/fhir/generate_mock_resources.py first.")
        return

    with open(bundle_path) as f:
        bundles = json.load(f)

    results = []
    for bundle in bundles:
        patient = bundle["patient"]
        has_abha = any(patient.get("identifier", []))
        result = simulate_journey(patient["id"], has_abha)
        results.append(result)

    out_path = DATA_DIR / "journey_simulation_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    avg_breaks_with_abha = sum(r["continuity_breaks"] for r in results if r["abha_available"]) / max(
        1, sum(1 for r in results if r["abha_available"])
    )
    avg_breaks_without_abha = sum(r["continuity_breaks"] for r in results if not r["abha_available"]) / max(
        1, sum(1 for r in results if not r["abha_available"])
    )

    print(f"Simulated {len(results)} patient journeys -> {out_path}")
    print(f"Average continuity breaks (ABHA available):    {avg_breaks_with_abha:.2f}")
    print(f"Average continuity breaks (ABHA unavailable):   {avg_breaks_without_abha:.2f}")


if __name__ == "__main__":
    main()
