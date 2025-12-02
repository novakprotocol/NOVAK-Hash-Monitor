from .eir import verify_eir, build_eir
from .chain import append_eir

def gate_action(rule_hash, data_hash, output_hash, chain_file, action_func):
    eir = build_eir(rule_hash, data_hash, output_hash)

    if not verify_eir(eir):
        raise Exception("NOVAK Gate: Integrity check failed. Action forbidden.")

    append_eir(chain_file, eir)

    return action_func()
