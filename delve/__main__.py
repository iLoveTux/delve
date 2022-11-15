import os
from pathlib import Path
import logging.config
import sys

from typer import Typer
import toml
from pony.orm import (
    Database,
    Required,
    db_session,
)

from  .defaults import (
    default_installation_directory,
    get_defaults,
)
from  .models import (
    Event,
    Tag,
    db,
)
from .config import load_config, get_module_from_name
from .inputs import handle_inputs
from .search import handle_search_query
from .apps import load_apps

cli = Typer()

@cli.command()
def startapp(
    name: str,
    installation_directory: Path=default_installation_directory,
):
    base_app_directory = installation_directory.joinpath("apps")
    app_directory = base_app_directory.joinpath(name)
    app_directory.mkdir()
    app_directory.joinpath("__init__.py").touch()
    app_directory.joinpath("inputs.py").write_text(
        "from delve import inputs\n"
        "\n"
        "# Put your input plugins below"
    )
    app_directory.joinpath("search.py").write_text(
        "from delve import search\n"
        "from argparse import ArgumentParser"
        "\n"
        "parser = ArgumentParser()"
        "\n"
        "# Put your search plugins below"
    )


@cli.command()
def install(
    installation_directory: Path=default_installation_directory,
):
    installation_directory.mkdir(parents=True, exist_ok=True)
    defaults = get_defaults(installation_directory=installation_directory)
    config_directory  = installation_directory.joinpath("config")
    config_directory.mkdir(parents=True, exist_ok=True)

    config_directory.joinpath("inputs.toml").write_text(toml.dumps(defaults["default_inputs_config"]))
    config_directory.joinpath("plugins.toml").write_text(toml.dumps(defaults["default_plugins_config"]))
    config_directory.joinpath("database.toml").write_text(toml.dumps(defaults["default_database_config"]))
    config_directory.joinpath("logging.toml").write_text(toml.dumps(defaults["default_logging_config"]))

    log_directory = installation_directory.joinpath("logs")
    log_directory.mkdir(parents=True, exist_ok=True)

    apps_directory = installation_directory.joinpath("apps")
    apps_directory.mkdir(parents=True, exist_ok=True)
    # apps_directory.joinpath("__init__.py").touch()
    
@cli.command()
def index(
    installation_directory: Path=default_installation_directory,
):
    apps_directory = installation_directory.joinpath("apps")
    sys.path.insert(0, apps_directory)
    logging_config =  load_config("logging", installation_directory)
    logging.config.dictConfig(logging_config)
    plugins_config = load_config("plugins", installation_directory)
    inputs_config = load_config("inputs", installation_directory)
    database_config = load_config("database", installation_directory)
    
    db.bind(**database_config["bind"])
    db.generate_mapping(create_tables=True)

    handler_map = plugins_config["input"]["handler_map"]
    
    handle_inputs(inputs_config, handler_map)

    return 0

@cli.command()
def search(
    query: str,
    installation_directory: Path=default_installation_directory,
):
    apps_directory = installation_directory.joinpath("apps")
    sys.path.insert(0, apps_directory)
    logging_config =  load_config("logging", installation_directory)
    logging.config.dictConfig(logging_config)
    plugins_config = load_config("plugins", installation_directory)
    database_config = load_config("database", installation_directory)
    
    db.bind(**database_config["bind"])
    db.generate_mapping(create_tables=False)

    handle_search_query(
        query=query,
        installation_directory=installation_directory,
        plugins_config=plugins_config,
    )
    return 0

@cli.command()
def serve(
    installation_directory: Path=default_installation_directory,
):
    from subprocess import run
    apps_directory = installation_directory.joinpath("apps")
    sys.path.insert(0, str(apps_directory))
    logging_config =  load_config("logging", installation_directory)
    logging.config.dictConfig(logging_config)
    plugins_config = load_config("plugins", installation_directory)
    database_config = load_config("database", installation_directory)

    log = logging.getLogger(__name__)

    # installed_apps = plugins_config["installed_apps"]
    # installed_apps = {
    #     name: Path(get_module_from_name(name).__file__).parent
    #     for name in installed_apps
    # }
    # dashboards = {}
    # for app_name, directory in installed_apps.items():
    #     log.debug(f"Found directory: {directory}")
    #     for path in directory.joinpath("dashboards").glob("*.py"):
    #         log.debug(f"Found path: {path}")
    #         if path.name.startswith("_"):
    #             continue
    #         log.debug(f"Found dashboard: {path}")
    #         _name = path.name.replace(".py", "")
    #         dashboards[".".join((app_name.split(".")[-1], _name))] = path.resolve()  # ".".join((app_name, _name)) 

    # default_dashboard = plugins_config["default_dashboard"]
    # default_dashboard = dashboards[default_dashboard]

    os.environ["DELVE_INSTALLATION_DIRECTORY"] = str(installation_directory.resolve())

    run(
        [
            "streamlit",
            "run",
            Path(__file__).parent.joinpath("shim.py"),
        ]
    )
    

    # with st.sidebar:
    #     selected_dashboard = st.selectbox(
    #         "Select Dashboard",
    #         dashboards,
    #     )
    # st.write(selected_dashboard)


if __name__ == "__main__":
    sys.exit(cli())
