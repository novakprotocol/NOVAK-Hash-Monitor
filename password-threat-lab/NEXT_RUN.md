# NEXT_RUN

## Current objective

Review the scoped Password Threat Lab draft pull request, confirm the local-proof receipt, and decide whether the isolated Pages subpath should be merged.

## Start sequence

1. Read the live pull request and current head SHA.
2. Confirm all changed paths remain under `password-threat-lab/**`.
3. Read `docs/n-sdt/current-truth.md` and `docs/n-sdt/handoff.md`.
4. Run `python scripts/quality_gate.py --write-report reports/local-proof.json` from this directory.
5. Inspect the desktop and mobile layout using synthetic samples only.
6. Verify the parent root page, workflows, settings, license, packages, releases, and visibility are unchanged.

## Stop conditions

Stop and request a new scoped decision if:

- files outside `password-threat-lab/**` changed;
- external runtime dependencies or telemetry appear;
- a workflow, license, setting, secret, package, release, or visibility change is proposed;
- the live head differs from the head named in an approval;
- local proof fails or is stale;
- any readiness, security, audit, hosted-CI, or deployment claim exceeds evidence.

## Merge boundary

Do not mark ready or merge from this file alone. Use the exact authorization format in `docs/n-sdt/handoff.md` after verifying the live PR number and full head SHA.
