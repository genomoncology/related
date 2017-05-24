from attr import attrs


def mutable(maybe_cls=None):

    def wrap(cls):
        return attrs(cls)

    return wrap(maybe_cls) if maybe_cls is not None else wrap


def immutable(maybe_cls=None):

    def wrap(cls):
        return attrs(cls, frozen=True, slots=True)

    return wrap(maybe_cls) if maybe_cls is not None else wrap
