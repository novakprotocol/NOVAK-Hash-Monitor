# Handoff

## Next safe action

Review the live draft pull request and reproduce the local quality gate from the scoped directory.

```bash
python scripts/quality_gate.py --write-report reports/local-proof.json
```

## Required live checks before any merge decision

1. Confirm repository and pull-request number.
2. Confirm base is `main`.
3. Confirm head is `agent/password-threat-lab` and capture its full current SHA.
4. Confirm every changed path is under `password-threat-lab/**`.
5. Confirm no workflow, setting, secret, license, package, release, visibility, or root-page change exists.
6. Review `reports/local-proof.json`; reproduce the checks if the head changed.
7. Use synthetic samples only for visual review.
8. Preserve all claim boundaries.

## Exact authorization required to merge

```text
Approve merge of novakprotocol/NOVAK-Hash-Monitor PR #<number> using <merge method> at head <full SHA>.
```

An approval naming a stale SHA, different repository, different PR, or different merge method is insufficient.

## Post-merge verification, only after approval and merge

- open the intended Pages subpath directly;
- verify CSS, JavaScript, and JSON load from the subpath;
- exercise a synthetic sample;
- confirm no network request contains the sample;
- record the exact deployed commit and verification result;
- do not claim deployment, MVP readiness, production readiness, security, or audit status beyond the recorded evidence.

## Fail-safe

Stop on scope drift, stale evidence, failed checks, blocked Pages behavior, or any request to bypass a hard gate.
