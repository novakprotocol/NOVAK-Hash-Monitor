import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .hashing import sha256_file
from .eir import build_eir
from .chain import append_eir

class NovakWatcher(FileSystemEventHandler):
    def __init__(self, chain_file, rule_hash):
        self.chain_file = chain_file
        self.rule_hash = rule_hash

    def handle(self, event, action):
        digest = sha256_file(event.src_path)
        eir = build_eir(self.rule_hash, digest, digest)
        append_eir(self.chain_file, eir)
        print(f"{action}: {event.src_path} → {digest}")

    def on_modified(self, event):
        if not event.is_directory:
            self.handle(event, "MODIFIED")

    def on_created(self, event):
        if not event.is_directory:
            self.handle(event, "CREATED")

    def on_deleted(self, event):
        if not event.is_directory:
            self.handle(event, "DELETED")

def watch_path(path, chain_file, rule_hash):
    observer = Observer()
    observer.schedule(NovakWatcher(chain_file, rule_hash), path, recursive=True)
    observer.start()
    print(f"Watching {path}… (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
