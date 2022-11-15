import os
import sys
from pathlib import Path

import streamlit as st

from delve.defaults import default_installation_directory
from delve.search import handle_search_query
from delve.config import load_config
from delve.models import (
    # Event,
    # Tag,
    db,
    # bind_db,
)

installation_directory = Path(os.environ.get("DELVE_INSTALLATION_DIRECTORY", default_installation_directory))

@st.experimental_memo
def to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

st.markdown('<h1 style="text-align: center; padding: 0">Delve</h1>', unsafe_allow_html=True)
# st.markdown('<h3 style="text-align: center">Get your hands dirty...with data</h1>', unsafe_allow_html=True)

query = st.text_area("Search")

plugins_config = load_config("plugins", installation_directory)

database_config = load_config("database", installation_directory)
    
# bind_db(**database_config["bind"])
if "db" not in st.session_state:
    try:
        db.bind(**database_config["bind"])
        db.generate_mapping(create_tables=True)
    except:
        pass
    st.session_state["db"] = db

if query:
    df = handle_search_query(
        query,
        installation_directory=installation_directory,
        plugins_config=plugins_config,
    )

    st.write(df)