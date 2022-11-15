import argparse
import logging
import operator
import sys
import re
from functools import partial

from pony.orm import (
    db_session,
    count,
    select,
)

from delve.models import (
    Event,
    Tag,
    db,
)


def lenient_getattrs(item, field):
    log = logging.getLogger(__name__)
    log.debug(f"Entering lenient_getattr args: {item}, {field}")
    parts = field.split(".")
    log.debug(f"Found parts: '{parts}'")
    ret = item
    log.debug(f"Found ret: '{ret}'")
    for part in  parts:
        try:
            ret = getattr(ret, part)
            log.debug(f"Found ret: '{ret}'")
        except AttributeError:
            try:
                ret = ret[part]
                log.debug(f"Found ret: 'ret'")
            except KeyError:
                log.debug(f"Field '{part}' not found in '{ret}'.")
                ret = None
    log.debug(f"Found final return value: '{ret}'")
    return ret


def get_field_name(field):
    log = logging.getLogger(__name__)
    _field = "e"
    # __field = "Event"
    parts = field.split(".")
    log.debug(f"Found parts: '{parts}'")
    if parts[0] == "extracted_fields":
        # Would be nice to auto-detect JSON fields. but for now,  go with the one we know about
        log.debug(f"Examining extracted_fields: '{parts}'")
        _field += ".extracted_fields"
        # __field += ".extracted_fields"
        for part in parts[1:]:
            log.debug(f"Found part: '{part}'")
            _field += f"['{part}']"
            # __field += f"['{part}']"
    else:
        for part in parts:
            _field += f".{part}"
            # __field += f".{part}"
    log.debug(f"Found field name: '{_field}'")
    # print(eval(__field).py_type)
    return _field

def parse_filter_expression(expression, resolve_field_name=True):
    log = logging.getLogger(__name__)
    match = re.match("^(?P<field>(\w+\.?)+)(?P<op>[><=!~]{1,3})(?P<value>.*?)$", expression)
    if not match:
        log.error(f"Cannot parse filter expression: '{expression}'")
        sys.exit(2)
    field_expression = match.groupdict()["field"]
    op = match.groupdict()["op"]
    value = match.groupdict()["value"]
    log.debug(f"Parsed filter expression: field: '{field_expression}', operator: '{op}', value: '{value}'")
    if resolve_field_name:
        field_name = get_field_name(field_expression)
    else:
        field_name = field_expression
    return field_name, op, value

def should_include(result, _filters):
    include = True
    for _filter in _filters:
        field_name, op, value = parse_filter_expression(_filter, resolve_field_name=False)
        # field_name = field_name.replace("e.", "", 1)
        # value = result
        # for part in field_name.split("."):
        _value = lenient_getattrs(result, field_name)
        if _value is None:
            include = False
            break
        _cls = type(_value)
        # import streamlit as st; st.write(f"{value}: {_value}")
        match op:
            case "==":
                if _cls(value) == _value:
                    pass
                else:
                    include = False
                    break
            case "~=":
                if _value.startswith(_cls(value)):
                    pass
                else:
                    include = False
                    break
            case "=~":
                if _value.endswith(_cls(value)):
                    pass
                else:
                    include = False
                    break
            case "~=~":
                if _cls(value) in _value:
                    pass
                else:
                    include = False
                    break
            case "!=":
                if _cls(value) != _value:
                    pass
                else:
                    include = False
                    break
            case ">":
                if _value > _cls(value):
                    pass
                else:
                    include = False
                    break
            case ">=":
                if _value >= _cls(value):
                    pass
                else:
                    include = False
                    break
            case "<":
                if _value < _cls(value):
                    pass
                else:
                    include = False
                    break
            case "<=":
                if _value <= _cls(value):
                    pass
                else:
                    include = False
                    break
    return include

parser = argparse.ArgumentParser()
parser.add_argument("filters", nargs="*")
parser.add_argument("-s", "--sort", action="append")
parser.add_argument("-p", "--page", type=int, default=None)
parser.add_argument("-S", "--page-size", type=int, default=50)
def search(argv, results=None):
    log = logging.getLogger(__name__)
    log.debug(f"Found argv: '{argv}'")
    args = parser.parse_args(argv)
    log.debug(f"Found args: '{args}'")
    if results is not None:
        ret = []
        for result in results:
            if should_include(result, args.filters):
                ret.append(result)
        return ret
    else:
        with db_session():
            query = select(event for event in Event)
            if args.sort:
                for sort_field  in args.sort:
                    field_name = get_field_name(sort_field)
                    query = query.order_by(f"lambda e: {field_name}")
            if args.filters:
                for _filter in args.filters:
                    log.debug(f"Found args.filter: '{_filter}'")
                    field_name, op, value = parse_filter_expression(_filter)
                    if op == "==":
                        # Equality
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} == '{value}'")
                        query = query.filter(f"lambda e: {field_name} == '{value}'")
                    elif op == "~=":
                        # startswith
                        log.debug(f"Lambda Expression Build: lambda e: {field_name}.startswith('{value}')")
                        query = query.filter(f"lambda e: {field_name}.startswith('{value}')")
                    elif op == "=~":
                        # endswith
                        log.debug(f"Lambda Expression Build: lambda e: {field_name}.endswith('{value}')")
                        query = query.filter(f"lambda e: {field_name}.endswith('{value}')")
                    elif op == "~=~":
                        # Contains
                        log.debug(f"Lambda Expression Build: lambda e: '{value}' in {field_name}")
                        query = query.filter(f"lambda e: '{value}' in {field_name}")
                    elif op == "!=":
                        # Non-Equality
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} != '{value}'")
                        query = query.filter(f"lambda e: {field_name} != '{value}'")
                    elif op == ">=":
                        # Greater than or equal
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} >= '{value}'")
                        query = query.filter(f"lambda e: {field_name} >= '{value}'")
                    elif op == "<=":
                        # Less than or Equal to
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} <= '{value}'")
                        query = query.filter(f"lambda e: {field_name} <= '{value}'")
                    elif op == ">":
                        # Greater than
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} > '{value}'")
                        query = query.filter(f"lambda e: {field_name} > '{value}'")
                    elif op == "<":
                        # Less than
                        log.debug(f"Lambda Expression Build: lambda e: {field_name} < '{value}'")
                        query = query.filter(f"lambda e: {field_name} < '{value}'")

        # if args.host:
        #     log.debug(f"Found args.host: '{args.host}'")
        #     query = query.filter(lambda r: r.host==args.host)
        # if args.source:
        #     log.debug(f"Found args.source: '{args.source}'")
        #     query = query.filter(lambda r: r.source==args.source)
        # if args.sourcetype:
        #     log.debug(f"Found args.sourcetype: '{args.sourcetype}'")
        #     query = query.filter(lambda r: r.sourcetype==args.sourcetype)

            if args.page:
                query = query.page(args.page, pagesize=args.page_size)
            results = list(result.to_dict() for result in query)
    return results