import inspect

from attr import attrs

from .functions import to_model, to_dict, is_model


def mutable(maybe_cls=None, strict=False):

    def wrap(cls):
        wrapped = attrs(cls)
        wrapped.__related_strict__ = strict
        return wrapped

    return wrap(maybe_cls) if maybe_cls is not None else wrap


def immutable(maybe_cls=None, strict=False):

    def wrap(cls):
        wrapped = attrs(cls, frozen=True, slots=True)
        wrapped.__related_strict__ = strict
        return wrapped

    return wrap(maybe_cls) if maybe_cls is not None else wrap


def _get_annotation_map(func, **kwargs):
    annotation_map = kwargs.copy()

    try:
        func_sig = inspect.signature(func)
        for index, arg in enumerate(func_sig.parameters.values()):
            if is_model(arg.annotation):
                annotation_map[arg.name] = arg.annotation
    except AttributeError:
        pass

    return annotation_map


def serializer(func=None, **kwargs):

    def _serializer(func):
        # collect map of related models by name (currently not arg index)
        annotation_map = _get_annotation_map(func, **kwargs)

        def wrapper(*args, **kwargs):
            # iterate keys that intersect
            for key in (set(kwargs.keys()) & set(annotation_map.keys())):
                kwargs[key] = to_model(annotation_map[key], kwargs[key])

            # run function getting result
            result = func(*args, **kwargs)

            # return
            return to_dict(result)

        return wrapper

    return _serializer(func) if func is not None else _serializer
