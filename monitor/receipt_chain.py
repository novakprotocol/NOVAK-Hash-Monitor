# ✅ Tamper-Evident Receipt Chain (SHA-linked)
import hashlib, json, time

chain = []

def add_receipt(file_path, file_hash, prev_hash=None):
    data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "file": file_path,
        "hash": file_hash,
        "prev_receipt_hash": prev_hash or "",
    }
    content = json.dumps(data, sort_keys=True).encode()
    data["eir_hash"] = hashlib.sha256(content).hexdigest()
    return data

# Example use:
chain.append(add_receipt("/etc/passwd", "abc123"))
chain.append(add_receipt("/etc/hosts", "def456", chain[-1]["eir_hash"]))

with open('receipt_chain.jsonl', 'w') as out:
    for item in chain:
        out.write(json.dumps(item) + "\n")
