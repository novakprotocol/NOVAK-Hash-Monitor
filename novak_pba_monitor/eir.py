import time
from .hvet import hvet

def build_eir(rule_hash, data_hash, output_hash, timestamp=None):
    if timestamp is None:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    hv = hvet(rule_hash, data_hash, output_hash, timestamp)

    return {
        "rule": rule_hash,
        "data": data_hash,
        "output": output_hash,
        "timestamp": timestamp,
        "hvet": hv
    }

def verify_eir(eir):
    expected = hvet(
        eir["rule"],
        eir["data"],
        eir["output"],
        eir["timestamp"]
    )
    return expected == eir["hvet"]
