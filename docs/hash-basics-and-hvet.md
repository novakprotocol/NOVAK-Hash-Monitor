# NOVAK Cryptography 101 — Hashes, HVET, and Execution Receipts

This page is for engineers who understand basic computing, but may not be deep into cryptography yet.

## 1. What is a cryptographic hash? (SHA-256 in plain language)

A cryptographic hash function takes **any input** (1 byte or 1 GB) and returns a **fixed-size output** (for SHA-256, 256 bits).

Properties we rely on:

1. **Deterministic**  
   Same input → same hash every time.

2. **One-way**  
   Given the hash, it should be infeasible to recover the original input.

3. **Collision-resistant**  
   It should be infeasible to find *two different* inputs that produce the same hash.

4. **Avalanche effect**  
   A 1-bit change in input should completely change the output hash.

In practice, SHA-256 is used as a “fingerprint” of data: if the hash changes, the data changed.

---

## 2. The problem NOVAK solves

TLS, disk encryption, logging, and even blockchain mostly tell you:

> “We securely transmitted / stored / recorded *something* at time T.”

They **do not guarantee** that:

- the **inputs were correct**,  
- the **governing rules were the correct version**, and  
- the **outputs weren’t silently changed** *before* execution.

NOVAK adds this missing piece: **proof-before-action**.

---

## 3. NOVAK’s HVET: binding Rule + Data + Output + Time

NOVAK defines a **Hash-Verified Execution Trace (HVET)** as:

> A cryptographic commitment to **which rule**, **which input data**, **which output**, and **when** it all happened.

Conceptually:

```text
HR = SHA-256(rule_blob)
HD = SHA-256(input_data_blob)
HO = SHA-256(output_blob)
t  = ISO-8601 timestamp

HVET = SHA-256(HR || HD || HO || t)

Where || means concatenation.

Why this matters

If any of these change:

different rule version

different input data

different output

forged timestamp

…then HVET changes. That’s the foundation for NOVAK’s “execution integrity”.

4. EIR — Execution Identity Receipt

An Execution Identity Receipt (EIR) is NOVAK’s canonical record of a vetted decision:

eir_id – unique ID

HR – hash of governing rule set

HD – hash of input data

HO – hash of output

timestamp

HVET – binding hash

recorded_at – when it was written to the audit log

version – NOVAK-EIR-v1, etc.

Think of an EIR as a tamper-evident invoice for what the system decided.

5. RGAC — Recursive Global Audit Chain

EIRs are chained together with a simple hash link, forming RGAC:

link_i = SHA-256(HVET_{i-1} || HVET_i)


First entry uses "GENESIS" as the previous value.

Each link commits to the entire history up to that point.

If any past EIR is altered, a verifier can detect it by recomputing the chain.

6. Safety Gate, PL-X, and PS-X (very high level)

Before a decision is allowed to execute, NOVAK’s Safety Gate runs:

PL-X — Physical Layer Drift
Detects corruption / impossible values (e.g., sensor glitches, nonsensical encodings, overflows).

PS-X — Psycho-Social Manipulation
Heuristics / rules for spotting manipulative or policy-violating instructions, prompts, or rule changes.

If PL-X or PS-X flags a violation, execution is blocked and no EIR is issued.
