NOVAK PbA Monitor
Reference Implementation of the NOVAK Proof-Before-Action Primitive, HVET, and EIR Integrity System

Created by Matthew Novak

🔒 Overview

NOVAK PbA Monitor is the world’s first implementation of the Proof-Before-Action (PbA) cryptographic primitive — a new class of integrity mechanism that requires proof first, before any system or software is allowed to act.

Where traditional systems log or detect tampering after the fact, NOVAK enforces correctness before execution, using:

HVET — Hash-Verified Execution Trace

EIR — Execution Identity Receipt

RGAC — Recursive Global Audit Chain

Merkle Anchors

OS-Level Integrity Hooks

This repository contains the reference monitor, implemented in Python and installable as the CLI tool:

novak-pba

🚀 Features
✔ 1. Proof-Before-Action (PbA) Enforcement

A cryptographic gate that prevents execution unless the mathematical proof is valid.

✔ 2. HVET Construction

Rules, Data, Outputs, and Timestamps are bound into a single hash commitment:

HVET = H( H(R) || H(D) || H(O) || H(time) )

✔ 3. EIR Receipts (Self-Authenticating Proof Objects)

Every state change generates an Execution Identity Receipt with:

Hash of Rule

Hash of Data

Hash of Output

Timestamp

HVET (the binding proof)

✔ 4. Tamper-Evident EIR Chain (RGAC)

Every EIR is appended to a cryptographically chained ledger.
If anything changes → the chain breaks.

✔ 5. OS-Level File Integrity Monitoring

Built on watchdog for cross-platform support:

Linux (inotify)

macOS (FSEvents)

Windows (ReadDirectoryChangesW)

✔ 6. Baseline Scanning + Re-Verification

Generate a SHA-256 baseline of a filesystem and detect later modifications.

✔ 7. Merkle Anchoring

Optional Merkle root generation for anchoring daily states externally.

🧩 Install
pip install .


Or from PyPI (when you release it):

pip install novak_pba_monitor

🖥 CLI Usage
Create a baseline
novak-pba baseline /etc -o baseline.json

Real-time monitoring with HVET + EIR
novak-pba watch /etc --rule <rulehash>

Verify a filesystem against its baseline
novak-pba verify /etc --baseline baseline.json

Gate an action behind NOVAK PbA
novak-pba gate --rule X --data Y --output Z


If the math is valid → the action executes.
If not → blocked.

📘 Cryptographic Foundations

NOVAK is built on three core components:

1. PbA (Proof-Before-Action)

A new cryptographic primitive enforcing:

“No execution without proof.”

2. HVET (Hash-Verified Execution Trace)

A canonicalized hash binding Rules + Data + Output + Time.

3. EIR (Execution Identity Receipt)

A self-authenticating proof object documenting each execution event.

4. RGAC (Recursive Global Audit Chain)

A hash chain of EIRs providing global tamper detection.

🔬 Security Properties

Rule Binding

Data Binding

Output Binding

Replay Resistance

Temporal Singularity

Deterministic Execution Integrity

Pre-Execution Correctness

End-to-End Trace Integrity

Formal reduction proofs included in the NOVAK whitepaper.
