# NOVAK PROTOCOL — PART 5  
## SYSTEM MODEL & EXECUTION FLOW

---

# 1. System Overview

NOVAK is a pipeline of:

- deterministic rule enforcement  
- input attestation  
- identity binding  
- physical/socio integrity checks  
- pre-execution hashing  
- global audit chain insertion  
- deterministic execution  

---

# 2. Execution Flow

### Step 1 — Request Initiation  
A user, system, AI model, or robot requests an action.

### Step 2 — Rule Attestation (HR)  
Rule must match canonical form.

### Step 3 — Data Attestation (HD)  
Data must be schema-locked and hashed.

### Step 4 — Identity Binding (HI)  
EIR is initiated with:

- user identity  
- device identity  
- jurisdiction  
- intent  

### Step 5 — Safety Gate Validation  
Execution blocked unless:

- L1–L15 pass  
- PL-X stable  
- PS-X validated  
- output prediction correct  

### Step 6 — EIR Construction

### Step 7 — HVET Construction

### Step 8 — RGAC Insertion

### Step 9 — Execution

### Step 10 — Post-State Verification

---

# 3. NOVAK Enforcement

If any condition fails, execution returns:

NOVAK_DENY

makefile
Copy code

otherwise:

NOVAK_ALLOW

Copy code
