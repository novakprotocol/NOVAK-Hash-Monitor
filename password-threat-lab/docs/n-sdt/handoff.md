# Handoff

## Last completed work

A scoped candidate was assembled for an isolated `password-threat-lab/` GitHub Pages surface inside `NOVAK-Hash-Monitor`.

## Verify first

1. Read live branch and pull-request state.
2. Confirm the current head SHA and changed-file list.
3. Compare live files with `docs/n-sdt/current-truth.md`.
4. Run:

```bash
python scripts/quality_gate.py
```

5. Confirm `reports/local-proof.json` was generated from the same source state.

## Review focus

- Privacy wording and do-not-enter-real-credentials warning.
- Whether any browser action can transmit or persist the sample.
- Pattern-model false confidence.
- Attack-rate labels and assumptions.
- Grover/Shor separation.
- Source accuracy and link destinations.
- Mobile, keyboard, and screen-reader behavior.
- Parent branding and license language.
- Whether a root README discovery link is sufficient.

## Stop conditions

Stop and request exact owner approval before:

- marking the pull request ready;
- merging;
- deleting the branch;
- publishing or claiming Pages deployment;
- changing root Pages behavior;
- changing workflows, settings, visibility, secrets, license, packages, or releases;
- upgrading MVP, production, security, audit, benchmark, or quantum-feasibility claims.

## Exact merge authority format

Use a fresh line containing:

```text
Approve merge of novakprotocol/NOVAK-Hash-Monitor PR #<number> using <merge method> at head <full SHA>.
```

Re-fetch live PR state and head SHA before acting.

## Next safe action

Review the draft pull request and local-proof receipt. Record findings without changing the claim boundary.
