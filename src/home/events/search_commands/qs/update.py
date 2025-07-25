# Copyright (C) 2025 All rights reserved.
# This file is part of the Delve project, which is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).
# See the LICENSE file in the root of this repository for details.

import logging
import argparse
from typing import Any, Dict, List

from django.db.models.query import QuerySet
from django.http import HttpRequest

from events.search_commands.decorators import search_command
from events.search_commands.util import has_permission_for_model

from ._util import parse_field_expressions, generate_keyword_args

update_parser = argparse.ArgumentParser(
    prog="update",
    description="Update the specified fields in the QuerySet",
)
update_parser.add_argument(
    "field_expressions",
    nargs="*",
    help="The fields to update",
)

@search_command(update_parser)
def update(request: HttpRequest, events: QuerySet, argv: List[str], environment: Dict[str, Any]) -> int:
    """
    Update the specified fields in the QuerySet.

    Args:
        request (HttpRequest): The HTTP request object.
        events (QuerySet): The QuerySet to operate on.
        argv (List[str]): List of command-line arguments.
        environment (Dict[str, Any]): Dictionary used as a jinja2 environment (context) for rendering the arguments of a command.

    Returns:
        int: The number of rows affected by the update.
    """
    log = logging.getLogger(__name__)
    log.info("In update")
    args = update_parser.parse_args(argv[1:])

    if not isinstance(events, QuerySet):
        log.critical(f"Type QuerySet expected, received {type(events)}")
        raise ValueError(
            f"update can only operate on QuerySets like "
            "the output of the search command"
        )
    model = events.query.model
    if not has_permission_for_model('change', model, request):
        raise PermissionError("Permission denied")
    
    log.debug(f"Received {args=}")
    parsed_expressions = parse_field_expressions(args.field_expressions)
    log.debug(f"Parsed expressions: {parsed_expressions}")
    positional_args, keyword_args = generate_keyword_args(parsed_expressions)
    log.debug(f"Generated positional_args: {positional_args}, keyword_args: {keyword_args}")
    return events.update(**keyword_args)
