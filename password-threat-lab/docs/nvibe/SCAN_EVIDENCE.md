# N-VIBE Limitation and Risk Evidence

## Scope

This is a bounded pre-exposure risk review of `password-threat-lab/**`. It is not an N-VIBE formal scan result, penetration test, cryptographic review, or security audit.

## Positive controls in the candidate

- no form submission;
- no backend or account system;
- no third-party scripts, fonts, analytics, or trackers;
- no cookies, local storage, or session storage;
- no sample hashing or transmission;
- local JSON only;
- text-only DOM rendering;
- masked input by default;
- 256-character input limit;
- explicit sample-only warning and pagehide clear;
- restrictive meta CSP;
- source links limited by static policy to NIST and NCCoE;
- synthetic samples in automated checks.

## Residual risks

| Risk | Current treatment | Residual boundary |
|---|---|---|
| Users enter a real credential | prominent warning and masked input | user behavior cannot be guaranteed |
| Browser extension or compromised device reads input | no app persistence or transmission | outside the page's trust boundary |
| Model overstates security | pattern/random comparison and claim text | bounded heuristics omit attacker strategies |
| Scenario rate is mistaken for a benchmark | profiles labelled illustrative | users may still overgeneralize |
| Grover proxy is mistaken for feasibility | no seconds; query-only explanation | not a fault-tolerant resource estimate |
| Meta CSP limitations | strict meta policy | GitHub Pages response headers are outside scope |
| External source navigation leaks ordinary metadata | `no-referrer`, explicit links | destination receives a user-initiated request |
| Parent root page has external dependencies | isolated subpath has none | root-page remediation is separate work |

## Exposure decision

Suitable for owner and reviewer evaluation as a draft candidate, subject to local proof and content review. This file does not authorize merge, public deployment, readiness claims, or security claims.
