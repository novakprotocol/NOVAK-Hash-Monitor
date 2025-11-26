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
