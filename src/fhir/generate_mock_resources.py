"""
generate_mock_resources.py

Generates synthetic, FHIR-shaped Patient, Encounter, and Condition resources
representing interstate migrant worker care journeys.

IMPORTANT: All data generated here is synthetic. No real patient data,
real ABHA IDs, or real facility identifiers are used anywhere in this file.
Structure loosely follows India's FHIR Implementation Guide (NRCES) for
educational/conceptual purposes only -- this is not a validated FHIR
producer and should not be used against a live FHIR server.
"""

import json
import random
import uuid
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "synthetic"

HOME_STATES = ["West Bengal", "Bihar", "Odisha", "Assam", "Uttar Pradesh"]
DESTINATION_DISTRICTS = [
    "Ernakulam", "Thiruvananthapuram", "Kozhikode", "Thrissur", "Kollam"
]
CONDITIONS = [
    ("J45", "Asthma"),
    ("E11", "Type 2 diabetes mellitus"),
    ("L01", "Skin infection"),
    ("S93", "Ankle sprain"),
    ("A09", "Gastroenteritis"),
]


def synthetic_patient(has_abha: bool) -> dict:
    """Build one synthetic FHIR-shaped Patient resource."""
    patient_id = str(uuid.uuid4())
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": (
            [{"system": "https://healthid.ndhm.gov.in", "value": f"SYNTH-ABHA-{patient_id[:8]}"}]
            if has_abha else []
        ),
        "meta": {"note": "SYNTHETIC DATA -- not a real patient"},
        "name": [{"text": f"Synthetic Worker {patient_id[:6]}"}],
        "extension": [
            {"url": "homeState", "valueString": random.choice(HOME_STATES)},
            {"url": "destinationDistrict", "valueString": random.choice(DESTINATION_DISTRICTS)},
            {"url": "abhaAvailable", "valueBoolean": has_abha},
        ],
    }


def synthetic_encounter(patient_id: str, stage: str) -> dict:
    """Build one synthetic FHIR-shaped Encounter resource for a journey stage."""
    return {
        "resourceType": "Encounter",
        "id": str(uuid.uuid4()),
        "status": "finished",
        "subject": {"reference": f"Patient/{patient_id}"},
        "class": {"code": stage},
        "meta": {"note": "SYNTHETIC DATA -- not a real encounter"},
    }


def synthetic_condition(patient_id: str) -> dict:
    """Build one synthetic FHIR-shaped Condition resource."""
    code, display = random.choice(CONDITIONS)
    return {
        "resourceType": "Condition",
        "id": str(uuid.uuid4()),
        "subject": {"reference": f"Patient/{patient_id}"},
        "code": {"coding": [{"system": "http://hl7.org/fhir/sid/icd-10", "code": code, "display": display}]},
        "meta": {"note": "SYNTHETIC DATA -- not a real diagnosis"},
    }


def generate_bundle(n_patients: int = 10, abha_rate: float = 0.5) -> list:
    """Generate n synthetic patient bundles. abha_rate controls what fraction have ABHA."""
    bundles = []
    for _ in range(n_patients):
        has_abha = random.random() < abha_rate
        patient = synthetic_patient(has_abha)
        encounter = synthetic_encounter(patient["id"], stage="ambulatory")
        condition = synthetic_condition(patient["id"])
        bundles.append({"patient": patient, "encounter": encounter, "condition": condition})
    return bundles


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    bundles = generate_bundle(n_patients=10, abha_rate=0.5)
    out_path = OUTPUT_DIR / "synthetic_patient_bundles.json"
    with open(out_path, "w") as f:
        json.dump(bundles, f, indent=2)
    print(f"Generated {len(bundles)} synthetic patient bundles -> {out_path}")


if __name__ == "__main__":
    main()
