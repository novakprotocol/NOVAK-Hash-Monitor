# Commands

## Launch

```bash
python serve.py
python serve.py --port 8080 --open
```

## Focused validation

```bash
python scripts/check_napp_contract.py
python scripts/check_surface_contract.py
python scripts/check_static_site.py
python -m unittest discover -s tests -v
node tests/test_browser_contract.mjs
python scripts/browser_smoke.py
```

## Complete local proof

```bash
python scripts/quality_gate.py --write-report reports/local-proof.json
```

## Regenerate visual evidence

```bash
python scripts/browser_smoke.py --screenshots
```

## Operational boundary

No command in this directory changes GitHub settings, Pages settings, workflows, secrets, licenses, packages, releases, repository visibility, or protected branches.
