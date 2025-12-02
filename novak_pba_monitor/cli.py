import argparse, os, json
from .hashing import sha256_file
from .eir import build_eir
from .watch import watch_path
from .chain import append_eir
from .verify import verify_chain
from .gate import gate_action

def baseline(path, output):
    result = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            full = os.path.join(root, f)
            digest = sha256_file(full)
            if digest:
                result[full] = digest
    with open(output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Baseline written: {output}")

def verify(path, baseline_file):
    with open(baseline_file) as f:
        base = json.load(f)

    current = {}
    for root, dirs, files in os.walk(path):
        for f in files:
            full = os.path.join(root, f)
            digest = sha256_file(full)
            if digest:
                current[full] = digest

    for f, dig in base.items():
        now = current.get(f)
        if now != dig:
            print(f"CHANGED: {f}")

def gate(rule, data, output, chain_file):
    def dummy_action():
        print("Action executed under NOVAK Gate.")
        return True
    gate_action(rule, data, output, chain_file, dummy_action)

def run():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    b = sub.add_parser("baseline")
    b.add_argument("path")
    b.add_argument("-o", "--output", default="baseline.json")

    w = sub.add_parser("watch")
    w.add_argument("path")
    w.add_argument("--chain", default="chain.jsonl")
    w.add_argument("--rule", required=True)

    v = sub.add_parser("verify")
    v.add_argument("path")
    v.add_argument("--baseline", default="baseline.json")

    g = sub.add_parser("gate")
    g.add_argument("--rule", required=True)
    g.add_argument("--data", required=True)
    g.add_argument("--output", required=True)
    g.add_argument("--chain", default="chain.jsonl")

    args = p.parse_args()

    if args.cmd == "baseline":
        baseline(args.path, args.output)

    elif args.cmd == "watch":
        watch_path(args.path, args.chain, args.rule)

    elif args.cmd == "verify":
        verify(args.path, args.baseline)

    elif args.cmd == "gate":
        gate(args.rule, args.data, args.output, args.chain)
