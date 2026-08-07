# Architecture

## 1. Reference model: WHO-ITU Digital Health Platform Handbook

This project uses the WHO Digital Health Platform Handbook as its reference architecture, and positions ABDM as a real-world implementation of it. The handbook describes national digital health infrastructure as layered, not monolithic:

```
Health Applications
Information & Mediation Services
Shared Health Services
Registries
Standards & Interoperability
Infrastructure
```

ABDM maps onto this cleanly:

| Layer | ABDM equivalent |
|---|---|
| Infrastructure | Cloud infrastructure, national data centers |
| Standards | HL7 FHIR, SNOMED CT, ICD, LOINC |
| Registries | ABHA (patient identity), Health Facility Registry, Healthcare Professional Registry |
| Shared services | Consent Manager, authentication, audit logging |
| Information & mediation | Health Information Exchange (HIE), Unified Health Interface (UHI) |
| Applications | Hospital EMRs, telemedicine apps, personal health records |

ABDM is well-aligned with WHO recommendations: federated architecture, open APIs, HL7 FHIR, digital registries, and consent-based data sharing. The literature (Mantri et al., 2024; Raj, Dananjayan & Agarwal, 2023) documents this alignment clearly.

## 2. Where the design assumption breaks

ABDM's registries and consent flows are built around ABHA as the primary patient identifier. This works when a patient has stable registration, consistent digital access, and continuity of engagement with the health system.

Interstate informal migrant workers frequently do not meet these conditions:

- Inconsistent or absent ABHA registration
- Variable digital literacy and smartphone access
- No fixed address for identity verification
- Interruption of care across state administrative boundaries
- Language barriers at point of registration

Bangla, Kapoor & Jeer (2026) frame this as a structural pattern: digital health systems designed without deliberately accounting for vulnerable populations tend to reproduce or amplify existing inequities rather than resolve them — what they term "digital-by-default" marginalization.

## 3. The hybrid continuity pathway

Rather than proposing a replacement for ABHA, this project designs a **fallback-aware architecture**:

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

**Primary pathway (ABHA available):** standard ABDM-compliant FHIR-based exchange through the Health Information Exchange, as currently designed.

**Fallback pathway (ABHA unavailable or unreliable):** privacy-preserving record linkage using encrypted demographic matching (name, date of birth, phone number) — inspired by the RECONNECT project's approach (Ngo et al., 2024) to linking records across Ireland's independent health systems without a centralized database or exposed identifiers.

**Common layer:** both pathways feed into a consent-governed federated query engine. Data stays where it already lives (hospital, PHC, labour camp clinic); only queries travel. This preserves ABDM's core federated-architecture principle rather than proposing a competing centralized system.

## 4. The patient journey being modeled

The simulation (`src/simulation/journey_simulator.py`) traces a synthetic migrant worker through nine stages, logging what data is generated, lost, duplicated, or inaccessible at each step:

1. Home state (baseline health record, if any)
2. Migration (loss of continuity begins)
3. Hospital/PHC registration in destination state
4. ABHA usage attempt
5. Clinical consultation
6. Laboratory
7. Pharmacy
8. Referral (if needed)
9. Discharge and return to home state

This journey map is the empirical backbone connecting the architecture above to a concrete, demonstrable failure mode.

## References

- Mantri et al. (2024). Frontiers in Digital Health.
- Bangla, S., Kapoor, A., & Jeer, G. (2026). *International Journal of Equity in Health.*
- Ngo et al. (2024). RECONNECT project. arXiv:2410.13880.
- Raj GM, Dananjayan S, Agarwal N (2023). *Health Care Science.*
- Ummer O, Scott K, Mohan D, et al. (2021). *BMJ Global Health.*
