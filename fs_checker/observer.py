import time
import json

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app import get_user_input


class CustomEncoder(json.JSONEncoder):
    def encode(self, obj):
        if isinstance(obj, dict):
            return '{\n' + ','.join(f'"{k}":{self.encode(v)}' for k, v in obj.items()) + '}\n'
        elif isinstance(obj, list):
            return '[' + ','.join(f'"{item}"' if isinstance(item, str) else str(item) for item in obj) + ']\n'
        elif isinstance(obj, str):
            return f'"{obj}"'
        else:
            return json.JSONEncoder.encode(self, obj)

    def iterencode(self, obj, _one_shot=False):
        return self.encode(obj)

class DirectoryEventHandler(FileSystemEventHandler):
    def __init__(self, notice_method):
        self.notice_method = notice_method
    
    def on_created(self, event):
        self.notice_method(event.src_path, event.dest_path)
    
class FileSystemWatcher:
    def __init__(self):
        self.observer = Observer()
        self.observer.schedule(DirectoryEventHandler(self.get_interface), "./images/", recursive=True)
        self.observer.start()

    def get_interface(self, src_path, dest_path):
        tags = ["<start>", *get_user_input(), "<end>"]
        print(tags)
        with open("./images/descriptions.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        with open("./images/descriptions.json", "w", encoding="utf-8") as file:
            data[src_path.split("/")[-1].split(".")[0]] = tags
            file.seek(0)
            json.dump(data, file, cls=CustomEncoder, indent=4)

    def __del__(self):
        self.observer.stop()
        self.observer.join()

watcher = FileSystemWatcher()

while True:
    time.sleep(1)