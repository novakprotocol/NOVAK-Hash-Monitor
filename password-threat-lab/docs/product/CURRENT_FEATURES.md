# Current Features

Only implemented features with local proof are listed here.

| Feature | Evidence |
|---|---|
| Static responsive analyzer page | `index.html`, `assets/styles.css`, browser smoke |
| Masked representative-sample input with show/hide and clear | `index.html`, `assets/app.js`, browser smoke |
| No form submission or browser persistence | `scripts/check_static_site.py` |
| Common-password and basic leetspeak recognition | `assets/estimator.js`, Python and Node tests |
| Predictable word-plus-number/punctuation detection | estimator tests using synthetic `Password1!` |
| Keyboard, character-sequence, repeated-character, repeated-block, date, and word-phrase candidates | estimator source and tests |
| Random-character upper-bound estimate using logarithmic work units | estimator source and long-input tests |
| Five local classical attack profiles plus bounded custom rate | `data/attack-profiles.json`, `assets/app.js` |
| Grover square-root query proxy without wall-clock timing | estimator source, UI, Python and Node tests |
| Separate Shor/PQC educational section | `index.html` |
| Primary-source links restricted to NIST and NCCoE | `index.html`, static checker |
| N-App and surface contracts | `app.manifest.json`, `app.surface.json`, contract checks |
| Python reference model and repeatable local quality gate | `tools/reference_estimator.py`, `scripts/quality_gate.py` |
