# Evaluation

Compares two scenarios over the same synthetic patient journeys:

- **Baseline** — current ABDM design assumption. No ABHA means no fallback; continuity breaks stay broken.
- **Hybrid** — the proposed architecture (`src/continuity/pathway.py`). No ABHA triggers a privacy-preserving record linkage fallback, which recovers some fraction of otherwise-broken stages through the federated query engine.

## Run it

```bash
python src/fhir/generate_mock_resources.py
python src/simulation/journey_simulator.py
python evaluation/run_scenarios.py
```

Output is written to `evaluation/results/scenario_comparison.json` and printed to the console.

## What this does and doesn't show

This quantifies the *mechanism* of the proposed architecture on synthetic data — it shows that, if a fallback pathway recovers some share of continuity breaks, overall continuity improves. It does not measure a real-world effect size, and the 0.5 recovery rate is an illustrative placeholder, not an empirical estimate. See [`../docs/limitations.md`](../docs/limitations.md).
