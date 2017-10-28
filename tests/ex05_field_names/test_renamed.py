import related
import enum
import uuid


EXAMPLE_UUID = uuid.uuid4()


@enum.unique
class DataType(enum.Enum):
    STRING = 'string'
    NUMBER = 'number'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    ARRAY = 'array'
    OBJECT = 'object'


@related.immutable
class MyChild(object):
    my_int = related.IntegerField(key="int")
    my_float = related.FloatField(key="float")
    my_uuid = related.UUIDField(key="uuid")


@related.immutable
class MyModel(object):
    is_for = related.StringField(key="for")
    criss = related.StringField(key="cross")
    cross = related.StringField(key="criss")
    is_not = related.BooleanField(key="not")
    is_list = related.SequenceField(str, key="list")
    is_type = related.ChildField(DataType, key="type")
    is_dict = related.MappingField(MyChild, "int", key="dict", required=False)


def test_renamed():
    obj = MyModel(
        is_for="Elise",
        criss="A",
        cross="B",
        is_not=True,
        is_list=["a", "b", "c"],
        is_dict={5: MyChild(my_int=5, my_uuid=EXAMPLE_UUID, my_float=3.14)},
        is_type=DataType.OBJECT,
    )

    d = related.to_dict(obj)

    assert related.to_model(MyModel, d) == obj

    d.pop("dict")

    assert d == {
        "for": "Elise",
        "criss": "B",
        "cross": "A",
        "not": True,
        'list': ['a', 'b', 'c'],
        "type": "object",
    }
