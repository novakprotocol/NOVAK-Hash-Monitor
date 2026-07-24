# Password Threat Lab

A static, local-only educational surface for comparing:

- pattern-aware classical password guessing;
- a uniform random-character search-space upper bound;
- selected illustrative classical guess-rate scenarios;
- Grover's square-root query-complexity proxy; and
- Shor's separate threat to vulnerable public-key cryptography.

The project is scoped as an extension of the public `NOVAK-Hash-Monitor` GitHub Pages repository. It is not a password cracker, authentication system, breached-password service, hardware benchmark, quantum resource estimate, or security audit.

## Public path after approved merge

```text
https://novakprotocol.github.io/NOVAK-Hash-Monitor/password-threat-lab/
```

A branch or draft pull request does not constitute Pages deployment. The path above becomes the intended public surface only after an authorized merge to the repository's publishing source.

## Privacy boundary

- No account, backend, database, analytics, cookies, or third-party scripts.
- The sample is processed only in browser memory.
- The sample is not placed in the URL, written to browser storage, hashed, logged, or transmitted by the application.
- The input is cleared on `pagehide`.
- Same-origin `fetch()` is used only to load `data/attack-profiles.json`; a built-in fallback supports direct local opening.
- Browser extensions, screen capture, malware, and a compromised endpoint are outside this page's control.

Do not enter a real credential. Use a structurally similar made-up sample.

## Run locally

Python 3.10 or later is recommended. The runtime and proof tooling use only the Python standard library.

```bash
cd password-threat-lab
python serve.py
```

Open:

```text
http://127.0.0.1:8000/
```

The public interaction layer uses HTML, CSS, and browser JavaScript. It uses no Java.

## Estimation model

The calculator reports two classical values:

1. **Pattern-aware estimate** — the lowest-cost strategy found among a bounded set of common-password, leetspeak, suffix, sequence, repeat, date, passphrase, and character-space models.
2. **Random-model upper bound** — the average position in an inferred full character space, assuming the value was sampled uniformly at random.

Classical time is calculated from:

```text
average guesses / selected guesses per second
```

The rates in `data/attack-profiles.json` are transparent educational assumptions. They are not represented as current GPU benchmarks. A defensible deployment should replace them with measurements for the exact hash, parameters, software, hardware, and date relevant to the threat model.

### Grover boundary

The page displays the square root of the **random-model** average search work as a query-complexity proxy. It does not convert that proxy into seconds. A wall-clock quantum estimate would require a reversible verifier circuit, logical-depth analysis, error-correction assumptions, hardware assumptions, and a treatment of serial oracle queries.

### Shor boundary

Shor's algorithm is described separately because its principal cryptographic impact is on mathematical problems used by vulnerable public-key systems such as RSA and elliptic-curve cryptography. It is not modeled as a direct password-hash guessing profile.

## Local proof

Run the complete gate:

```bash
python scripts/quality_gate.py
```

Write a machine-readable local receipt:

```bash
python scripts/quality_gate.py --write-report reports/local-proof.json
```

The gate checks:

- the scoped RepoOps file floor;
- JSON validity;
- whitespace and final-newline discipline;
- `app.manifest.json` and `app.surface.json` contracts;
- CSP, local-dependency, privacy, and approved-source-link rules;
- Python reference-model tests;
- JavaScript estimator tests when Node.js is available;
- loopback HTTP asset loading; and
- a Chromium rendered-page smoke test when Chromium is available.

A passing local receipt is not hosted CI, production readiness, production-grade status, or a formal security review.

## Primary sources

The interface links directly to official NIST and NCCoE materials, including:

- NIST SP 800-63B for password verifier requirements;
- NIST CSRC material on practical Grover costs;
- NIST quantum cryptanalysis context for Shor and Grover;
- NIST's FIPS 203, 204, and 205 announcement; and
- NCCoE's post-quantum migration fact sheet.

## N-stack route

- **N-Idea decision:** `extend-existing`.
- **Owning product repository:** `NOVAK-Hash-Monitor`.
- **N-RepoOps boundary:** isolated subdirectory, local evidence, draft-PR-first, no workflow/settings/license/release changes.
- **N-Suite accounting:** a new repository registry entry is not required because this is a new surface inside an existing public product repository.
- **N-SDT state:** recorded under `docs/n-sdt/`.
- **N-VIBE state:** bounded static review and limitation note under `docs/nvibe/`; no formal audit claim.

See `docs/PRODUCT_RECONNAISSANCE.md` and `docs/STACK_EVIDENCE_PACKET.md`.

## Layout

```text
password-threat-lab/
├── index.html
├── assets/
│   ├── app.js
│   ├── estimator.js
│   ├── styles.css
│   └── sections.css
├── data/attack-profiles.json
├── app.manifest.json
├── app.surface.json
├── docs/
├── reports/
├── scripts/
├── tests/
├── tools/reference_estimator.py
└── serve.py
```

## License and contribution boundary

This subdirectory does not alter the parent repository's license, contribution policy, trademark position, or release terms. Parent repository terms apply. No license or repository-setting change is part of this work packet.
