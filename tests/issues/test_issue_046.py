import related
import pytest


@related.immutable
class Person:
    a_name = related.StringField(key='name')
    an_age = related.IntegerField(key='age')


def test_no_kwarg():
    json = {'name': 'John Doe', 'age': 74}
    person = related.to_model(Person, json)
    assert json == related.to_dict(person)


def test_deserialization_kwarg():
    json_no_kwarg = {'name': 'John Doe', 'age': 74}
    json_kwarg = {'a_name': 'John Doe', 'an_age': 74}
    person = related.to_model(Person, json_kwarg, ignore_keys=True)
    assert json_no_kwarg == related.to_dict(person)


def test_serialization_kwarg():
    json_no_kwarg = {'name': 'John Doe', 'age': 74}
    json_kwarg = {'a_name': 'John Doe', 'an_age': 74}
    person = related.to_model(Person, json_no_kwarg)
    assert json_kwarg == related.to_dict(person, ignore_keys=True)


def test_invalid_mapping_no_kwarg():
    json_no_kwarg = {'name': 'John Doe', 'age': 74}
    with pytest.raises(TypeError):
        related.to_model(Person, json_no_kwarg)


def test_invalid_mapping_kwarg():
    json_kwarg = {'a_name': 'John Doe', 'an_age': 74}
    with pytest.raises(TypeError):
        related.to_model(Person, json_kwarg, ignore_keys=True)
