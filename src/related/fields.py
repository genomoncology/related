# -*- coding: utf-8 -*-
from decimal import Decimal
from future.moves.urllib.parse import ParseResult
from attr import attrib, NOTHING
from collections import OrderedDict
from uuid import uuid4, UUID
from datetime import date, datetime, time
from six import string_types, PY2

from . import _init_fields, types, converters, validators


attrib_additional_kwargs = {} if PY2 else {'kw_only': True}


def BooleanField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None):
    """
    Create new bool field on a model.

    :param default: any boolean value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, bool)
    return attrib(default=default, validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def ChildField(cls, default=NOTHING, required=True, repr=True, cmp=True,
               key=None):
    """
    Create new child field on a model.

    :param cls: class (or name) of the model to be related.
    :param default: any object value of type cls
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    converter = converters.to_child_field(cls)
    validator = _init_fields.init_validator(
        required, object if isinstance(cls, str) else cls
    )
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, cmp=cmp, metadata=dict(key=key),
                  **attrib_additional_kwargs)


def DateField(formatter=types.DEFAULT_DATE_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None):
    """
    Create new date field on a model.

    :param default: any date or string that can be converted to a date value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, date)
    converter = converters.to_date_field(formatter)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key),
                  **attrib_additional_kwargs)


def DateTimeField(formatter=types.DEFAULT_DATETIME_FORMAT, default=NOTHING,
                  required=True, repr=True, cmp=True, key=None):
    """
    Create new datetime field on a model.

    :param default: any datetime or string that can be converted to a datetime
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, datetime)
    converter = converters.to_datetime_field(formatter)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key),
                  **attrib_additional_kwargs)


def TimeField(formatter=types.DEFAULT_TIME_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None):
    """
    Create new time field on a model.

    :param default: any time or string that can be converted to a time value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, time)
    converter = converters.to_time_field(formatter)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=dict(formatter=formatter, key=key),
                  **attrib_additional_kwargs)


def FloatField(default=NOTHING, required=True, repr=True, cmp=True,
               key=None):
    """
    Create new float field on a model.

    :param default: any float value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, float)
    return attrib(default=default, convert=converters.float_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def IntegerField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None):
    """
    Create new int field on a model.

    :param default: any integer value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, int)
    return attrib(default=default, convert=converters.int_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def MappingField(cls, child_key, default=NOTHING, required=True, repr=False,
                 key=None):
    """
    Create new mapping field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param key: key field on the child object to be used as the mapping key.
    :param default: any mappingtype
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, OrderedDict())
    converter = converters.to_mapping_field(cls, child_key)
    validator = _init_fields.init_validator(required, types.TypedMapping)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, metadata=dict(key=key),
                  **attrib_additional_kwargs)


def RegexField(regex, default=NOTHING, required=True, repr=True, cmp=True,
               key=None):
    """
    Create new str field on a model.

    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types,
                                            validators.regex(regex))
    return attrib(default=default, convert=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def SequenceField(cls, default=NOTHING, required=True, repr=False, key=None):
    """
    Create new sequence field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param default: any TypedSequence or list
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, [])
    converter = converters.to_sequence_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSequence)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, metadata=dict(key=key),
                  **attrib_additional_kwargs)


def SetField(cls, default=NOTHING, required=True, repr=False, key=None):
    """
    Create new set field on a model.

    :param cls: class (or name) of the model to be related in Set.
    :param default: any TypedSet or set
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, set())
    converter = converters.to_set_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSet)
    return attrib(default=default, convert=converter, validator=validator,
                  repr=repr, metadata=dict(key=key),
                  **attrib_additional_kwargs)


def StringField(default=NOTHING, required=True, repr=True, cmp=True,
                key=None):
    """
    Create new str field on a model.

    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types)
    return attrib(default=default, convert=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def URLField(default=NOTHING, required=False, repr=True, cmp=True, key=None):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    cls = ParseResult
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, cls)
    return attrib(default=default, convert=converters.str_to_url,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def UUIDField(default=NOTHING, required=False, repr=True, cmp=True, key=None):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    cls = UUID
    default = _init_fields.init_default(required, default, uuid4)
    validator = _init_fields.init_validator(required, cls)
    return attrib(default=default, convert=converters.str_to_uuid,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)


def DecimalField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None):
    """
    Create new decimal field on a model.

    :param default: any decimal value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, Decimal)
    return attrib(default=default, convert=lambda x: Decimal(x),
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=dict(key=key), **attrib_additional_kwargs)
