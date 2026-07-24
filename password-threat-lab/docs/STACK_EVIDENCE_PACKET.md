# N-Stack Evidence Packet

## Branch / Base / Bounds

- Repository: `novakprotocol/NOVAK-Hash-Monitor`
- Base branch: `main`
- Base commit observed before branch creation: `630acfc764b2986dd607fdeb61d9545a511b8d13`
- Work branch: `agent/password-threat-lab`
- Allowed path: `password-threat-lab/**`
- Explicitly excluded: root `index.html`, `.github/**`, repository or Pages settings, secrets, licenses, packages, releases, visibility, branch protection, and parent product claims.

## Worktree / Work lease

No user worktree or local checkout was assumed. The implementation was assembled in an isolated execution workspace, validated there, then prepared for GitHub as a non-main branch patch. The work lease ends at the draft-pull-request boundary unless the owner supplies a new scoped instruction.

## Receipts / Risks

Expected receipt:

- `reports/local-proof.json`
- Python unit-test output
- Node estimator-test output
- static privacy/dependency check
- loopback HTTP asset check
- synthetic Chromium interaction smoke
- optional screenshots generated from synthetic input

Material residual risks:

- The estimator is bounded and heuristic; an attacker may use strategies not modeled.
- Scenario rates are assumptions, not verified hardware benchmarks.
- Browser extensions, clipboard history, screen capture, and device compromise are outside the application boundary.
- A meta CSP is weaker than a response-header CSP; GitHub Pages response headers are not controlled by this scoped patch.
- Primary-source links leave the local page only after user action.
- The parent root page's existing third-party dependencies are not remediated by this isolated subsite.
- Local proof is not hosted CI or a formal audit.

## Authority / Approvals

The owner's instruction to “run this through N-Suite/N-stack, N-Idea, and RepoOps” and “go” is treated as authorization for:

- live read-only stack reconnaissance;
- route selection;
- the scoped non-main branch;
- files under `password-threat-lab/**`;
- local proof; and
- a draft pull request.

It is not treated as authorization to:

- mark the pull request ready;
- merge;
- delete the branch;
- change settings or workflows;
- change secrets, license, packages, releases, or visibility;
- publish a release; or
- upgrade readiness, security, audit, hosted-CI, or deployment claims.

## Final handoff / Fail-safe

The run stops after opening a draft pull request and recording the current head. Before merge, re-read live changed files, proof, and head SHA. Any scope drift or failed proof stops the action.

Exact merge approval format:

```text
Approve merge of novakprotocol/NOVAK-Hash-Monitor PR #<number> using <merge method> at head <full SHA>.
```

The intended Pages subpath is not considered live until an approved merge and direct post-merge verification succeed.
