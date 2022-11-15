import logging
from urllib.parse import urlparse

from pony.orm import db_session

from .models import (
    Event,
    Tag,
)
from .config import get_cls_from_name

def handle_inputs(config: dict, handler_map: dict):
    log = logging.getLogger(__name__)
    log.debug(f"Found config: '{config}'")
    print(handler_map)
    log.debug(f"Found handler_map: '{handler_map}'")
    
    inputs = {}
    for name, conf in config.items():
        log.debug(f"Found name: '{name}', conf: '{conf}'")
        if name in inputs:
            raise ValueError(f"Duplicate input: '{name}'")
        parsed_name = urlparse(name)
        log.debug(f"Found parsed_name: '{parsed_name}'")

        handler_cls_name = handler_map.get(parsed_name.scheme, None)
        if handler_cls_name is None:
            raise ValueError(f"No handler found for {parsed_name.proto}")
        log.debug(f"Found handler_cls_name: '{handler_cls_name}'")
        handler_cls = get_cls_from_name(handler_cls_name)
        log.debug(f"Found handler_cls: '{handler_cls}'")

        tag_names = conf.get("tags")
        log.debug(f"Found tag_names: '{tag_names}'")

        extractions = conf.get("extractions")
        extractions = [get_cls_from_name(extraction) for extraction in extractions]
        # tags = []
        with db_session():
            for tag_name in tag_names:
                log.debug(f"Found tag_name: '{tag_name}'")
                tag = Tag.get(name=tag_name)
                if tag is None:
                    log.debug(f"Tag '{tag_name}' does not exist. Creating.")
                    tag = Tag(name=tag_name)
                # tags.append(tag)
        inputs[name] = (handler_cls(parsed_name, conf), tag_names, extractions)
        log.debug(f"Found input: '{name}': '{inputs[name]}'")

    while inputs:
        for name, (handler, tag_names, extractions) in inputs.copy().items():
            log.debug(f"Polling for event from input '{name}': '{handler}'")
            try:
                event = next(handler)
                event = event.strip()
                log.debug(f"Found event: '{event}'")
            except StopIteration:
                log.info(f"Input '{name}' has stopped producing events. (It raised a StopIteration Exception). Removing input.")
                del inputs[name]
            if not event:
                continue
            extracted_fields = {}
            for extraction in extractions:
                extracted_fields.update(extraction(event))
            with db_session():
                tags = [Tag.get(name=tag_name) for tag_name in tag_names]
                e = Event(
                    raw=event,
                    text=event,
                    index=handler.conf.get("index"),
                    host=handler.conf.get("host"),
                    source=handler.conf.get("source"),
                    sourcetype=handler.conf.get("sourcetype"),
                    extracted_fields=extracted_fields,
                    tags=tags,
                )
