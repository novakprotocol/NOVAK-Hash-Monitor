APPENDIX C — REGULATORY MAPPING
How NOVAK Maps to U.S. Federal, Commercial, and International Standards
C.1 Overview

NOVAK does not replace laws, policies, or regulatory systems.
Instead, it enforces the semantic integrity of those laws by ensuring:

they are executed correctly

deterministically

identically

verifiably

without tampering

before action occurs

This appendix maps NOVAK’s components to the regulatory frameworks it supports.

C.2 NOVAK Laws (L0–L15) Mapped to U.S. Federal Integrity Requirements

The following table maps each NOVAK Law to existing federal standards:

NOVAK Law	Regulatory Alignment	Description
L0 — No Post-Execution Modification	FISMA, FedRAMP, NIST 800-53 (AU-9)	Prevents modifying evidence after execution.
L1 — Deterministic Rule Purity	APA, CFR	Rules must be applied identically for all individuals.
L2 — Data Attestation	HIPAA, IRS Pub 1075	Data must be proven authentic before decisionmaking.
L3 — Rule–Input Binding	CMS, VA adjudication rules	Ensures correct rule is tied to correct dataset.
L4 — Predictable Output	Administrative law, due process	Prevents arbitrary or inconsistent decisions.
L5 — HVET Requirement	NIST SP 800-57, digital signature guidelines	Provides cryptographically bound pre-execution proof.
L6 — Identity Binding	CJIS, FIPS 201 (PIV), Zero Trust identity	Ensures non-repudiation of actions.
L7 — RGAC Lineage	Federal audit standards (GAO Yellow Book)	Creates an immutable audit trail.
L8 — Monotonic Timestamps	OMB timing requirements, log integrity	Prevents backdating or timestamp fraud.
L9 — Jurisdictional Canon Enforcement	CFR, APA, statutory interpretation	Rule used must match law exactly.
L10 — Cross-Domain Coherence	CISA cyber directives	Prevents contradictory outputs in multi-system pipelines.
L11 — Public Verifiability	FOIA, open-data mandates	Enables external verification of decisions.
L12 — Trust Minimization	Zero Trust Architecture (ZTA)	Removes unnecessary trusted intermediaries.
L13 — Rule Ambiguity Prohibited	Federal Register rule precision	Rules must be clear and unambiguous.
L14 — Machine Non-Deviation	FAA/DoD safety rules, model determinism	Prevents unpredictable automated behavior.
L15 — Universal Auditability	GAO, IG investigations, oversight bodies	Ensures all actions can be independently reviewed.
C.3 NOVAK Components Mapped to Regulatory Domains
C.3.1 Healthcare (HIPAA, CMS, FDA)
Requirement	Regulation	NOVAK Mapping
Deterministic medical adjudication	CMS rules	L1–L5
Tamper-proof audit trails	HIPAA (164.312)	L0, L7
Device integrity	FDA 21 CFR 820	PL-X
Human error/fraud mitigation	CMS Program Integrity	PS-X
Non-repudiation	HIPAA 164.312(c)(2)	L6
C.3.2 Veterans Affairs (VA), DoD, Federal Benefits
Requirement	Authority	NOVAK Mapping
Benefits consistency	Title 38 USC	L1–L4
No silent claim manipulation	VA Office of Inspector General	L0, L7
Verification of claim changes	M21-1 adjudication manual	L2, L3
Prevention of automation error	VA modernization mandates	L14
Identity accountability	PIV / CAC	L6
C.3.3 Financial Regulation (FINRA, SEC, CFPB, Basel III)
Requirement	Standard	NOVAK Mapping
No post-hoc record alteration	SEC 17a-4	L0, L7
Deterministic compliance rules	CFPB UDAAP compliance	L1, L13
Fraud prevention	AML/KYC, BSA	PS-X
Transaction correctness	FINRA	L4
Identity traceability	AML requirements	L6
C.3.4 AI/ML Regulations (NIST AI RMF, EU AI Act)
Requirement	Standard	NOVAK Mapping
Predictability & determinism	NIST AI RMF	L1–L4
Tamper-evident logs	EU AI Act Article 12	L0, L7
Human oversight & integrity	EU AI Act	PS-X
Data integrity	NIST RMF	L2
Model traceability	NIST	HVET, EIR
C.3.5 Autonomous Robotics (FAA, DOT, DoD)
Requirement	Regulation	NOVAK Mapping
No unverified action	FAA Part 107	Safety Gate
Verified operational state	DoD autonomic systems policy	PL-X
No deviation from predicted path	FAA/ICAO	L14
Global traceability	DoD cyber audit	RGAC
C.4 NOVAK As a “Rule-of-Law Execution Engine”

NOVAK satisfies the Foundational Administrative Law Requirements:

consistency

transparency

predictability

fairness

accountability

non-discrimination

auditability

It enforces these requirements in mathematical form — something no agency currently achieves automatically.

C.5 NOVAK Mapping to Audit & Inspector General Frameworks
Government Accountability Office (GAO)

NOVAK supports all GAO audit pillars:

Evidence integrity → HVET

Traceability → RGAC

Non-repudiation → EIR

Consistency → Safety Gate

Preventive control → Proof-before-action

Office of Inspector General (OIG)

NOVAK detects:

improper payments

benefit manipulation

“silent denials”

timing fraud

evidence alteration

unauthorized system behavior

Before harm occurs.

C.6 NOVAK in National Security Context

NOVAK supports:

DoD auditability requirements

CMMC 2.0 Level 3 mandates

CISA Zero Trust pillars

Defense automation correctness

Nuclear command integrity principles

Autonomous platform verification

By enforcing:

identity binding

tamper-proof lineage

deterministic rule execution

non-deviation guarantees

C.7 International Regulatory Alignment

NOVAK aligns to:

Region / Standard	Mapping
GDPR	Identity + audit traceability (L6, L7)
ISO 27001	Integrity control mechanisms
ISO 21434 (Automotive security)	Determinism + anti-deviation
EU AI Act	Deterministic, transparent, predictable AI
ICAO Air Safety Standards	Path determinism & pre-authorization
C.8 Summary: NOVAK as the Enforcement Mechanism for Regulations

NOVAK is not a policy.
It is not a rule engine.
It is the enforcement mechanism below rules that guarantees:

correct

auditable

identical

lawful

non-malleable

predictable

execution of all regulated actions.

NOVAK converts law from “interpreted after the fact” into “mathematically enforced before action.”
