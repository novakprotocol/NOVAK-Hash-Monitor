# NOVAK Standards & Whitepapers

This page collects the **formal, citable artifacts** that define the NOVAK Protocol.

All documents are covered by the NOVAK Public Safety License (NPSL) and the
NOVAK Commercial License as described in `/legal/`.

---

## 1. Core Standards (SP Series)

- **SP-1 — NOVAK Execution Integrity Standard**  
  Defines the proof-before-action model, execution identity, and baseline requirements
  for deterministic decision pipelines.

- **SP-2 — HVET / EIR / RGAC Cryptographic Standard**  
  Formal specification of HVET, Execution Identity Receipts, and the Recursive Global Audit Chain.

- **SP-3 — Safety Gate + PL-X / PS-X Standard**  
  How NOVAK models physical drift, human drift, and automation adversaries.

- **SP-4 — NOVAK Implementation Requirements**  
  Minimal requirements for any implementation claiming NOVAK conformance.

- **SP-5 — NOVAK Certification Standard**  
  Levels of assurance and certification tiers for systems using NOVAK.

- **SP-6 — NOVAK Conformance Testing Suite**  
  Test harness definitions and required conformance scenarios.

- **SP-7 — NOVAK Federal Adoption & Compliance Guide**  
  Guidance for U.S. Federal agencies, VA, DoD, and regulated industries.

- **SP-8 — NOVAK Unified Technical & Governance Model**  
  Bridges the cryptographic core with governance, oversight, and regulatory use.

> All SP documents are available under `/standards/` and `/docs/whitepapers/`.

---

## 2. Threat Models (NTM Series)

- **NTM-1 — NOVAK Threat Model (High-Level)**  
  Baseline adversary models across network, internal, human, and automation actors.

- **NTM-2 — NOVAK Threat Model (Cryptographic & Systemic)**  
  Deep cryptographic and architecture-level threats.

- **NTM-3 — NOVAK Adversarial AI Test Suite**  
  Full adversarial prompt libraries, gradient-space attack vectors, multilingual ambiguity matrices.

> Available under `/docs/threat-models/` and `/docs/appendices/`.

---

## 3. Test Suites & Appendices

- **Appendix A — NOVAK Adversarial Prompt Library**  
  800+ adversarial prompts organized by drift type, domain, and language.

- **Appendix B — Gradient-Space Adversarial Simulation Vectors**  
  Vector-style attack definitions for model-space testing.

- **A13-S1 — Multilingual Ambiguity Matrix**  
  Stress-tests cross-lingual ambiguity and regulatory interpretation drift.

---

## 4. Cryptographic Challenge

The **NOVAK Cryptographic Challenge** is published as a separate PDF and ResearchGate
edition. It invites cryptographers, AI safety researchers, and auditors to:

- Break the assumptions  
- Attack the drift models  
- Show failure cases  

…and receive formal acknowledgment for any confirmed issues.

---

## 5. Source Repository

The canonical, evolving source for all NOVAK materials is:

- **GitHub:** `https://github.com/novakprotocol/NOVAK-Hash-Monitor`

The GitHub repo is the **living source of truth**; the PDFs and whitepapers are the
citable, frozen snapshots for legal and academic use.
