import json
import logging
import argparse

import streamlit as st

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--field", default="text")
def extract_json(argv, results):
    log = logging.getLogger(__name__)
    args = parser.parse_args(argv)
    field = args.field
    for result in results:
        log.debug(f"Found result: {result[field]}")
        try:
            if isinstance(result[field], str):
                parsed = json.loads(result[field])
            elif isinstance(result[field], dict):
                parsed = result[field]
            else:
                raise ValueError(f"Unable to parse type: {type(result[field])}")
        except:
            # st.write(result["text"])
            yield result
            continue
        # st.write(result)
        if "extracted_fields" in result:
            result["extracted_fields"].update(parsed)
        else:
            result["extracted_fields"] = parsed
        # st.write(result)
        yield result
