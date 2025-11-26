APPENDIX A — NOVAK GLOSSARY
Complete Terminology, Cryptographic Constructs, Components, and Legal Definitions

This glossary defines every term used throughout the NOVAK Protocol.
It covers all technical, cryptographic, regulatory, physical, and socio-technical components, including both:

Current NOVAK terminology

Historical terminology (old → new mappings)

A.1 Core NOVAK Components
NOVAK Protocol

Novak Objective Verification of Autonomous Knowledge.
A deterministic, proof-before-action execution integrity system governing any rule-based decision, action, or computation.

Safety Gate (formerly “HARMONEE”)

The deterministic safety layer enforcing all NOVAK Laws (L0–L15).
It prohibits execution unless all proofs and attestations validate successfully.

EIR — Execution Identity Receipt (formerly “NIPS”)

A pre-execution cryptographic artifact binding:

rule

input

predicted output

identity

timestamp

jurisdiction

execution intent

Serves as tamper-proof evidence that the system proved correctness before acting.

RGAC — Recursive Global Audit Chain (formerly “REVELATION”)

A forward-chaining, global, monotonic audit ledger where each new HVET binds to the previous, forming a provable timeline of execution events.

Not blockchain.
Not consensus-driven.
Not distributed by mining.

A deterministic audit lineage.

HVET — Hash-Verified Execution Trace

A cryptographic hash binding:

HR || HD || HO || HI || timestamp


Where:

HR = hash(rule)

HD = hash(data)

HO = hash(predicted output)

HI = hash(identity+environment)

A.2 NOVAK Laws (L0–L15)

Mandatory invariants governing all NOVAK-compliant systems:

L0: No post-execution modification

L1: Deterministic rule purity

L2: Data attestation

L3: Rule–input binding

L4: Predictability of outputs

L5: HVET emission requirement

L6: Identity binding

L7: RGAC lineage binding

L8: Monotonic timestamps

L9: Jurisdictional canonical legality

L10: Cross-domain coherence

L11: Public verifiability

L12: Trust minimization

L13: No rule ambiguity

L14: Machine anti-deviation

L15: Global auditability guarantee

A.3 Industry Addenda
PL-X — Physical Layer Addendum

Ensures computational correctness under physical conditions:

metastability

voltage or frequency drift

bit-rot

cosmic interference

clock instability

timing jitter

thermal variance

hardware glitch injection

PS-X — Psycho-Social Layer Addendum

Ensures correctness under human deception or confusion:

fraud attempts

malicious intent

cognitive bias

social engineering

misunderstanding

adversarial manipulation

intention distortion

contextual ambiguity

A.4 Identity Components
Execution Identity (EI)

Immutable representation of:

user identity

device identity

jurisdiction

purpose

environment

authorization

role

HI — Hashed Identity

Hash of the identity block:

HI = H(user || device || jurisdiction || purpose || environment)

Authority Canon

The governing set of jurisdictional rules that a system must match under L9.

A.5 Hashing & Cryptographic Constructs
Hash Function

One-way, collision-resistant mapping H(x).

NOVAK relies on:

SHA-256

SHA-384

SHA-512

SHA-3

Deterministic Output (O)

The output produced by a pure rule given attested data.

Attested Data (D_attested)

Data whose cryptographic form (HD) has been verified as unmodified.

Predicted Output (O_predicted)

The output NOVAK computes before the action occurs.
Must match the actual output exactly.

Actual Output (O_actual)

The output produced at execution time.
If it diverges from O_predicted → system fails closed (L14).

A.6 System & Execution States
REQUEST State

Action requested but not verified.

PRE-EXECUTION State

Safety Gate evaluating all proofs.
Most actions fail here.

VERIFIED State

All NOVAK Laws validated.
Execution allowed.

EXECUTED State

Machine performs computation with rule and data.

COMMITTED State

RGAC updated and EIR finalized.

REJECTED State

Failure of any NOVAK Law or Addendum.

A.7 Physical, Logical & Social Layers
Physical Layer (PL-X)

Environmental integrity constraints: timing, stability, hardware.

Logical Layer

Deterministic rules, legality, canonical regulatory correctness.

Data Layer

Attestation, hashing, pre-execution trace.

Social Layer (PS-X)

Fraud resistance, intent verification, bias mitigation.

A.8 Regulatory Constructs
Canonical Legal Rule

The verified source-of-truth legal or policy definition a jurisdiction enforces.

Deterministic Legality Check

A computation verifying that the rule applied is the expected canonical version.

Malleability

Any capacity for rule, data, or output to shift unpredictably.
NOVAK prohibits malleability entirely.

Non-Repudiation

The property that identity cannot be detached from an action.

A.9 Machine Behavior Terms
Machine Deviation

When O_actual does not match O_predicted.
Under NOVAK → this is an illegal action.

Fail-Closed Execution

If deviation detected, system shuts down or rejects operation.

Deterministic Purity

Rule cannot touch or depend on external state.
No randomness.
No uncontrolled branches.

A.10 Audit & Verification
Public Verifiability

Any third party can recompute HVET and RGAC to confirm truth.

Irreversible Lineage

RGAC entries cannot be removed, replaced, or altered.

Attestation Layer

The combination of Safety Gate + HVET + PL-X ensuring input correctness.

A.11 Domain Usage Terms
AI Determinism

AI outputs must be predictable under a bounded decision rule before authorization.

Robotic Execution Integrity

Robot actions must provably match their predicted trajectories.

Regulatory Determinism

Legal rules must be executed identically for every citizen.

Financial Execution Integrity

All financial adjustments must be provably correct before commit.

A.12 Whitepaper Classification
Authoritative Source System

NOVAK becomes the authoritative executor of rule-governed calculations.

Proof-Before-Action (PBA)

The core philosophy: no action without cryptographic proof.
