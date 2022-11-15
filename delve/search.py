import json
import shlex
from pathlib import Path
from inspect import isgenerator

from .config import get_cls_from_name
from .encoders import UUIDEncoder

def handle_search_query(
        query: str,
        installation_directory: Path,
        plugins_config: dict,
    ):
    query_parts = query.split("|")
    results = None
    for query_part in query_parts:
        argv = shlex.split(query_part)
        plugin_name = argv[0]
        plugin_cls_name = plugins_config.get("search").get(plugin_name)
        plugin = get_cls_from_name(plugin_cls_name)
        results = plugin(argv[1:], results)
    if isgenerator(results):
        return list(result for result in results) 
    return results