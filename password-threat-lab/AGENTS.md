# AGENTS.md

## Read first

1. `README.md`
2. `docs/PRODUCT_RECONNAISSANCE.md`
3. `docs/STACK_EVIDENCE_PACKET.md`
4. `docs/n-sdt/current-truth.md`
5. `NEXT_RUN.md`
6. `COMMANDS.md`
7. `.repo-standard.yml`

## Scope

Work only inside `password-threat-lab/**` unless the owner explicitly authorizes a wider parent-repository change.

## Rules

- Preserve the N-Idea route decision: `extend-existing`.
- Do not replace or silently edit the parent repository root page.
- Keep the public runtime local-only and dependency-free.
- Do not introduce forms, telemetry, third-party scripts, browser persistence, or password transmission.
- Do not convert Grover query complexity into a confident wall-clock estimate.
- Keep Shor and PQC separate from direct password guessing.
- Do not use Java.
- Do not change workflows, settings, secrets, licenses, packages, releases, visibility, or Pages configuration without exact owner approval.
- Do not claim MVP-ready, production-ready, production-grade, hosted-CI-green, secure, audited, or deployed status without current evidence and the required approval.
- Use representative synthetic samples in tests and screenshots; never include a real credential.

## Required local checks

```bash
python scripts/quality_gate.py --write-report reports/local-proof.json
```

A later merge still requires the exact owner authorization defined in `docs/n-sdt/handoff.md`.
