# ✅ Real-time OS-Level File Watching (via watchdog)
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib, os

class NovakWatcher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory: return
        with open(event.src_path, 'rb') as f:
            h = hashlib.sha256(f.read()).hexdigest()
        print(f"🔍 File Changed: {event.src_path} → {h}")
        # Optional: call EIR generator or logger

observer = Observer()
observer.schedule(NovakWatcher(), path="/path/to/watch", recursive=True)
observer.start()
