from pathlib import Path
from importlib import import_module
import logging

import toml

def load_config(name: str, installation_directory: Path):
    log = logging.getLogger(__name__)
    config_directory =  installation_directory.joinpath("config")
    log.debug(f"Found config_directory: '{config_directory}'")
    config = config_directory.joinpath(f"{name}.toml")
    log.debug(f"Found config: '{config}'")
    ret = toml.loads(config.read_text())
    log.debug(f"Found parsed config: '{ret}'")
    return ret

def get_cls_from_name(name: str):
    log = logging.getLogger(__name__)
    parts = name.split(".")
    log.debug(f"Class name split on '.': '{parts}'.")
    module = import_module('.'.join(parts[:-1]))
    log.debug(F"Module found: '{module}'.")
    cls  = getattr(module, parts[-1])
    log.debug(f"Class found: '{cls}'")
    return cls

def get_module_from_name(name: str):
    log = logging.getLogger(__name__)
    parts = name.split(".")
    log.debug(f"Class name split on '.': '{parts}'.")
    module = import_module('.'.join(parts))
    return module