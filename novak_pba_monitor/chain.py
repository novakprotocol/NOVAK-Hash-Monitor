import json, hashlib

def append_eir(chain_file, eir_obj):
    prev_hash = None

    try:
        with open(chain_file) as f:
            for line in f:
                prev = json.loads(line)
                prev_hash = prev.get("chain_hash")
    except:
        pass

    content = json.dumps({
        "eir": eir_obj,
        "prev": prev_hash
    }, sort_keys=True).encode()

    chain_hash = hashlib.sha256(content).hexdigest()

    record = {
        "eir": eir_obj,
        "prev": prev_hash,
        "chain_hash": chain_hash
    }

    with open(chain_file, "a") as f:
        f.write(json.dumps(record) + "\n")

    return chain_hash
