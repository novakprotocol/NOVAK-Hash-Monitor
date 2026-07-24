# Password Threat Lab

A privacy-first educational GitHub Pages surface for comparing:

- a bounded, pattern-aware classical password estimate;
- a random-character search-space estimate;
- an illustrative Grover square-root query proxy; and
- Shor's separate threat to vulnerable public-key cryptography.

This directory is a scoped extension of `novakprotocol/NOVAK-Hash-Monitor`, routed through N-Idea as `extend-existing`. It does not replace the parent site's root page.

## Intended public path

After an owner-approved merge into the Pages source branch, the intended path is:

```text
https://novakprotocol.github.io/NOVAK-Hash-Monitor/password-threat-lab/
```

A branch or draft pull request is not a deployment claim.

## Privacy boundary

The public runtime:

- contains no form submission;
- loads no third-party scripts, fonts, analytics, or trackers;
- stores no sample in cookies, local storage, or session storage;
- does not hash, log, append to a URL, or transmit the entered value;
- renders results with text-only DOM operations; and
- clears the transient sample on `pagehide` and by explicit user action.

Use a representative sample, not a credential currently protecting an account. Browser extensions, screen capture, clipboard history, and a compromised device remain outside this page's control.

## No Java

The site uses HTML, CSS, and browser JavaScript. JavaScript is not Java. Python is retained for the local reference model, tests, quality gate, and loopback-only development server.

## Run locally

```bash
cd password-threat-lab
python serve.py
```

Open `http://127.0.0.1:8000/`.

Optional:

```bash
python serve.py --port 8080 --open
```

## Local proof

```bash
python scripts/check_napp_contract.py
python scripts/check_surface_contract.py
python scripts/check_static_site.py
python -m unittest discover -s tests -v
node tests/test_browser_contract.mjs
python scripts/browser_smoke.py --screenshots
python scripts/quality_gate.py --write-report reports/local-proof.json
```

The quality gate records local evidence only. It does not imply hosted CI passed, production readiness, production-grade status, secure deployment, or a formal security audit.

## Model boundary

The pattern model tests a finite set of common-password, substitution, suffix, keyboard, sequence, repetition, date, and word-phrase strategies. It is not Hashcat, zxcvbn, a breach corpus, or an exhaustive attacker model.

Classical time is estimated by dividing average guess work by an explicitly labelled illustrative scenario rate. The Grover panel reports query complexity based on the random-space model and deliberately does not convert that value into seconds. Shor and PQC are explained as a separate public-key migration problem.

## Repository and license boundary

The parent repository's terms govern this directory. This change does not modify, replace, or reinterpret the parent license. No workflow, repository setting, secret, package, release, or root-page change is included.
