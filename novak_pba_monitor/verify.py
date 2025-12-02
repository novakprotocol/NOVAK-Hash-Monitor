import json
from .eir import verify_eir

def verify_chain(chain_file):
    with open(chain_file) as f:
        for line in f:
            rec = json.loads(line)
            if not verify_eir(rec["eir"]):
                return False
    return True
