#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Person, Address, Education, Degree

from related import to_dict, to_yaml, from_yaml

import pytest


def test_person():
    person = Person(name="Bob")
    assert repr(person) == "Person(name='Bob', age=None)"

    person = Person(name="Bill", age=40)
    assert repr(person) == "Person(name='Bill', age=40)"

    person = Person(name="John", age="50")
    assert repr(person) == "Person(name='John', age=50)"

    d = to_dict(person)
    assert d == {'address': None,
                 'education': [],
                 'age': 50,
                 'name': 'John'}

    new_person = Person(**d)
    assert to_dict(new_person) == d
    assert new_person == person


def test_address_yaml_roundtrip():
    address = Address(street="123 Main Street", city="Springfield",
                      zipcode="12345")
    assert repr(address) == "Address(street='123 Main Street', " \
                            "city='Springfield', zipcode='12345', " \
                            "street_two=None)"

    yaml = to_yaml(address)
    new_address = from_yaml(yaml, Address)
    assert new_address == address


def test_person_with_address():
    address = Address(street="123 Main Street", city="Springfield",
                      zipcode="12345")
    assert repr(address) == "Address(street='123 Main Street', " \
                            "city='Springfield', zipcode='12345', " \
                            "street_two=None)"

    # repr = False for address
    person = Person(name="Jim", address=address)
    assert repr(person) == "Person(name='Jim', age=None)"

    # to_dict() => convert model to dictionary
    d = to_dict(person)
    assert d == {'address': {'city': 'Springfield',
                             'street': '123 Main Street',
                             'street_two': None,
                             'zipcode': '12345'},
                 'education': [],
                 'age': None,
                 'name': 'Jim'}

    # now load from dictionary...
    new_person = Person(**d)
    assert to_dict(new_person) == d
    assert new_person == person


def test_enum():
    education = Education(school="My Alma Mater", degree=Degree.MASTERS)

    # to_dict() => convert model to dictionary
    d = to_dict(education)
    assert d == {'school': 'My Alma Mater',
                 'degree': Degree.MASTERS.value,
                 'field_of_study': None,
                 'from_year': None,
                 'to_year': None}

    # now load from dictionary...
    new_education = Education(**d)
    assert to_dict(new_education) == d
    assert new_education == education

    d = to_dict(new_education)
    assert d == {'school': 'My Alma Mater',
                 'degree': Degree.MASTERS.value,
                 'field_of_study': None,
                 'from_year': None,
                 'to_year': None}


def test_person_with_education_sequence():
    person = Person(name="Brainy", education=[
        Education(school="School 2", degree=Degree.MASTERS),
        Education(school="School 1", degree=Degree.BACHELORS),
    ])

    # to_dict() => convert model to dictionary
    d = to_dict(person)
    assert d == {'address': None,
                 'age': None,
                 'education': [
                     {'degree': Degree.MASTERS.value,
                      'field_of_study': None,
                      'from_year': None,
                      'school': 'School 2',
                      'to_year': None},
                     {'degree': Degree.BACHELORS.value,
                      'field_of_study': None,
                      'from_year': None,
                      'school': 'School 1',
                      'to_year': None}],
                 'name': 'Brainy'}

    # now load from dictionary...
    new_person = Person(**d)
    assert new_person.education == person.education
    assert new_person == person


def test_person_with_education_to_yaml_and_back():
    person = Person(name="Brainy", education=[
        Education(school="School 2", degree=Degree.MASTERS),
        Education(school="School 1", degree=Degree.BACHELORS),
    ])

    yaml = to_yaml(person)
    new_person = from_yaml(yaml, Person)
    assert new_person.education == person.education
    assert new_person == person


def test_fail_missing_field():
    with pytest.raises(TypeError):
        Person()


def test_fail_invalid_age_field():
    with pytest.raises(ValueError):
        Person(name="Joe", age="invalid")


def test_fail_invalid_address_class():
    with pytest.raises(TypeError):
        Person(name="Joe", address="My Address")


def test_with_invalid_class_type():
    Education(school="My Alma Mater")
    with pytest.raises(ValueError):
        Education(school="My Alma Mater", degree="Master of Universe")
