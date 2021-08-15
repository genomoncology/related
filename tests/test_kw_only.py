import datetime
import decimal
import uuid

import related


@related.immutable
class User:
    name = related.StringField()
    company = related.StringField(default="N.A.")

    # Without kw_only=True this would not be possible
    some_boolean_field = related.BooleanField(kw_only=True)
    some_child_field = related.ChildField(kw_only=True, cls=str)
    some_date_field = related.DateField(kw_only=True)
    some_datetime_field = related.DateTimeField(kw_only=True)
    some_time_field = related.TimeField(kw_only=True)
    some_float_field = related.FloatField(kw_only=True)
    some_integer_field = related.IntegerField(kw_only=True)
    some_mapping_field = related.MappingField(kw_only=True, cls=int, child_key="field")
    some_regex_field = related.RegexField(kw_only=True, regex=r"\w+")
    some_sequence_field = related.SequenceField(kw_only=True, cls=str)
    some_set_field = related.SetField(kw_only=True, cls=str)
    some_url_field = related.URLField(kw_only=True)
    some_uuid_field = related.UUIDField(kw_only=True)
    some_decimal_field = related.DecimalField(kw_only=True)


def test_boolean_field():
    data = {
        "name": "Foo Bar",
        "some_boolean_field": True,
        "some_child_field": "Hello",
        "some_date_field": datetime.date(2021, 12, 24).isoformat(),
        "some_datetime_field": datetime.datetime(2021, 12, 24).isoformat(),
        "some_time_field": "12:12:12",
        "some_float_field": 13.37,
        "some_integer_field": 42,
        "some_mapping_field": {"field": 69},
        "some_regex_field": "abc",
        "some_sequence_field": ["A", "B", "C"],
        "some_set_field": {"A", "B", "C"},
        "some_url_field": "https://google.de",
        "some_uuid_field": uuid.uuid4(),
        "some_decimal_field": 13.37,
    }
    user = related.to_model(User, data)

    assert user.name == "Foo Bar"
    assert user.some_boolean_field
    assert user.some_child_field == "Hello"
    assert user.some_date_field == datetime.date(2021, 12, 24)
    assert user.some_datetime_field == datetime.datetime(2021, 12, 24)
    assert user.some_time_field == datetime.time.fromisoformat("12:12:12")
    assert user.some_float_field == 13.37
    assert user.some_integer_field == 42
    assert user.some_mapping_field["field"] == 69
    assert user.some_sequence_field == ["A", "B", "C"]
    assert user.some_set_field == {"A", "B", "C"}
    assert user.some_url_field
    assert user.some_uuid_field
    assert user.some_decimal_field == decimal.Decimal(13.37)
