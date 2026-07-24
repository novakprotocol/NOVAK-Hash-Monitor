# Product Reconnaissance — Password Threat Lab

## Record

- Schema: `n.product.recon.v1`
- Decision: `extend-existing`
- Target repository: `novakprotocol/NOVAK-Hash-Monitor`
- Target path: `password-threat-lab/`
- Repo class: public educational static-site extension
- New repository required: no

## 1. Trigger

The owner requested a public password break-time educational site and supplied:

- a previously generated Python standard-library estimator; and
- a Gemini-generated single-page HTML concept comparing classical attacks, Grover's algorithm, Shor's algorithm, and PQC.

The owner then directed the work through N-Suite/N-stack, N-Idea, and N-RepoOps.

## 2. Source summary

The supplied HTML concept presents four educational threat panels and a browser calculator. Its calculator infers a character set, computes `charset^length`, divides by an illustrative classical rate, and applies a square root for a quantum comparison. It uses Tailwind's browser CDN, external Google Fonts, and inline JavaScript.

The prior Python estimator adds bounded pattern detection, configurable JSON profiles, local serving, and tests, but it cannot run server-side on GitHub Pages.

## 3. User problem

Users need a clear explanation of why:

- current password-cracking charts generally describe classical offline attacks;
- human-chosen patterns can be far weaker than a uniform character-space calculation suggests;
- Grover provides a query-complexity advantage rather than a simple universal quantum guesses-per-second number; and
- Shor's algorithm is primarily a public-key migration threat, not a direct password-hash cracking profile.

## 4. Product and market reconnaissance

Password-strength meters and crack-time estimators are a crowded category. A limited GitHub reconnaissance found multiple projects using names such as `password-strength-checker` and `password-crack-time-estimator`, along with established zxcvbn implementations. The reconnaissance does not establish an exact project count.

The differentiation opportunity is not another dramatic timer. It is a privacy-first, dependency-free, transparent threat-model lab that separates classical guessing, Grover query complexity, and Shor/PQC migration.

## 5. N-stack overlap

| Owner | Overlap | Decision |
|---|---|---|
| `NOVAK-Hash-Monitor` | Existing public browser-based cryptographic education and GitHub Pages surface | Owns implementation |
| `N-SHA-Lab` | Private hash education and analysis laboratory | Do not duplicate; no direct product route needed |
| `N-Idea` | Reconnaissance and route decision | Owns this record shape |
| `N-RepoOps` | Repository floor, evidence, PR boundaries, and claims | Governs work packet |
| `N-Suite` | Portfolio accounting | No new repo registry entry; existing product gains a sub-surface |
| `N-App-SDK` | Manifest and surface contracts | Scoped contracts included |
| `N-SDT` | Current truth and handoff | Scoped docs included |
| `N-VIBE` | Before-exposure risk evidence | Limitation note and static checks included |

## 6. Route decision

`extend-existing`

Reasons:

1. `NOVAK-Hash-Monitor` is already a public cryptographic education site with GitHub Pages.
2. The requested surface is adjacent to its existing hash and integrity education scope.
3. A new repository would duplicate public-site operations, branding, and Pages configuration.
4. An isolated subpath limits regression risk to the existing root application.

## 7. Material not to reuse

- Gemini or another provider's branding.
- Source-specific prose or visual identity.
- Tailwind CDN or other third-party executable dependencies.
- External web fonts.
- The simplistic claim that a uniform `charset^length` result accurately models human passwords.
- A fixed quantum operations-per-second timer.
- Unsupported annual GPU improvement percentages or named-device benchmark claims.

The implementation is independently written from the stated product requirements and public technical concepts.

## 8. Intended better-than-original delta

The N-stack version is intended to provide:

- no third-party runtime dependencies;
- a prominent do-not-enter-real-credentials boundary;
- no password submission, storage, hashing, analytics, or telemetry;
- pattern-aware and random-model results side by side;
- average-guess calculations in logarithmic space;
- configurable, clearly illustrative classical profiles;
- Grover query complexity without fabricated wall-clock precision;
- separate Shor/PQC context;
- official primary-source links;
- accessibility and responsive layout;
- Python and JavaScript contract tests; and
- N-stack manifests, current truth, handoff, and local proof.

This is an implementation target, not a superiority claim. Evidence is listed below.

## 9. Proof needed

- Python reference-model tests pass.
- JavaScript estimator tests pass where Node.js is available.
- Static scan finds no external scripts, stylesheets, storage APIs, or submission form.
- Local HTTP smoke loads every required asset.
- Chromium renders the page and reaches the application-ready state where available.
- Human review confirms copy, accessibility, and visual hierarchy.
- Draft PR shows only scoped files plus an optional parent README link.
- Exact owner approval is recorded before merge and Pages publication.

## 10. Safety boundary

- Educational estimator only.
- No actual password cracking or hash ingestion.
- No breach corpus or username/context lookup.
- No real credential required or requested.
- No network submission of the sample.
- No authentication, access-control, or policy decision.
- No claim that a displayed time predicts a specific attacker.
- No Grover wall-clock or fault-tolerant hardware forecast.
- No claim that Shor currently breaks a specific live connection.
- No production-ready, production-grade, secure, audited, or hosted-CI-green claim.

## 11. Feature memory

### Current implementation target

- Static GitHub Pages-compatible analyzer.
- Local pattern-aware estimator.
- Random-space comparison.
- Classical attack profiles from local JSON.
- Custom illustrative rate.
- Grover random-space query proxy.
- Shor/PQC educational separation.
- Primary-source section.
- Local proof and N-stack docs.

### Future

- Vetted benchmark import with full provenance.
- Additional local strength model after license review.
- Automated accessibility suite.
- Localization.

### Out of scope

- Server-side Python on GitHub Pages.
- Java.
- Password cracking, hash uploads, or credential collection.
- Remote breached-password API.
- User accounts, analytics, ads, or telemetry.
- Root-site redesign.
- Workflow, settings, license, package, or release changes.

### Owner decision needed

- Final public wording and brand placement.
- Whether to add a root-site navigation link after the isolated surface is reviewed.
- Exact merge method and publication authorization.

## 12. MVP-ready evidence boundary

The surface may be considered for an MVP-ready review only when:

- the primary local and Pages paths render end to end;
- all required local checks pass at the reviewed head SHA;
- the privacy and claim boundaries remain intact;
- current features match implementation;
- review feedback is resolved; and
- the owner separately authorizes any claim upgrade.

No MVP-ready claim is made in this packet.

## Machine-readable equivalent

```json
{
  "schema_version": "n.product.recon.v1",
  "title": "Password Threat Lab",
  "source": "owner request, supplied HTML concept, and prior Python estimator",
  "source_summary": "Educational classical-versus-quantum password threat page with an interactive calculator.",
  "user_problem": "Explain classical crack-time assumptions while separating Grover query complexity and Shor public-key risk.",
  "n_stack_overlap": [
    "NOVAK-Hash-Monitor",
    "N-SHA-Lab",
    "N-Idea",
    "N-RepoOps",
    "N-Suite",
    "N-App-SDK",
    "N-SDT",
    "N-VIBE"
  ],
  "route_decision": "extend-existing",
  "do_not_reuse": [
    "source branding",
    "source-specific copy",
    "Tailwind CDN",
    "external fonts",
    "fixed quantum operations-per-second timer",
    "unsupported benchmark claims"
  ],
  "better_than_original_delta": [
    "local-only",
    "third-party dependency free",
    "pattern-aware",
    "transparent assumptions",
    "Grover query boundary",
    "N-stack evidence"
  ],
  "proof_needed": [
    "Python tests",
    "JavaScript tests",
    "static privacy scan",
    "loopback HTTP smoke",
    "Chromium render smoke",
    "human review",
    "draft PR",
    "exact merge approval"
  ],
  "feature_memory": {
    "current_features": [
      "static analyzer",
      "pattern-aware estimate",
      "random-space estimate",
      "attack profile JSON",
      "Grover query proxy",
      "Shor/PQC context"
    ],
    "mvp_required_features": [
      "primary user path works end to end",
      "privacy boundary holds",
      "local gate passes",
      "review complete"
    ],
    "future_features": [
      "benchmark imports",
      "additional licensed local model",
      "accessibility automation",
      "localization"
    ],
    "out_of_scope_features": [
      "password cracking",
      "credential collection",
      "remote breach API",
      "server-side GitHub Pages Python",
      "Java"
    ],
    "blocked_features": [],
    "owner_decision_needed": [
      "final brand placement",
      "root navigation link",
      "merge method and publication"
    ]
  },
  "mvp_ready_evidence": [
    "clean local serve",
    "core tests",
    "quality gate",
    "render proof",
    "current features doc",
    "owner review"
  ],
  "safe_build_boundary": [
    "static local-only surface",
    "no third-party runtime dependencies",
    "no real credentials",
    "no production or audit claim",
    "no settings, workflow, license, package, or release changes"
  ],
  "next_action": "Create an isolated draft PR in NOVAK-Hash-Monitor and stop before merge/publication."
}
```
