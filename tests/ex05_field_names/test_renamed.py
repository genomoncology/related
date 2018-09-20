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


@enum.unique
class IntEnum(enum.Enum):
    a = 1
    b = 2
    c = 3


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
    is_nullable_list = related.NullableSequenceField(str, key="nullable_list")
    is_type = related.ChildField(DataType, key="type")
    is_dict = related.MappingField(MyChild, "int", key="dict", required=False)
    is_enum = related.ChildField(IntEnum, key="enum", required=False)


def test_renamed():
    obj = MyModel(
        is_for="Elise",
        criss="A",
        cross="B",
        is_not=True,
        is_list=["a", "b", "c"],
        is_nullable_list=["a", None, "c"],
        is_dict={5: MyChild(my_int=5, my_uuid=EXAMPLE_UUID, my_float=3.14)},
        is_type=DataType.OBJECT,
        is_enum=IntEnum.a,
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
        "nullable_list": ["a", None, "c"],
        "type": "object",
        "enum": 1
    }
