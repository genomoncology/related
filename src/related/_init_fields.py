from attr import validators, NOTHING
from .validators import composite


def init_default(required, default, optional_default):
    """
    Returns optional default if field is not required and
    default was not provided.

    :param bool required: whether the field is required in a given model.
    :param default: default provided by creator of field.
    :param optional_default: default for the data type if none provided.
    :return: default or optional default based on inputs
    """
    if not required and default == NOTHING:
        default = optional_default

    return default


def init_validator(required, cls, *additional_validators):
    """
    Create an attrs validator based on the cls provided and required setting.
    :param bool required: whether the field is required in a given model.
    :param cls: the expected class type of object value.
    :return: attrs validator chained correctly (e.g. optional(instance_of))
    """
    validator = validators.instance_of(cls)

    if additional_validators:
        additional_validators = list(additional_validators)
        additional_validators.append(validator)
        validator = composite(*additional_validators)

    return validator if required else validators.optional(validator)
