# N-VIBE Scan Evidence and Limitation Note

## Status

Bounded static and local-runtime review only. This is not a formal security audit, penetration test, privacy certification, accessibility certification, or assurance that the hosting environment is uncompromised.

## Reviewed controls

- No submitting HTML form.
- Password input defaults to `type="password"`.
- No external runtime script, stylesheet, font, or image dependency.
- Restrictive CSP meta policy without `unsafe-inline` or `unsafe-eval`.
- No `localStorage`, `sessionStorage`, cookies, `sendBeacon`, `XMLHttpRequest`, or WebSocket use.
- Same-origin `fetch()` is limited to attack-profile JSON.
- No console logging in application JavaScript.
- Sample cleared on `pagehide`.
- Text is rendered with `textContent`, not user-controlled HTML.
- External links are limited by the static check to approved NIST/NCCoE hosts.
- Long arithmetic uses logarithms rather than unbounded integer expansion.
- No actual cracking, hashes, usernames, account identifiers, or breach data are accepted.

## Residual risks

1. A user can ignore the warning and enter a real credential.
2. Browser extensions, malware, screen recording, clipboard history, accessibility tooling, or a compromised OS can observe input.
3. GitHub Pages response headers are not controlled by this subdirectory; a CSP meta tag has narrower capabilities than an HTTP header.
4. Source links navigate away from the site and are subject to the destination's policies.
5. Future edits could introduce an external dependency or transmission path unless the static gate remains enforced.
6. Heuristic estimates can understate or overstate actual guess order.
7. Custom guess rates can be unreasonable and are only bounded numerically.
8. Quantum query complexity can be misunderstood as practical machine capability.
9. The parent repository's root page currently uses third-party dependencies; this isolated sub-surface does not remediate the parent surface.

## Before-exposure recommendation

- Keep the work in a draft pull request.
- Review the actual changed-file set.
- Re-run the quality gate at the final head SHA.
- Manually inspect the rendered page in at least one desktop and one mobile-size browser.
- Preserve the warning, CSP, no-third-party rule, and no-wall-clock quantum boundary.
- Obtain exact owner authorization before merge and Pages publication.

## Claim boundary

The available evidence supports only the statement that the candidate passed the recorded local checks in the recorded environment. It does not establish that the site is secure, audited, production-ready, production-grade, or safe for real credentials.
