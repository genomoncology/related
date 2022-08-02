from decimal import Decimal
from future.moves.urllib.parse import ParseResult
from collections import OrderedDict
from enum import Enum
from uuid import UUID
from datetime import date, datetime, time

from .functions import to_dict
from .types import (
    TypedSequence, TypedMapping, TypedSet, DEFAULT_DATE_FORMAT,
    DEFAULT_DATETIME_FORMAT, DEFAULT_TIME_FORMAT
)


@to_dict.register(list)  # noqa F811
@to_dict.register(set)
@to_dict.register(tuple)
def _(obj, **kwargs):
    suppress_empty_values = kwargs.get("suppress_empty_values", False)
    retain_collection_types = kwargs.get("retain_collection_types", False)

    if not suppress_empty_values or len(obj):
        cf = obj.__class__ if retain_collection_types else list
        return cf([to_dict(i, **kwargs) for i in obj])


@to_dict.register(dict)  # noqa F811
def _(obj, **kwargs):
    suppress_empty_values = kwargs.get("suppress_empty_values", False)
    dict_factory = kwargs.get("dict_factory", OrderedDict)

    items = []
    for kk, vv in obj.items():
        vv = to_dict(vv, **kwargs)
        if (not suppress_empty_values) or (vv is not None):
            items.append((to_dict(kk, **kwargs), vv))

    if not suppress_empty_values or len(items):
        return dict_factory(items)


@to_dict.register(TypedSequence)  # noqa F811
def _(obj, **kwargs):
    return to_dict(obj.list, **kwargs)


@to_dict.register(TypedSet)  # noqa F811
def _(obj, **kwargs):
    return to_dict(obj.set, **kwargs)


@to_dict.register(TypedMapping)  # noqa F811
def _(obj, **kwargs):
    suppress_map_key_values = kwargs.get("suppress_map_key_values", False)
    suppress_empty_values = kwargs.get("suppress_empty_values", False)
    rv = kwargs.get("dict_factory", OrderedDict)()

    items = obj.items()

    for key_value, item in items:
        sub_dict = to_dict(item, **kwargs)
        if suppress_map_key_values:
            sub_dict.pop(obj.key)
        rv[key_value] = sub_dict

    if not suppress_empty_values or len(items):
        return rv


@to_dict.register(Enum)  # noqa F811
def _(obj, **kwargs):
    return obj.value


@to_dict.register(UUID)  # noqa F811
def _(obj, **kwargs):
    return str(obj)


@to_dict.register(ParseResult)  # noqa F811
def _(obj, **kwargs):
    return obj.geturl()


@to_dict.register(date)  # noqa F811
def _(obj, **kwargs):
    formatter = kwargs.get('formatter') or DEFAULT_DATE_FORMAT
    return obj.strftime(formatter)


@to_dict.register(datetime)  # noqa F811
def _(obj, **kwargs):
    formatter = kwargs.get('formatter') or DEFAULT_DATETIME_FORMAT
    return (obj.isoformat() if formatter == "ISO_FORMAT"
            else obj.strftime(formatter))


@to_dict.register(time)  # noqa F811
def _(obj, **kwargs):
    formatter = kwargs.get('formatter') or DEFAULT_TIME_FORMAT
    return obj.strftime(formatter)


@to_dict.register(Decimal)  # noqa F811
def _(obj, **kwargs):
    return str(obj)
