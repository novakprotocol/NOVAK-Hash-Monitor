# Product Reconnaissance — Password Threat Lab

## Decision

```text
schema_version: n.product.recon.v1
route_decision: extend-existing
owning_repository: novakprotocol/NOVAK-Hash-Monitor
scoped_path: password-threat-lab/
status: approved-for-scoped-draft-implementation
```

## Trigger

The owner supplied an educational brief about classical password cracking, Grover's algorithm, Shor's algorithm, and post-quantum cryptography, then requested a public password-time estimator. A prior Python-only implementation and a separate Gemini HTML prototype were available as inputs.

## Source summary

The supplied HTML prototype presents four explanatory panels and a browser calculator that estimates a complete character space, divides it by a fixed classical rate, and applies a square-root operation for an illustrative quantum result. It uses Tailwind's browser CDN, Google Fonts, a visible text input, and an assumed quantum operations-per-second value.

The prior Python implementation adds bounded pattern recognition and multiple classical attack profiles, but its server-side form model is not directly deployable on GitHub Pages.

## User problem

Provide a public, understandable tool that:

- demonstrates why predictable passwords fail before a full brute-force search;
- distinguishes online and offline classical scenarios;
- explains Grover without presenting an unsupported quantum clock;
- explains why Shor and PQC concern public-key migration; and
- does not collect or transmit the representative sample.

## Market and repository reconnaissance

Password strength meters and crack-time estimators are common. Several repositories use names such as `password-crack-time-estimator`, and established pattern estimators already exist. The exact number of similar projects was not established, so this record does not claim “thousands.”

The useful differentiation is not the existence of another timer. It is the combination of:

- local-only operation with no third-party runtime code;
- explicit attack-profile assumptions;
- pattern-aware versus random-space comparison;
- Grover query complexity without a wall-clock claim;
- Shor/PQC separation; and
- N-stack evidence, handoff, and claim boundaries.

## N-stack overlap and route

| Repository | Overlap | Decision |
|---|---|---|
| `NOVAK-Hash-Monitor` | Existing public GitHub Pages cryptography/integrity education surface | Extend as an isolated subpath |
| `N-SHA-Lab` | Private SHA analysis and visualization laboratory | Do not expose or couple private laboratory assets |
| `N-Idea` | Product reconnaissance and routing | Owns this recon record |
| `N-RepoOps` | Repository floor, evidence, hard gates, and claim boundaries | Apply scoped floor here |
| `N-Suite` | Portfolio accounting | No new repository entry; this is an existing-repo surface |
| `N-App-SDK` | App and surface metadata | Apply scoped manifest contracts |

Creating a duplicate public repository would fragment the existing cryptography education surface. The route is therefore `extend-existing`.

## Material not reused

The implementation does not reuse:

- Gemini branding or source-specific prose;
- Tailwind CDN code or external font calls;
- an assumed fixed quantum operations-per-second timer;
- unsupported current-GPU benchmark claims;
- third-party visual assets; or
- any real user credential.

The general educational concepts and standard mathematical relationships are implemented independently and documented with primary sources.

## Intended better-than-original delta

The scoped build is intended to improve the inputs by providing:

- no third-party executable runtime;
- a masked input and explicit sample-only warning;
- a finite pattern-aware estimator alongside the random model;
- selectable, labelled classical scenarios from local JSON;
- logarithmic calculations for long-input stability;
- a query-complexity-only Grover panel;
- separate Shor/PQC content;
- accessible responsive layout; and
- repeatable Python, Node, HTTP, static, and Chromium checks.

This is an intended delta, not an unqualified superiority claim. Evidence is recorded in `reports/local-proof.json` and remains local until independently reproduced.

## Safe build boundary

- Static HTML, CSS, browser JavaScript, local JSON, and Python standard-library proof tools.
- No Java.
- No backend, accounts, analytics, trackers, database, or credential storage.
- No network call involving the sample.
- No breach-corpus lookup.
- No real password requirement.
- No quantum wall-clock forecast.
- No parent root-page, workflow, settings, secret, license, package, release, or visibility change.
- No production, security-audit, hosted-CI, deployment, or readiness claim.

## Feature memory

### Current implementation scope

- responsive local-only analyzer;
- common, leetspeak, suffix, sequence, repeat, date, phrase, and random-space candidates;
- five classical attack profiles plus a bounded custom rate;
- Grover random-space query proxy;
- separate Shor/PQC threat explanation;
- primary-source links;
- N-App and surface metadata;
- Python reference model and local quality gate.

### First-MVP evidence required

- clean static load;
- analyzer works end-to-end with synthetic inputs;
- clear and show/hide controls work;
- all runtime dependencies remain local;
- privacy/static contract passes;
- Python and Node model tests pass;
- desktop and mobile browser smoke passes;
- current features and handoff are documented;
- owner review and merge decision.

### Future features

- optional locally bundled, license-reviewed mature pattern estimator;
- attack-profile import/export with provenance;
- broader browser and accessibility automation;
- localized explanatory content;
- a separate PQC migration visualizer.

### Out of scope

- cracking passwords;
- accepting uploaded hash databases;
- online account testing;
- breach lookup;
- hardware benchmarking;
- authentication policy enforcement;
- a fault-tolerant quantum resource estimate;
- server-side Python on GitHub Pages.

### Owner decision needed

- whether to add a root-page navigation link in a later, separately scoped change;
- whether to retain parent branding in the final public copy;
- whether future breach-awareness features may make network requests;
- whether to formalize this surface as an independent N-Suite app later.

## Proof needed for a later status upgrade

- local proof reproduced from a clean checkout;
- human visual and content review;
- live changed-file and head-SHA review;
- owner-approved merge;
- post-merge Pages verification at the intended subpath;
- any additional N-RepoOps or parent-repository requirements then current.

## Machine-readable record

```json
{
  "schema_version": "n.product.recon.v1",
  "title": "Password Threat Lab",
  "source": "owner brief, prior Python estimator, and supplied Gemini HTML prototype",
  "source_summary": "Educational classical-versus-quantum password and cryptography explainer with an interactive estimator.",
  "user_problem": "Publish a privacy-first educational estimator on GitHub Pages without misleading quantum timing claims.",
  "n_stack_overlap": ["NOVAK-Hash-Monitor", "N-SHA-Lab", "N-Idea", "N-RepoOps", "N-Suite", "N-App-SDK"],
  "route_decision": "extend-existing",
  "do_not_reuse": ["source branding", "source prose", "Tailwind CDN", "external fonts", "fixed quantum timer", "unsupported benchmark claims"],
  "better_than_original_delta": ["local-only runtime", "pattern-aware comparison", "transparent profiles", "query-only Grover framing", "Shor separation", "evidence floor"],
  "proof_needed": ["tests", "static privacy check", "HTTP smoke", "browser smoke", "human review", "post-merge Pages verification"],
  "safe_build_boundary": ["scoped subpath", "no backend", "no telemetry", "no password transmission", "no Java", "no readiness or security claim"],
  "next_action": "Open a scoped draft pull request against NOVAK-Hash-Monitor and stop before merge."
}
```
