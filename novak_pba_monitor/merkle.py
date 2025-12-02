import hashlib, json

def merkle_root(items):
    if not items:
        return None
    level = [hashlib.sha256(json.dumps(i).encode()).hexdigest() for i in items]
    while len(level) > 1:
        next_level = []
        for a, b in zip(level[0::2], level[1::2]):
            combined = hashlib.sha256((a + b).encode()).hexdigest()
            next_level.append(combined)
        if len(level) % 2 == 1:
            next_level.append(level[-1])
        level = next_level
    return level[0]
