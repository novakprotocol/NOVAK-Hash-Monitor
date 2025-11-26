APPENDIX B — MATHEMATICAL NOTATION GUIDE
Formal Symbols, Operators, Sets, Functions & Execution Constraints for NOVAK
B.1 Core Symbols & Variables
Symbol	Meaning
R	Deterministic rule (pure function)
D	Attested input data
O	Output of rule R applied to data D
O_predicted	Expected output computed pre-execution
O_actual	Output produced during execution
T	Timestamp
I	Execution identity block (user/device/jurisdiction/purpose/environment)
HI	Hash(identity)
HVET	Hash-Verified Execution Trace
RGAC	Recursive Global Audit Chain
Σ	System state (specific moment)
Σ′	Successor state
q	State in the automaton
M	NOVAK automaton
H(x)	Cryptographic hash function
B.2 Basic Function Definitions
Deterministic Rule
R: D → O


A pure function mapping input to output with no side effects or non-deterministic behavior.

State Transition Function
F: Σ × (R, D) → Σ′


Executes transitions only after NOVAK verification.

Identity Binding Function
HI = H( user ∥ device ∥ jurisdiction ∥ purpose ∥ environment )

Predicted Output Function
O_predicted = R(D)

B.3 Hashing & Binding Operators
Hash Composition Operator (⊕)

Used to denote concatenation prior to hashing:

H(x ⊕ y ⊕ z)


Equivalent to:

H( concatenate(x, y, z) )

Vertical Concatenation ( ∥ )
x ∥ y ∥ z


Denotes byte-stream concatenation.

HVET Construction Function
HVET = H( HR ∥ HD ∥ HO ∥ HI ∥ T )


Where:

HR = H(R)

HD = H(D)

HO = H(O_predicted)

B.4 Execution Equivalence Operators
Output Consistency Condition
O_actual ≡ O_predicted


Strict equality; deviation violates NOVAK Law L14.

Hash Consistency Condition
H(O_actual) = HO

Timestamp Monotonicity
T_i > T_(i-1)


Required by NOVAK Law L8.

B.5 Sequence, Ordering & Lineage
Execution Event (E_i)
E_i = (R_i, D_i, O_i, T_i, I_i)

RGAC Chaining Function
RGAC_i = H( HVET_i ∥ RGAC_(i-1) )

Strict Total Order (≺)
E_1 ≺ E_2 ≺ E_3 ≺ … ≺ E_n


Each event is globally ordered relative to all others.

Non-Malleability Constraint
∀ element x ∈ {R, D, O, I, T}: modify(x) → HVET' ≠ HVET

B.6 Logical Sets & Domains
Execution Domain
𝔼 = { all valid execution events E_i }

Rule Domain
ℛ = { all deterministic rules }

Data Domain
𝔻 = { all attested data }

Identity Domain
𝕀 = { all valid identities }

Timestamp Domain
𝕋 = { all valid monotonic timestamps }

State Domain
𝕊 = { REQUEST, PREEXEC, VERIFIED, EXECUTED, COMMITTED, REJECTED }

B.7 Automaton & FSM Notation
NOVAK Automaton
M = (Q, Σ, δ, q0, F)


Where:

Q = set of states

Σ = input alphabet

δ = transition function

q0 = initial state

F = accepting (committed) states

Transition Function δ
δ(q, x) = q′


Produces a new state q′ given state q and input x.

Legal Transitions
REQUEST → PREEXEC → VERIFIED → EXECUTED → COMMITTED

Illegal Transitions
REQUEST → EXECUTED
PREEXEC → EXECUTED
REJECTED → EXECUTED


Violations instantly fail under L0 and L14.

B.8 Logical Predicates
Determinism Predicate
Deterministic(R) ≡ ∀D: R(D) = O

Attestation Predicate
Attested(D) ≡ HD == H(D)

Identity Predicate
ValidIdentity(I) ≡ HI == H(I)

Canon Predicate
LegalCanon(R, jurisdiction) ≡ R ≡ R_canonical

Physical Integrity Predicate (PL-X)
PhysicalStable(env) ≡ (no jitter) ∧ (no voltage drift) ∧ (no metastability)

Psycho-Social Integrity Predicate (PS-X)
HumanIntegrity(intent) ≡ honest(intent) ∧ unmanipulated(intent)

B.9 Execution-Time Constraints
Constraint 1 — Rule Purity
UsesNoGlobalState(R)
∧ NotRandom(R)
∧ NotTimeDependent(R)

Constraint 2 — Predictability
O_predicted = R(D)

Constraint 3 — No Side Effects
SideEffects(R) = ∅

Constraint 4 — Fail-Closed
if O_actual ≠ O_predicted → REJECT

B.10 NOVAK Invariants (Formal Expression)
Invariant I1 — Deterministic Execution
∀ exec: R(D) = O

Invariant I2 — Hash Integrity
∀ modifications x: HVET(x) ≠ HVET_original

Invariant I3 — Ordered Lineage
RGAC_i = H( HVET_i ∥ RGAC_(i-1) )

Invariant I4 — Non-Repudiation
identity_bound = TRUE

Invariant I5 — Proof-Before-Action
execute_only_if( safety_gate_passed = TRUE )

B.11 Numeric & Symbolic Types
Symbol	Type
T	integer or monotonic timestamp
D, R, O	byte sequences
HVET, RGAC	hash outputs (256–512 bit)
I, HI	structured identity → hash
Σ	structured system state
B.12 Extended Operators (Used in Formal Sections)
Projection Operator π_x

Extracts component x from a tuple:

π_R(E_i) = R_i

Composition Operator (∘)

Function composition:

(f ∘ g)(x) = f(g(x))

Domain Restriction (↾)

Limits a function to a narrower input domain.

Set Membership (∈)
O ∈ Outputs

B.13 Special Mathematical Objects
Execution Event Vector
𝐄 = [E_1, E_2, …, E_n]

Hash Vector
𝐇 = [HVET_1, HVET_2, …, HVET_n]

Lineage Vector
𝐑 = [RGAC_1, RGAC_2, …, RGAC_n]

APPENDIX B COMPLETE

This is now ready for GitHub upload.
