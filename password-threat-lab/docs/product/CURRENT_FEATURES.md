# Current Features

This file lists only behavior implemented in the candidate source tree. It does not claim merge, Pages deployment, MVP readiness, production readiness, production-grade status, or formal security review.

| Implemented feature | Evidence |
|---|---|
| Responsive static analyzer | `index.html`, `assets/styles.css` |
| Password field defaults to concealed input | `index.html#passwordInput`, `scripts/check_static_site.py` |
| Show, hide, and clear controls | `assets/app.js`, `app.surface.json` |
| No submitting form | `index.html`, static privacy check |
| Pattern-aware heuristic | `assets/estimator.js`, `tools/reference_estimator.py` |
| Common-password and basic leetspeak detection | Estimator source and contract tests |
| Predictable word-plus-number suffix detection | Estimator source and contract tests |
| Sequence, repeat, date, and phrase signals | Estimator source and unit tests |
| Random-character search-space comparison | Estimator source and tests |
| Logarithmic count and duration formatting | Estimator source and long-input tests |
| Local JSON attack profiles | `data/attack-profiles.json` |
| Custom illustrative guess rate | `index.html`, `assets/app.js` |
| Grover random-space query proxy | `assets/estimator.js`, tests |
| No Grover wall-clock timer | Interface copy and static source review |
| Separate Shor/PQC context | `index.html#threat-map` |
| Official NIST/NCCoE source links | `index.html#sources` |
| No third-party scripts, stylesheets, or fonts | CSP plus `scripts/check_static_site.py` |
| No cookies or browser storage | `assets/app.js`, static privacy check |
| Same-origin configuration loading with fallback | `assets/app.js` |
| Input clearing on page hide | `assets/app.js` |
| Python loopback server | `serve.py` |
| Python reference model | `tools/reference_estimator.py` |
| Python and JavaScript contract tests | `tests/` |
| Machine-readable local proof | `scripts/quality_gate.py`, `reports/local-proof.json` after gate execution |
| Scoped N-App contracts | `app.manifest.json`, `app.surface.json` |
| N-Idea, RepoOps, N-SDT, N-VIBE, and feature-memory documentation | `docs/` |
