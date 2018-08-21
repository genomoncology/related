from __future__ import absolute_import, division, print_function

from collections import OrderedDict
from enum import Enum

import yaml
import json

from attr._make import fields

try:
    from functools import singledispatch
except ImportError:
    from singledispatch import singledispatch


@singledispatch
def to_dict(obj, **kwargs):
    """
    Convert an object into dictionary. Uses singledispatch to allow for
    clean extensions for custom class types.

    Reference: https://pypi.python.org/pypi/singledispatch

    :param obj: object instance
    :param kwargs: keyword arguments such as suppress_private_attr,
                   suppress_empty_values, dict_factory
    :return: converted dictionary.
    """

    # if is_related, then iterate attrs.
    if is_model(obj.__class__):
        return related_obj_to_dict(obj, **kwargs)

    # else, return obj directly. register a custom to_dict if you need to!
    #   reference: https://pypi.python.org/pypi/singledispatch
    else:
        return obj


def related_obj_to_dict(obj, **kwargs):
    """ Covert a known related object to a dictionary. """

    # Explicitly discard formatter kwarg, should not be cascaded down.
    kwargs.pop('formatter', None)

    # If True, remove fields that start with an underscore (e.g. _secret)
    suppress_private_attr = kwargs.get("suppress_private_attr", False)

    # if True, don't store fields with None values into dictionary.
    suppress_empty_values = kwargs.get("suppress_empty_values", False)

    # get list of attrs fields
    attrs = fields(obj.__class__)

    # instantiate return dict, use OrderedDict type by default
    return_dict = kwargs.get("dict_factory", OrderedDict)()

    for a in attrs:

        # skip if private attr and flag tells you to skip
        if suppress_private_attr and a.name.startswith("_"):
            continue

        metadata = a.metadata or {}

        # formatter is a related-specific `attrs` meta field
        #   see fields.DateField
        formatter = metadata.get('formatter')

        # get value and call to_dict on it, passing the kwargs/formatter
        value = getattr(obj, a.name)
        value = to_dict(value, formatter=formatter, **kwargs)

        # check flag, skip None values
        if suppress_empty_values and value is None:
            continue

        # field name can be overridden by the metadata field
        key_name = a.metadata.get('key') or a.name

        # store converted / formatted value into return dictionary
        return_dict[key_name] = value

    return return_dict


def to_model(cls, value):
    """
    Coerce a value into a model object based on a class-type (cls).
    :param cls: class type to coerce into
    :param value: value to be coerced
    :return: original value or coerced value (value')
    """

    if isinstance(value, cls) or value is None:
        pass  # skip if right type or value is None

    elif issubclass(cls, Enum):
        value = cls(value)

    elif is_model(cls) and isinstance(value, dict):
        value = convert_key_to_attr_names(cls, value)
        value = cls(**value)

    else:
        value = cls(value)

    return value


def convert_key_to_attr_names(cls, original):
    """ convert key names to their corresponding attribute names """
    attrs = fields(cls)
    updated = {}
    keys_pulled = set()

    for a in attrs:
        key_name = a.metadata.get('key') or a.name
        if key_name in original:
            updated[a.name] = original.get(key_name)
            keys_pulled.add(key_name)

    if getattr(cls, '__related_strict__', False):
        extra = set(original.keys()) - keys_pulled
        if len(extra):
            raise ValueError("Extra keys (strict mode): {}".format(extra))

    return updated


def is_model(cls):
    """
    Check whether *cls* is a class with ``attrs`` attributes.

    :param type cls: Class to introspect.
    :raise TypeError: If *cls* is not a class.

    :rtype: :class:`bool`
    """
    return getattr(cls, "__attrs_attrs__", None) is not None


def to_yaml(obj, stream=None, dumper_cls=yaml.Dumper, default_flow_style=False,
            **kwargs):
    """
    Serialize a Python object into a YAML stream with OrderedDict and
    default_flow_style defaulted to False.

    If stream is None, return the produced string instead.

    OrderedDict reference: http://stackoverflow.com/a/21912744
    default_flow_style reference: http://stackoverflow.com/a/18210750

    :param data: python object to be serialized
    :param stream: to be serialized to
    :param Dumper: base Dumper class to extend.
    :param kwargs: arguments to pass to to_dict
    :return: stream if provided, string if stream is None
    """

    class OrderedDumper(dumper_cls):
        pass

    def dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(OrderedDict, dict_representer)

    obj_dict = to_dict(obj, **kwargs)

    return yaml.dump(obj_dict, stream, OrderedDumper,
                     default_flow_style=default_flow_style)


def from_yaml(stream, cls=None, loader_cls=yaml.Loader,
              object_pairs_hook=OrderedDict, **extras):
    """
    Convert a YAML stream into a class via the OrderedLoader class.
    """

    class OrderedLoader(loader_cls):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    yaml_dict = yaml.load(stream, OrderedLoader) or {}
    yaml_dict.update(extras)
    return cls(**yaml_dict) if cls else yaml_dict


def to_json(obj, indent=4, sort_keys=True, **kwargs):
    """
    :param obj: object to convert to dictionary and then output to json
    :param indent: indent json by number of spaces
    :param sort_keys: sort json output by key if true
    :param kwargs: arguments to pass to to_dict
    :return: json string
    """
    obj_dict = to_dict(obj, **kwargs)
    return json.dumps(obj_dict, indent=indent, sort_keys=sort_keys)


def from_json(stream, cls=None, object_pairs_hook=OrderedDict, **extras):
    """
    Convert a JSON string or stream into specified class.
    """
    stream = stream.read() if hasattr(stream, 'read') else stream
    json_dict = json.loads(stream, object_pairs_hook=object_pairs_hook)
    if extras:
        json_dict.update(extras)  # pragma: no cover
    return to_model(cls, json_dict) if cls else json_dict
