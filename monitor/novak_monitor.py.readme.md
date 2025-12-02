# 1) Create baseline
python -m monitor.novak_monitor baseline / -o baseline.json

# 2) Check against baseline, write chained receipts
python -m monitor.novak_monitor check / -b baseline.json --chain receipts.jsonl

# 3) Watch a directory in real time (requires watchdog)
pip install watchdog
python -m monitor.novak_monitor watch /etc --chain receipts.jsonl
