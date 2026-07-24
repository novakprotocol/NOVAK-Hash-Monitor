# AGENTS.md

## Read first

1. `README.md`
2. `docs/PRODUCT_RECONNAISSANCE.md`
3. `docs/STACK_EVIDENCE_PACKET.md`
4. `docs/product/CURRENT_FEATURES.md`
5. `docs/n-sdt/current-truth.md`
6. `NEXT_RUN.md`
7. `COMMANDS.md`
8. `.repo-standard.yml`

## Scope

This directory owns the Password Threat Lab static Pages surface, its bounded estimator, scoped manifests, documentation, and local proof.

The parent `NOVAK-Hash-Monitor` repository owns the public repository, root Pages surface, license, release policy, and broader product claims.

## Rules

- Keep all application computation local to the browser.
- Never add analytics, trackers, third-party scripts, external fonts, cookies, or credential submission.
- Never put the analyzed value in a URL, storage API, log, report, test fixture, screenshot, or telemetry event.
- Tests may use only clearly synthetic examples.
- Keep Grover output as query complexity; do not invent a wall-clock quantum cracking time.
- Keep Shor separate from password-hash guessing.
- Label attack rates as illustrative unless exact benchmark evidence is recorded.
- Prefer official NIST/NCCoE primary sources for factual cryptographic claims.
- Preserve the parent repository's license and contribution boundary.
- Do not edit root Pages behavior, repository settings, workflows, secrets, release metadata, or visibility without exact owner approval.
- Do not claim hosted CI, MVP-ready, production-ready, production-grade, secure, audited, or quantum-feasible status without the corresponding evidence and approval.

## Required checks

```bash
python scripts/quality_gate.py
```

Focused checks:

```bash
python scripts/check_napp_contract.py
python scripts/check_surface_contract.py
python scripts/check_static_site.py
python -m unittest discover -s tests -p "test_*.py" -v
node tests/test_browser_contract.mjs
```

Node.js and Chromium checks are evidence-enhancing but environment-dependent. The Python gate records `not-run` honestly when either executable is unavailable.

## Handoff rule

Update `docs/n-sdt/current-truth.md`, `docs/n-sdt/handoff.md`, `docs/product/CURRENT_FEATURES.md`, and the local-proof receipt when behavior changes. Keep wish-list items out of the current-features file.
