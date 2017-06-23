# coding=utf-8
from related.types import TypedSequence, TypedMapping, TypedSet, ImmutableDict
from attr.exceptions import FrozenInstanceError
from related.converters import str_if_not_none
from collections import OrderedDict
import pytest


def test_immutable_dict():
    immutable = ImmutableDict(dict(a=1))

    with pytest.raises(FrozenInstanceError):
        del immutable['a']

    assert immutable == dict(a=1)

    with pytest.raises(FrozenInstanceError):
        immutable['b'] = 2

    assert immutable == dict(a=1)

    with pytest.raises(FrozenInstanceError):
        immutable.clear()

    assert immutable == dict(a=1)

    with pytest.raises(FrozenInstanceError):
        immutable.pop('a')

    assert immutable == dict(a=1)

    with pytest.raises(FrozenInstanceError):
        immutable.something = 0

    assert immutable == dict(a=1)

    with pytest.raises(FrozenInstanceError):
        del immutable.something_else

    assert immutable == dict(a=1)


def test_str_if_not_none():
    unicode_value = "Registered Trademark ®"
    assert unicode_value == str_if_not_none(unicode_value)
    assert "1" == str_if_not_none(1)
    assert str_if_not_none(None) is None


def test_sequence():
    lst = ["a", "b", "c"]
    seq = TypedSequence(str, lst)
    assert seq == lst
    assert str(seq) == str(lst)
    assert repr(seq) == repr(lst)
    assert len(seq) == len(lst)

    del seq[1]
    del lst[1]
    assert seq == lst

    seq[1] = "d"
    assert seq != lst

    with pytest.raises(TypeError):
        seq[1] = 4.0


def test_mapping():
    dct = OrderedDict(a=1, b=2, c=3)
    map = TypedMapping(int, dct)
    assert map == dct
    assert str(map) == str(dct)
    assert repr(map) == repr(dct)
    assert len(map) == len(dct)

    del map["b"]
    del dct["b"]
    assert map == dct

    with pytest.raises(TypeError):
        map["d"] = 4.0

    with pytest.raises(TypeError):
        map.add(5)

    map.add(4, 'd')
    dct['d'] = 4
    assert map == dct


def test_set():
    orig = {"a", "b", "c"}
    typed = TypedSet(str, orig)

    assert orig == typed
    assert len(orig) == len(typed)
    assert 'a' in str(typed)
    assert 'a' in repr(typed)

    typed.add("d")
    assert "d" in typed
    assert orig != typed

    typed.discard("d")
    assert "d" not in typed
    assert orig == typed

    with pytest.raises(TypeError):
        typed.add(5)
