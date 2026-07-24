# N-Stack Evidence Packet

## Work packet

- Goal: add a professional, public-ready Password Threat Lab as an isolated static surface.
- Owner repository: `novakprotocol/NOVAK-Hash-Monitor`.
- Route: `extend-existing`.
- Planned branch: `agent/password-threat-lab-v1`.
- Base: refresh live `main` at branch creation and repeat the exact SHA in the pull request.
- Inspected baseline: `630acfc764b2986dd607fdeb61d9545a511b8d13` on 2026-07-24; this must be refreshed before write operations.
- Bounds: `password-threat-lab/**` plus a minimal parent `readme.md` discovery link if included.
- Excluded: root `index.html`, workflows, settings, visibility, secrets, license, packages, releases, and production/security claim surfaces.

## B/W/R/A/F Buddy Check

### B — Branch / Base / Bounds

- Non-main branch required.
- Base branch: `main`.
- Product changes remain in `password-threat-lab/`.
- No root Pages behavior replacement.
- No force-push or branch deletion.

### W — Worktree / Work lease

- No user worktree was assumed or modified.
- Files were generated and checked in an isolated tool workspace.
- GitHub writes are limited to the named branch and draft pull request.
- Unrelated parent-repository content must remain unchanged.

### R — Receipts / Risks

Expected receipts:

- `reports/local-proof.json` from the complete local quality gate.
- Python unit-test output.
- JavaScript contract-test output where Node.js exists.
- Chromium render smoke where Chromium exists.
- Draft PR changed-file review.

Primary risks:

1. Users may enter a real credential despite the warning.
2. Heuristic times may be mistaken for precise attacker forecasts.
3. A static CSP meta tag cannot provide every response-header protection.
4. Browser extensions or endpoint compromise can observe page contents.
5. Attack-rate assumptions can become stale or be quoted without context.
6. Grover query complexity may be misread as a practical quantum machine forecast.
7. Parent branding or licensing language may require owner adjustment.

Mitigations are documented in the interface, static checks, N-VIBE note, and claim boundary.

### A — Authority / Approvals

- The owner explicitly directed the work through the N-stack and said to proceed.
- That direction authorizes scoped branch creation, files, local proof, and a draft PR for this task.
- Because the target repository is public, branch and PR content are publicly visible; the owner's instruction included a public website objective.
- Mark-ready, merge, branch deletion, Pages publication, settings, workflow, secret, license, package, release, and claim upgrades remain hard-gated.
- Merge requires a fresh exact owner line naming repository, PR number, merge method, and current live head SHA.

### F — Final handoff / Fail-safe

- Stop after draft PR creation and evidence reporting.
- Do not infer that the site is deployed because the branch exists.
- Do not mark the PR ready or merge it without exact owner approval and fresh head verification.
- If local and GitHub evidence diverge, GitHub state wins and the packet must be refreshed.

## Extension packet

This is an existing-repository extension, not a new-repository birth. The analogous birth fields are preserved here:

| Field | Decision |
|---|---|
| Repo class | Static educational web surface |
| Product owner | `NOVAK-Hash-Monitor` |
| Recon label | `extend-existing` |
| Current features | See `docs/product/CURRENT_FEATURES.md` |
| MVP boundary | End-to-end local/Pages path, privacy intact, checks pass, review complete |
| Future features | See `docs/product/CURRENT_VS_PLANNED.md` |
| Out of scope | Cracking, credential collection, remote breach lookup, quantum wall-clock forecast |
| Local checks | `python scripts/quality_gate.py` |
| Claim boundary | Candidate only; no readiness, security, audit, or benchmark claim |
| Handoff | `docs/n-sdt/handoff.md` |

## N-Suite accounting decision

No new N-Suite repository registry entry is proposed. The work adds a product surface inside an already existing public repository. Portfolio accounting can reference the target PR or a later feature-map update after merge; it should not register a duplicate N-family repository.

## Publication boundary

The intended post-merge Pages path is:

```text
https://novakprotocol.github.io/NOVAK-Hash-Monitor/password-threat-lab/
```

This packet does not claim that the path is live at the draft-PR stage.
