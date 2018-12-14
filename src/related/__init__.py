# -*- coding: utf-8 -*-

from .decorators import (
    mutable,
    immutable,
    serializer,
)

from .types import (
    ImmutableDict,
    TypedSequence,
    TypedMapping,
    TypedSet,
)

from .fields import (
    BooleanField,
    ChildField,
    DateField,
    DateTimeField,
    TimeField,
    FloatField,
    IntegerField,
    MappingField,
    RegexField,
    SequenceField,
    SetField,
    StringField,
    URLField,
    UUIDField,
    DecimalField,
)

from .functions import (
    from_json,
    from_yaml,
    is_model,
    to_dict,
    to_json,
    to_model,
    to_yaml,
)

from . import dispatchers  # noqa F401

__all__ = [
    # decorators.py
    "mutable",
    "immutable",
    "serializer",

    # types.py
    "ImmutableDict",
    "TypedSequence",
    "TypedMapping",
    "TypedSet",

    # fields.py
    "BooleanField",
    "ChildField",
    "DateField",
    "DateTimeField",
    "TimeField",
    "FloatField",
    "IntegerField",
    "MappingField",
    "RegexField",
    "SetField",
    "StringField",
    "SequenceField",
    "URLField",
    "UUIDField",
    "DecimalField",

    # functions.py
    "from_json",
    "from_yaml",
    "is_model",
    "to_dict",
    "to_json",
    "to_model",
    "to_yaml",
]


__author__ = """Ian Maurer"""
__email__ = 'ian@genomoncology.com'
__version__ = '0.7.2'

__uri__ = "http://www.github.com/genomoncology/related"
__copyright__ = "Copyright (c) 2017 genomoncology.com"
__description__ = "Related: Straightforward nested object models in Python"
__doc__ = __description__ + " <" + __uri__ + ">"
__license__ = "MIT"
__title__ = "related"
