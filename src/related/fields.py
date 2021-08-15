# -*- coding: utf-8 -*-
from decimal import Decimal
from future.moves.urllib.parse import ParseResult
from attr import attrib, NOTHING
from collections import OrderedDict
from uuid import uuid4, UUID
from datetime import date, datetime, time
from six import string_types

from . import _init_fields, types, converters, validators


def BooleanField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, kw_only: bool = False):
    """
    Create new bool field on a model.

    :param default: any boolean value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, bool)
    return attrib(default=default, validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def ChildField(cls, default=NOTHING, required=True, repr=True, cmp=True,
               key=None, kw_only: bool = False):
    """
    Create new child field on a model.

    :param cls: class (or name) of the model to be related.
    :param default: any object value of type cls
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    converter = converters.to_child_field(cls)
    validator = _init_fields.init_validator(
        required, object if isinstance(cls, str) else cls
    )
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp, metadata=dict(key=key), kw_only=kw_only)


def DateField(formatter=types.DEFAULT_DATE_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None, kw_only: bool = False):
    """
    Create new date field on a model.

    :param formatter: date formatter string (default: "%Y-%m-%d")
    :param default: any date or string that can be converted to a date value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, date)
    converter = converters.to_date_field(formatter)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key), kw_only=kw_only)


def DateTimeField(formatter=types.DEFAULT_DATETIME_FORMAT, default=NOTHING,
                  required=True, repr=True, cmp=True, key=None, kw_only: bool = False):
    """
    Create new datetime field on a model.

    :param formatter: datetime formatter string (default: "ISO_FORMAT")
    :param default: any datetime or string that can be converted to a datetime
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, datetime)
    converter = converters.to_datetime_field(formatter)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key), kw_only=kw_only)


def TimeField(formatter=types.DEFAULT_TIME_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None, kw_only: bool = False):
    """
    Create new time field on a model.

    :param formatter: time formatter string (default: "%H:%M:%S")
    :param default: any time or string that can be converted to a time value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, time)
    converter = converters.to_time_field(formatter)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key), kw_only=kw_only)


def FloatField(default=NOTHING, required=True, repr=True, cmp=True,
               key=None, kw_only: bool = False):
    """
    Create new float field on a model.

    :param default: any float value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, float)
    return attrib(default=default, converter=converters.float_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def IntegerField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, kw_only: bool = False):
    """
    Create new int field on a model.

    :param default: any integer value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, int)
    return attrib(default=default, converter=converters.int_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def MappingField(cls, child_key, default=NOTHING, required=True, repr=False,
                 key=None, kw_only: bool = False):
    """
    Create new mapping field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param child_key: key field on the child object to be used as the map key.
    :param default: any mapping type
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, OrderedDict())
    converter = converters.to_mapping_field(cls, child_key)
    validator = _init_fields.init_validator(required, types.TypedMapping)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=dict(key=key), kw_only=kw_only)


def RegexField(regex, default=NOTHING, required=True, repr=True, cmp=True,
               key=None, kw_only: bool = False):
    """
    Create new str field on a model.

    :param regex: regex validation string (e.g. "[^@]+@[^@]+" for email)
    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types,
                                            validators.regex(regex))
    return attrib(default=default, converter=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def SequenceField(cls, default=NOTHING, required=True, repr=False, key=None,
                  kw_only: bool = False):
    """
    Create new sequence field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param default: any TypedSequence or list
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, [])
    converter = converters.to_sequence_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSequence)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=dict(key=key), kw_only=kw_only)


def SetField(cls, default=NOTHING, required=True, repr=False, key=None,
             kw_only: bool = False):
    """
    Create new set field on a model.

    :param cls: class (or name) of the model to be related in Set.
    :param default: any TypedSet or set
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, set())
    converter = converters.to_set_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSet)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=dict(key=key), kw_only=kw_only)


def StringField(default=NOTHING, required=True, repr=True, cmp=True,
                key=None, kw_only: bool = False):
    """
    Create new str field on a model.

    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types)
    return attrib(default=default, converter=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def URLField(default=NOTHING, required=True, repr=True, cmp=True, key=None,
             kw_only: bool = False):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    cls = ParseResult
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, cls)
    return attrib(default=default, converter=converters.str_to_url,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def UUIDField(default=NOTHING, required=False, repr=True, cmp=True, key=None,
              kw_only: bool = False):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    cls = UUID
    default = _init_fields.init_default(required, default, uuid4)
    validator = _init_fields.init_validator(required, cls)
    return attrib(default=default, converter=converters.str_to_uuid,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)


def DecimalField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, kw_only: bool = False):
    """
    Create new decimal field on a model.

    :param default: any decimal value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param bool kw_only: have a generated __init__ with keyword-only arguments,
        relaxing the required ordering of default and non-default valued attributes.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, Decimal)
    return attrib(default=default, converter=lambda x: Decimal(x),
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), kw_only=kw_only)
