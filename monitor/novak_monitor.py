import argparse, os, hashlib, json, time

# ---------- Core Hash Helpers ----------

def sha256_file(path: str) -> str | None:
    """Return SHA-256 hex digest of a file, or None if unreadable."""
    try:
        with open(path, "rb") as f:
            h = hashlib.sha256()
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return None


def hash_dir(root: str) -> dict:
    """Recursively hash all files under root and return {path: digest}."""
    baseline = {}
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            full_path = os.path.join(dirpath, name)
            digest = sha256_file(full_path)
            if digest is not None:
                baseline[full_path] = digest
    return baseline


# ---------- Tamper-Evident Receipt Chain ----------

def load_last_eir_hash(chain_file: str) -> str | None:
    """Return eir_hash from the last line in the chain file, if any."""
    if not os.path.exists(chain_file):
        return None
    last = None
    with open(chain_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            last = line
    if not last:
        return None
    try:
        data = json.loads(last)
        return data.get("eir_hash")
    except json.JSONDecodeError:
        return None


def append_receipt(chain_file: str, file_path: str, file_hash: str | None, action: str) -> None:
    """Append a chained EIR-style receipt entry into a JSONL file."""
    prev_hash = load_last_eir_hash(chain_file)
    data = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "file": file_path,
        "hash": file_hash or "",
        "action": action,
        "prev_receipt_hash": prev_hash or "",
    }
    # Hash of all fields → eir_hash
    content = json.dumps(data, sort_keys=True).encode("utf-8")
    data["eir_hash"] = hashlib.sha256(content).hexdigest()

    with open(chain_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")


# ---------- Commands ----------

def cmd_baseline(args):
    """novak-monitor baseline ROOT -o baseline.json"""
    baseline = hash_dir(args.root)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2, sort_keys=True)
    print(f"✅ Baseline written to {args.output} ({len(baseline)} files)")


def cmd_check(args):
    """novak-monitor check ROOT -b baseline.json [--chain receipts.jsonl]"""
    with open(args.baseline, "r", encoding="utf-8") as f:
        baseline = json.load(f)
    current = hash_dir(args.root)

    baseline_paths = set(baseline.keys())
    current_paths = set(current.keys())

    missing = baseline_paths - current_paths
    new_files = current_paths - baseline_paths
    common = baseline_paths & current_paths

    print("🔍 Comparing against baseline...")

    for path in sorted(common):
        if baseline[path] != current[path]:
            print(f"⚠️  MODIFIED: {path}")
            if args.chain:
                append_receipt(args.chain, path, current[path], "modified")

    for path in sorted(new_files):
        print(f"➕ NEW: {path}")
        if args.chain:
            append_receipt(args.chain, path, current[path], "new")

    for path in sorted(missing):
        print(f"❌ MISSING: {path}")
        if args.chain:
            append_receipt(args.chain, path, None, "missing")

    print("✅ Check complete.")
    if args.chain:
        print(f"📜 Receipts appended to {args.chain}")


def cmd_watch(args):
    """novak-monitor watch PATH [--chain receipts.jsonl]"""
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        raise SystemExit("watchdog is not installed. Run: pip install watchdog")

    class NovakWatcher(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            digest = sha256_file(event.src_path)
            print(f"✏️  MODIFIED: {event.src_path} → {digest}")
            if args.chain:
                append_receipt(args.chain, event.src_path, digest, "modified")

        def on_created(self, event):
            if event.is_directory:
                return
            digest = sha256_file(event.src_path)
            print(f"➕ CREATED: {event.src_path} → {digest}")
            if args.chain:
                append_receipt(args.chain, event.src_path, digest, "new")

        def on_deleted(self, event):
            if event.is_directory:
                return
            print(f"🗑️  DELETED: {event.src_path}")
            if args.chain:
                append_receipt(args.chain, event.src_path, None, "deleted")

    observer = Observer()
    observer.schedule(NovakWatcher(), path=args.path, recursive=True)
    observer.start()
    print(f"👀 Watching {args.path} (recursive). Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


# ---------- CLI Wiring ----------

def build_parser():
    p = argparse.ArgumentParser(prog="novak-monitor", description="NOVAK Hash Monitor CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    # baseline
    b = sub.add_parser("baseline", help="Create a baseline hash set")
    b.add_argument("root", help="Root directory to hash, e.g. / or C:\\")
    b.add_argument("-o", "--output", default="baseline.json",
                   help="Baseline output file (default: baseline.json)")
    b.set_defaults(func=cmd_baseline)

    # check
    c = sub.add_parser("check", help="Check current hashes against baseline")
    c.add_argument("root", help="Root directory to scan")
    c.add_argument("-b", "--baseline", default="baseline.json",
                   help="Baseline file to compare against")
    c.add_argument("--chain", help="Optional receipt chain JSONL file")
    c.set_defaults(func=cmd_check)

    # watch
    w = sub.add_parser("watch", help="Watch a directory in real time")
    w.add_argument("path", help="Directory to watch")
    w.add_argument("--chain", help="Optional receipt chain JSONL file")
    w.set_defaults(func=cmd_watch)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
