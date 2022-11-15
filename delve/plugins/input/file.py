from urllib.parse import urlparse
from pathlib import Path

class FileInputHandler():
    def __init__(self, parsed_name: urlparse, conf: dict):
        print(parsed_name)
        self.conf = conf
        self.scheme = parsed_name.scheme
        self.netloc = parsed_name.netloc
        self.path = parsed_name.path
        self.obj = open(Path(self.path), "r")
        self.params = parsed_name.params
        self.query = parsed_name.query
        self.fragment = parsed_name.fragment
        
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.obj)
