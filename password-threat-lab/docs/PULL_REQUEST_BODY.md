## Summary

Add `password-threat-lab/`, an isolated GitHub Pages surface for explaining password attack models without collecting or transmitting credentials.

The page compares:

- a bounded, pattern-aware classical estimate;
- a uniform random-character upper-bound model;
- transparent illustrative classical guess-rate scenarios;
- Grover's square-root query-complexity proxy without a wall-clock forecast; and
- Shor's separate impact on vulnerable public-key cryptography.

## N-stack route

- **N-Idea:** `extend-existing`
- **Owning repository:** `NOVAK-Hash-Monitor`
- **N-RepoOps:** scoped subdirectory, evidence-first, draft-PR lane
- **N-Suite:** no duplicate repository registration; this is an existing-repo surface
- **N-SDT:** current truth and handoff included
- **N-VIBE:** bounded static review and limitation note included

## Scope

Changed path:

```text
password-threat-lab/**
```

Not changed:

- root `index.html`;
- GitHub Actions or other workflows;
- repository settings, visibility, secrets, Pages source, or branch protections;
- parent license, contribution policy, packages, or releases; or
- production, security-audit, benchmark, or quantum-feasibility claims.

## Privacy and security boundary

- No form submission or backend.
- No analytics, cookies, browser storage, third-party scripts, stylesheets, fonts, or images.
- The sample remains in browser memory and is cleared on `pagehide`.
- The value is not placed in a URL, hashed, logged, persisted, or transmitted by the application.
- Same-origin `fetch()` loads only the local attack-profile JSON.
- A restrictive CSP meta policy is included.
- The interface tells users to use a made-up sample rather than a real credential.

This is a bounded educational implementation, not a formal security audit or assurance that a browser, extension, endpoint, or host is uncompromised.

## Validation

Local receipt: `password-threat-lab/reports/local-proof.json`

Recorded checks:

- required RepoOps file floor;
- JSON parsing and whitespace discipline;
- N-App manifest and surface contracts;
- static privacy, CSP, local-dependency, and approved-link checks;
- 12 Python reference-model tests;
- 11 JavaScript estimator assertions;
- loopback HTTP asset smoke; and
- Chromium interaction smoke using a synthetic sample.

Run again at the final PR head:

```bash
python password-threat-lab/scripts/quality_gate.py \
  --write-report password-threat-lab/reports/local-proof.json
git diff --check
```

## Risks and review focus

1. Confirm the warning against entering real credentials is prominent enough.
2. Confirm attack-rate assumptions are presented as examples, not current hardware benchmarks.
3. Confirm Grover is shown only as query complexity and Shor remains a separate public-key migration topic.
4. Confirm no external runtime dependency or transmission path was introduced.
5. Confirm the parent repository's branding and licensing language remain accurate.
6. Review the browser-smoke observations and the bounded visual-review note at `password-threat-lab/docs/VISUAL_REVIEW.md`.

## Publication boundary

The intended post-merge path is:

```text
https://novakprotocol.github.io/NOVAK-Hash-Monitor/password-threat-lab/
```

A branch, draft PR, local receipt, or successful review does not establish that the path is deployed. Mark-ready, merge, branch deletion, settings changes, Pages publication, and claim upgrades remain separately authorized actions.
