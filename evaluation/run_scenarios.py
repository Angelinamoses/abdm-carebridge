"""
run_scenarios.py — compares two scenarios using the same synthetic patient
journeys:

  Scenario A (baseline): current ABDM design. If ABHA is unavailable,
    continuity breaks stay broken -- there is no fallback.

  Scenario B (hybrid): the proposed architecture. If ABHA is unavailable,
    the privacy-preserving record linkage fallback (src/continuity/pathway.py)
    runs, recovering some fraction of otherwise-broken stages.

This produces the comparison referenced in docs/proposal.pdf, Section 8.
All data is synthetic. See docs/limitations.md for what this does and does
not demonstrate.
"""

import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.continuity.pathway import run_hybrid_pathway, BREAK_STATUSES 

DATA_DIR = ROOT / "data" / "synthetic"
RESULTS_DIR = Path(__file__).resolve().parent / "results"


def load_baseline_results() -> list:
    """
    Loads Scenario A: the baseline journey simulation output
    (src/simulation/journey_simulator.py), representing the current
    ABHA-only design with no fallback pathway.
    """
    path = DATA_DIR / "journey_simulation_results.json"
    if not path.exists():
        raise FileNotFoundError(
            "No baseline simulation found. Run, in order:\n"
            "  python src/fhir/generate_mock_resources.py\n"
            "  python src/simulation/journey_simulator.py\n"
            "before running this evaluation."
        )
    with open(path) as f:
        return json.load(f)


def run_hybrid_scenario(baseline_results: list, recovery_rate: float = 0.5,
                         seed: int = 42) -> list:
    """
    Runs Scenario B: applies the hybrid continuity pathway on top of the
    same synthetic journeys used in the baseline.
    """
    rng = random.Random(seed)
    hybrid_results = []
    for r in baseline_results:
        result = run_hybrid_pathway(
            patient_id=r["patient_id"],
            has_abha=r["abha_available"],
            journey_log=r["journey_log"],
            recovery_rate=recovery_rate,
            rng=rng,
        )
        hybrid_results.append(result)
    return hybrid_results


def summarize(results: list, label: str) -> dict:
    with_abha = [r for r in results if r["abha_available"]]
    without_abha = [r for r in results if not r["abha_available"]]

    def avg_breaks(group):
        return round(sum(r["continuity_breaks"] for r in group) / len(group), 2) if group else None

    return {
        "scenario": label,
        "n_patients": len(results),
        "n_with_abha": len(with_abha),
        "n_without_abha": len(without_abha),
        "avg_breaks_with_abha": avg_breaks(with_abha),
        "avg_breaks_without_abha": avg_breaks(without_abha),
        "avg_breaks_overall": avg_breaks(results),
    }


def main():
    RESULTS_DIR.mkdir(exist_ok=True)

    baseline = load_baseline_results()
    hybrid = run_hybrid_scenario(baseline, recovery_rate=0.5, seed=42)

    baseline_summary = summarize(baseline, "baseline_abha_only")
    hybrid_summary = summarize(hybrid, "hybrid_with_pprl_fallback")

    total_recovered = sum(r["breaks_recovered"] for r in hybrid)

    comparison = {
        "baseline": baseline_summary,
        "hybrid": hybrid_summary,
        "total_breaks_recovered_by_fallback": total_recovered,
        "note": (
            "Synthetic data, illustrative recovery_rate=0.5. This demonstrates "
            "the mechanism of the proposed architecture, not a validated "
            "empirical effect size. See docs/limitations.md."
        ),
    }

    out_path = RESULTS_DIR / "scenario_comparison.json"
    with open(out_path, "w") as f:
        json.dump(comparison, f, indent=2)

    print("Scenario A (baseline, ABHA-only, no fallback):")
    print(f"  avg breaks with ABHA:    {baseline_summary['avg_breaks_with_abha']}")
    print(f"  avg breaks without ABHA: {baseline_summary['avg_breaks_without_abha']}")
    print()
    print("Scenario B (hybrid, with PPRL fallback):")
    print(f"  avg breaks with ABHA:    {hybrid_summary['avg_breaks_with_abha']}")
    print(f"  avg breaks without ABHA: {hybrid_summary['avg_breaks_without_abha']}")
    print()
    print(f"Total continuity breaks recovered by the fallback pathway: {total_recovered}")
    print(f"\nFull comparison written to {out_path}")


if __name__ == "__main__":
    main()
