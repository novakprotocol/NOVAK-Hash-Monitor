# ✅ Full-Disk Hashing Baseline & Verification
import os, hashlib, json

def hash_dir(root):
    baseline = {}
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            try:
                full_path = os.path.join(dirpath, f)
                with open(full_path, 'rb') as file:
                    content = file.read()
                    digest = hashlib.sha256(content).hexdigest()
                    baseline[full_path] = digest
            except Exception:
                continue
    return baseline

# Save to file
baseline = hash_dir('/')
with open('baseline.json', 'w') as out:
    json.dump(baseline, out, indent=2)
