from collections import OrderedDict
from uuid import UUID
from future.moves.urllib.parse import urlparse
from six import string_types, callable
from datetime import datetime
from inspect import isfunction
from dateutil import parser
from importlib import import_module

from .types import TypedSequence, TypedMapping, TypedSet
from .functions import to_model

CHILD_ERROR_MSG = "Failed to convert value ({}) to child object class ({}). " \
                  + "... [Original error message: {}]"


def to_child_field(cls):
    """
    Returns an callable instance that will convert a value to a Child object.

    :param cls: Valid class type of the Child.
    :return: instance of ChildConverter.
    """

    class ChildConverter(object):

        def __init__(self, cls):
            self._cls = cls

        @property
        def cls(self):
            return resolve_class(self._cls)

        def __call__(self, value):
            try:
                # Issue #33: if value is the class and callable, then invoke
                if value == self._cls and callable(value):
                    value = value()

                return to_model(self.cls, value)
            except ValueError as e:
                error_msg = CHILD_ERROR_MSG.format(value, self.cls, str(e))
                raise ValueError(error_msg)

    return ChildConverter(cls)


def to_sequence_field(cls):
    """
    Returns a callable instance that will convert a value to a Sequence.

    :param cls: Valid class type of the items in the Sequence.
    :return: instance of the SequenceConverter.
    """
    class SequenceConverter(object):

        def __init__(self, cls):
            self._cls = cls

        @property
        def cls(self):
            return resolve_class(self._cls)

        def __call__(self, values):
            values = values or []
            args = [to_model(self.cls, value) for value in values]
            return TypedSequence(cls=self.cls, args=args)

    return SequenceConverter(cls)


def to_set_field(cls):
    """
    Returns a callable instance that will convert a value to a Sequence.

    :param cls: Valid class type of the items in the Sequence.
    :return: instance of the SequenceConverter.
    """
    class SetConverter(object):

        def __init__(self, cls):
            self._cls = cls

        @property
        def cls(self):
            return resolve_class(self._cls)

        def __call__(self, values):
            values = values or set()
            args = {to_model(self.cls, value) for value in values}
            return TypedSet(cls=self.cls, args=args)

    return SetConverter(cls)


def to_mapping_field(cls, key):  # pragma: no mccabe
    """
    Returns a callable instance that will convert a value to a Mapping.

    :param cls: Valid class type of the items in the Sequence.
    :param key: Attribute name of the key value in each item of cls instance.
    :return: instance of the MappingConverter.
    """
    class MappingConverter(object):

        def __init__(self, cls, key):
            self._cls = cls
            self.key = key

        @property
        def cls(self):
            return resolve_class(self._cls)

        def __call__(self, values):
            kwargs = OrderedDict()

            if isinstance(values, TypedMapping):
                return values

            if not isinstance(values, (type({}), type(None))):
                raise TypeError("Invalid type : {}".format(type(values)))

            if values:
                for key_value, item in values.items():
                    if isinstance(item, dict):
                        item[self.key] = key_value
                        item = to_model(self.cls, item)
                    kwargs[key_value] = item

            return TypedMapping(cls=self.cls, kwargs=kwargs, key=self.key)

    return MappingConverter(cls, key)


def str_if_not_none(value):
    """
    Returns an str(value) if the value is not None.

    :param value: None or a value that can be converted to a str.
    :return: None or str(value)
    """
    if not(value is None or isinstance(value, string_types)):
        value = str(value)

    return value


def int_if_not_none(value):
    """
    Returns an int(value) if the value is not None.

    :param value: None or a value that can be converted to an int.
    :return: None or int(value)
    """
    return None if value is None else int(value)


def float_if_not_none(value):
    """
    Returns an float(value) if the value is not None.

    :param value: None or a value that can be converted to an float.
    :return: None or float(value)
    """
    return None if value is None else float(value)


def str_to_url(value):
    """
    Returns a UUID(value) if the value provided is a str.

    :param value: str or UUID object
    :return: UUID object
    """
    return urlparse(value) if isinstance(value, string_types) else value


def str_to_uuid(value):
    """
    Returns a UUID(value) if the value provided is a str.

    :param value: str or UUID object
    :return: UUID object
    """
    if isfunction(value):
        value = value()

    return UUID(value) if isinstance(value, string_types) else value


def to_date_field(formatter):
    """
    Returns a callable instance that will convert a string to a Date.

    :param formatter: String that represents data format for parsing.
    :return: instance of the DateConverter.
    """
    class DateConverter(object):

        def __init__(self, formatter):
            self.formatter = formatter

        def __call__(self, value):
            if isinstance(value, string_types):
                value = datetime.strptime(value, self.formatter).date()

            if isinstance(value, datetime):
                value = value.date()

            return value

    return DateConverter(formatter)


def to_datetime_field(formatter):
    """
    Returns a callable instance that will convert a string to a DateTime.

    :param formatter: String that represents data format for parsing.
    :return: instance of the DateTimeConverter.
    """
    class DateTimeConverter(object):

        def __init__(self, formatter):
            self.formatter = formatter

        def __call__(self, value):
            if isinstance(value, string_types):
                value = parser.parse(value)

            return value

    return DateTimeConverter(formatter)


def to_time_field(formatter):
    """
    Returns a callable instance that will convert a string to a Time.

    :param formatter: String that represents data format for parsing.
    :return: instance of the TimeConverter.
    """
    class TimeConverter(object):

        def __init__(self, formatter):
            self.formatter = formatter

        def __call__(self, value):
            if isinstance(value, string_types):
                value = datetime.strptime(value, self.formatter).time()

            return value

    return TimeConverter(formatter)


def resolve_class(cls):
    if isinstance(cls, str):
        module_name, model_name = cls.rsplit(".", 1)
        module = import_module(module_name)
        cls = getattr(module, model_name)
    return cls
