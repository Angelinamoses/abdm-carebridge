# Limitations

This document states, deliberately and in one place, what this project does and does not prove. It is written to be more honest about scope than any single claim elsewhere in the repository or the proposal — that is intentional.

## 1. Data limitations

- **All patient data in this repository is synthetic.** No real ABHA IDs, real facility identifiers, or real health records are used anywhere. Nothing here reflects the actual health status, identity, or circumstances of any real migrant worker.
- **The synthetic generator is a simplification.** `src/fhir/generate_mock_resources.py` produces plausible-looking records (random home state, random condition, boolean ABHA availability) — it does not model real epidemiological patterns, real disease prevalence among migrant workers, or realistic distributions of ABHA adoption. The 50% ABHA-availability split used in early testing is an arbitrary illustrative parameter, not an estimate grounded in administrative data.
- **No real ABDM dashboard data has been integrated yet.** The proposal references the NHA ABDM Public Dashboard as a planned administrative data source; as of this prototype, none of its indicators have been pulled into the codebase.

## 2. Simulation limitations

- **The 9-stage journey simulator uses simplified, partly randomized rules** (e.g. a 30% chance of a stage being "isolated" when ABHA is unavailable) to assign continuity status at each stage. These probabilities are illustrative placeholders, not derived from empirical observation of how migrant worker health data actually moves — or fails to move — through Kerala's health system.
- **The "continuity breaks" metric is a simple count**, not a validated or clinically weighted score. A break at the "referral" stage is treated as equivalent in severity to a break at "discharge and return," which is very unlikely to be true in practice.
- **The comparison between ABHA-available and ABHA-unavailable scenarios (3.0 vs. 7.2 average breaks in early runs) is a demonstration of mechanism, not a finding.** It shows that the simulation logic behaves as designed — it does not show that real ABHA adoption produces this magnitude of difference in the real world.

## 3. Architecture and technical limitations

- **The privacy-preserving record linkage (PPRL) fallback pathway is currently a conceptual design, not an implemented algorithm.** No probabilistic matching, encryption scheme, or fuzzy-matching logic has been built yet. The architecture diagram represents an intended design inspired by the RECONNECT project (Ngo et al., 2024), not a working system.
- **The FHIR resources generated here are FHIR-shaped, not FHIR-validated.** They follow the general structure of Patient/Encounter/Condition resources for illustrative purposes but have not been validated against the NRCES India FHIR Implementation Guide's official profiles or a FHIR validator.
- **No integration with any live ABDM sandbox, API, or government system exists or is planned within this prototype's current scope.** Building that integration would require formal approval and credentialing processes well beyond a two-month internship.
- **The "federated query engine" in the architecture diagram is conceptual.** No federated query infrastructure has been implemented; the diagram illustrates an intended design pattern, not existing software.

## 4. Methodological limitations

- **This is a design-oriented systems analysis, not an empirical adoption study.** It does not survey, interview, or collect data from real migrant workers, healthcare providers, or ABDM administrators. Claims about barriers and gaps are synthesized from literature and policy documents, not from primary fieldwork.
- **The literature base, while deliberately chosen to triangulate the gap this project addresses, is not a systematic or exhaustive review.** Nine sources were used purposefully to build a specific argument; a comprehensive literature review of ABDM, migrant health, or digital health equity would draw on substantially more sources.
- **Kerala-specific claims about institutional readiness (drawing on Ummer et al., 2021) describe COVID-era, emergency-response capacity.** Whether that same capacity translates to routine, non-emergency digital health infrastructure is an assumption this project makes explicit but does not test.

## 5. Scope limitations

- **The two-month internship timeframe scopes this work to a demonstrator, not a deployable system.** Nothing in this repository should be interpreted as production-ready, security-audited, or suitable for use with real patient data.
- **Equity claims are theoretical, not measured.** The project applies Bangla, Kapoor & Jeer's (2026) digital health equity framework analytically; it does not measure real-world exclusion outcomes for Kerala's migrant workforce.

## Why this document exists

A reviewer who reads only the README or the proposal PDF could reasonably come away thinking the numbers here are stronger evidence than they are. This document is meant to correct that before anyone has to ask. Future updates to this repository (evaluation scenarios, real administrative data integration, an implemented PPRL module) should update this document alongside them — a limitations section that goes stale is worse than none at all.
