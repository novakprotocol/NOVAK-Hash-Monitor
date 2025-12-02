import json
from .hashing import sha256_bytes

def canonical(obj):
    return json.dumps(obj, separators=(",", ":"), sort_keys=True).encode()

def hvet(rule_hash, data_hash, output_hash, timestamp):
    inner = canonical({
        "rule": rule_hash,
        "data": data_hash,
        "output": output_hash,
        "timestamp": timestamp
    })
    return sha256_bytes(inner)
