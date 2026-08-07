# ABDM CareBridge

**Assessing ABDM's Design-Reality Gap for Kerala's Interstate Informal Migrant Workforce: A Systems Analysis of Continuity-of-Care Barriers**

> ⚠️ **Status: early-stage prototype.** This repository accompanies a research proposal submitted to the Kerala State Planning Board's Student Internship Programme 2026–27. It uses **synthetic data only** and is not connected to any live ABDM sandbox, government system, or real patient records. Full implementation and evaluation are planned across the internship period.

## The problem

India's Ayushman Bharat Digital Mission (ABDM) was designed to solve fragmented, siloed health records through a federated architecture built on ABHA IDs, FHIR-based interoperability, and consent-driven health information exchange. Most research on ABDM assumes the user has a stable address, consistent digital access, and continuous engagement with one region's health system.

Kerala's ~3.5 million interstate informal migrant workers rarely meet those assumptions. They cross state lines, change employers, and often have inconsistent registration — conditions under which most published ABDM research has not been tested.

This project asks: **when ABHA-based continuity fails, what would a resilient fallback actually look like?**

## The architecture

```
Migrant worker seeks care
          │
   ABHA available?
      /        \
    No          Yes
     │            │
Privacy-preserving   FHIR-based HIE
record linkage        exchange
     │            │
      \          /
   Federated query engine
   (consent-governed, no central store)
          │
   Continuity of care
```

Full explanation in [`docs/architecture.md`](docs/architecture.md). This design is inspired by the RECONNECT project's (Ngo et al., 2024) federated, privacy-preserving record linkage approach applied to Ireland's fragmented health systems — adapted here for a highly mobile population that ABDM's ABHA-first design does not fully account for.

## What's in this repo right now

| Path | Status |
|---|---|
| `src/fhir/` | Generates synthetic FHIR-compliant Patient/Encounter resources representing a migrant worker's care journey |
| `src/simulation/` | Simulates the 9-stage patient journey (home state → migration → registration → ABHA → consultation → lab → pharmacy → referral → discharge → return) and logs where continuity breaks |
| `data/synthetic/` | Generated synthetic patient records — no real data, ever |
| `docs/architecture.md` | Full write-up of the WHO Digital Health Platform layers, ABDM building blocks, and the hybrid continuity pathway |

## Planned during the internship

- `src/linkage/` — probabilistic record matching (fuzzy name/DOB/phone matching) for the no-ABHA fallback pathway
- `src/metrics/` and `evaluation/` — quantify continuity preserved under baseline (ABHA-only) vs. hybrid pathway scenarios
- `dashboard/` — interactive visualization of data loss across the patient journey
- `tests/` and CI — unit tests for the simulation and linkage modules
- `docs/limitations.md` — a deliberately honest accounting of what this prototype does and doesn't prove

## Why this approach

Most ABDM research either audits adoption (do people create ABHA IDs?) or reviews policy (what does ABDM claim to do?). This project instead asks a **systems-design question**: does the architecture hold up for a population it wasn't explicitly designed around, and if not, what's a concrete, implementable fallback?

Grounded in:
- WHO-ITU Digital Health Platform Handbook (reference architecture)
- Bangla, Kapoor & Jeer (2026) — digital health equity framework
- Ngo et al. (2024) — RECONNECT federated linkage architecture
- Ummer et al. (2021) — Kerala's demonstrated institutional capacity for coordinated digital health deployment

## Running it

```bash
pip install -r requirements.txt
python src/fhir/generate_mock_resources.py
python src/simulation/journey_simulator.py
```

## Citation

See [`CITATION.cff`](CITATION.cff).

## License

MIT — see [`LICENSE`](LICENSE).
