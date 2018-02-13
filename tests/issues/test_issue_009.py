import related
import pytest


@related.immutable
class Child(object):
    name = related.StringField()
    values = related.SequenceField(str, required=False)


@related.immutable
class Root(object):
    children = related.MappingField(Child, 'name', required=False)


def test_empty_mapping():
    root = related.from_yaml(INPUT_YAML, Root)
    assert related.to_yaml(root).strip() == OUTPUT_YAML


def test_null_mapping():
    root = related.from_yaml(OUTPUT_YAML, Root)
    assert related.to_yaml(root).strip() == OUTPUT_YAML


def test_invalid_mapping():
    with pytest.raises(TypeError):
        related.from_yaml(INVALID_YAML, Root)


INPUT_YAML = "children:"
OUTPUT_YAML = "children: null"
INVALID_YAML = "children: 5"
