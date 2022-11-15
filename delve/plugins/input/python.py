from urllib.parse import urlparse
from delve.config import get_cls_from_name

class PythonInputHandler():
    def __init__(self, parsed_name: urlparse, conf: dict):
        self.conf = conf
        self.scheme = parsed_name.scheme
        self.netloc = parsed_name.netloc
        self.obj = get_cls_from_name(self.netloc)
        self.path = parsed_name.path
        self.params = parsed_name.params
        self.query = parsed_name.query
        self.fragment = parsed_name.fragment
        
    def __iter__(self):
        return self
    
    def __next__(self):
        return next(self.obj)
