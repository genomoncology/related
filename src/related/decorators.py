from attr import attrs


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
