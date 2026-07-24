# GitHub Delivery Record

## Target

- Repository: `novakprotocol/NOVAK-Hash-Monitor`
- Visibility observed: public
- Default branch observed: `main`
- Intended feature branch: `agent/password-threat-lab-v1`
- Intended path: `password-threat-lab/`
- Intended PR state: draft

## Baseline observation

At the GitHub inspection performed on 2026-07-24:

- `main` was observed at `630acfc764b2986dd607fdeb61d9545a511b8d13`;
- no branch matching `password-threat` was found;
- no pull request matching `password threat lab` was found; and
- `password-threat-lab/index.html` was absent from the default branch.

This is a point-in-time observation, not a lock. Refresh `origin/main`, confirm the target path is still absent, and review the live diff before creating or updating the PR.

## Delivery boundaries

The prepared patch adds only `password-threat-lab/**`. It deliberately does not modify the parent root page, README, workflows, settings, visibility, Pages source, secrets, branch protections, license, packages, releases, or tags.

A root-site discovery link is an optional follow-up after owner review; it is not required for the direct Pages path to work after merge.

## Exact checks before push

```bash
git status --short
git fetch origin main
git diff --check origin/main...HEAD
python password-threat-lab/scripts/quality_gate.py \
  --write-report password-threat-lab/reports/local-proof.json
git diff --check
```

## Exact checks before merge authorization

- Read the current PR changed-file list.
- Confirm the live PR head SHA.
- Re-run or verify proof against that SHA.
- Confirm no workflow, settings, license, release, package, secret, or root-surface changes entered the PR.
- Obtain a fresh exact owner authorization naming repository, PR number, merge method, and live head SHA.
