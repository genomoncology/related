# -*- coding: utf-8 -*-
from attr.exceptions import FrozenInstanceError
from collections import OrderedDict

try:
    from collections.abc import (MutableSequence, MutableMapping, MutableSet)
except ImportError:
    from collections import (MutableSequence, MutableMapping, MutableSet)


DEFAULT_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_DATETIME_FORMAT = "ISO_FORMAT"
DEFAULT_TIME_FORMAT = "%H:%M:%S"


class ImmutableDict(dict):

    def __setitem__(self, key, value):
        raise FrozenInstanceError()

    def __delitem__(self, key):
        raise FrozenInstanceError()

    def __setattr__(self, name, value):
        raise FrozenInstanceError()

    def __delattr__(self, name):
        raise FrozenInstanceError()

    def pop(self, key, **kwargs):
        raise FrozenInstanceError()

    def clear(self):
        raise FrozenInstanceError()


class TypedSequence(MutableSequence):
    """
    Custom list type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """

    def __init__(self, cls, args, allow_none=True):
        self.cls = cls
        self.allowed_types = (cls, type(None)) if allow_none else cls
        self.list = []
        self.extend(args)

    def __str__(self):
        return str(self.list)

    def __repr__(self):
        return repr(self.list)

    def __len__(self):
        return len(self.list)

    def __eq__(self, other):
        if isinstance(other, TypedSequence):
            return self.list == other.list and self.cls == other.cls
        else:
            return self.list == other

    def __getitem__(self, i):
        return self.list[i]

    def __delitem__(self, i):
        del self.list[i]

    def __setitem__(self, i, v):
        self._check(v)
        self.list[i] = v

    def insert(self, i, v):
        self._check(v)
        self.list.insert(i, v)

    def _check(self, v):
        if not isinstance(v, self.allowed_types):
            raise TypeError("Invalid value %s (%s != %s)" %
                            (v, type(v), self.cls))


class TypedMapping(MutableMapping):
    """
    Custom dict type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """

    def __init__(self, cls, kwargs, key=None, allow_none=True):
        self.cls = cls
        self.allowed_types = (cls, type(None)) if allow_none else cls
        self.key = key
        self.dict = OrderedDict()
        self.update(kwargs)

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return repr(self.dict)

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __eq__(self, other):
        if isinstance(other, TypedMapping):
            return self.dict == other.dict and self.cls == other.cls
        else:
            return self.dict == other

    def __getitem__(self, i):
        return self.dict[i]

    def __delitem__(self, i):
        del self.dict[i]

    def __setitem__(self, i, v):
        self._check(v)
        self.dict[i] = v

    def add(self, v, key=None):
        if key is not None:
            self[key] = v

        elif self.key and hasattr(v, self.key):
            self[getattr(v, self.key)] = v  # pragma: no cover

        else:
            raise TypeError("No key set in instance or provided in call.")

    def _check(self, v):
        if not isinstance(v, self.allowed_types):
            raise TypeError("%s is not an instance of %s" % (v, self.cls))


class TypedSet(MutableSet):
    """
    Custom set type that checks the instance type of new values.

    reference:
    http://stackoverflow.com/a/3488283
    """

    def __init__(self, cls, args, allow_none=True):
        self.cls = cls
        self.allowed_types = (cls, type(None)) if allow_none else cls
        self.set = set()
        for arg in args or []:
            self.add(arg)

    def __str__(self):
        return str(self.set)

    def __repr__(self):
        return repr(self.set)

    def __len__(self):
        return len(self.set)

    def __eq__(self, other):
        if isinstance(other, TypedSet):
            return self.set == other.set and self.cls == other.cls
        else:
            return self.set == other

    def __iter__(self):
        return iter(self.set)

    def __contains__(self, item):
        return item in self.set

    def add(self, v):
        self._check(v)
        self.set.add(v)

    def discard(self, value):
        self.set.discard(value)

    def _check(self, v):
        if not isinstance(v, self.allowed_types):
            raise TypeError("Invalid value %s (%s != %s)" %
                            (v, type(v), self.cls))
