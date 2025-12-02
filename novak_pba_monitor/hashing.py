import hashlib
from blake3 import blake3

def sha256_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()

def blake3_file(path):
    try:
        with open(path, "rb") as f:
            return blake3(f.read()).hexdigest()
    except:
        return None

def blake3_bytes(b):
    return blake3(b).hexdigest()
