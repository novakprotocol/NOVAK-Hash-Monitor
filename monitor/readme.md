# NOVAK Monitor Engine (Python Core)

### ✅ watcher.py
Real-time OS-level file change monitor using `watchdog`.

### ✅ fullscan.py
Hashes all files recursively and stores as `baseline.json`.

### ✅ receipt_chain.py
Links EIR receipts cryptographically for tamper detection.

### ✅ novak_monitor.py

  1) Create baseline
  python -m monitor.novak_monitor baseline / -o baseline.json

  2) Check against baseline, write chained receipts
  python -m monitor.novak_monitor check / -b baseline.json --chain receipts.jsonl

  3) Watch a directory in real time (requires watchdog)
  pip install watchdog python -m monitor.novak_monitor watch /etc --chain receipts.jsonl

### 💡 Tip:
Use these with CLI or daemon. Not browser-based.
