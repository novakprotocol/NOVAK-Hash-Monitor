# Commands

## Launch

```bash
python serve.py
```

Custom port:

```bash
python serve.py --port 8080
```

## Reference-model demo

```bash
python tools/reference_estimator.py --demo
```

The demo uses built-in synthetic samples only.

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
node tests/test_browser_contract.mjs
```

## Contracts

```bash
python scripts/check_napp_contract.py
python scripts/check_surface_contract.py
python scripts/check_static_site.py
```

## Complete local gate

```bash
python scripts/quality_gate.py
```

## Write local proof receipt

```bash
python scripts/quality_gate.py --write-report reports/local-proof.json
```

## Git whitespace check from repository root

```bash
git diff --check
```

No command accepts or requires a real password.
