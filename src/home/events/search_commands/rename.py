# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

import argparse
from typing import Any, Dict, List, Union

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.util import resolve
from .decorators import search_command

parser = argparse.ArgumentParser(
    prog="rename",
    description="Rename a field.",
)
parser.add_argument(
    "-f",
    "--from-field",
    help="The field to rename from",
)
parser.add_argument(
    "-t",
    "--to-field",
    help="The field to rename to",
)

@search_command(parser)
def rename(request: HttpRequest, events: Union[QuerySet, List[Dict[str, Any]]], argv: List[str], environment: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Rename a field.

    Args:
        request (HttpRequest): The HTTP request object.
        events (Union[QuerySet, List[Dict[str, Any]]]): The result set to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries with the specified field renamed.
    """
    events = resolve(events)
    args = rename.parser.parse_args(argv[1:])
    for event in events:
        event[args.to_field] = event.pop(args.from_field)
        yield event
