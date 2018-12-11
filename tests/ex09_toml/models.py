from enum import Enum, unique
import related


@unique
class DayType(Enum):
    NORMAL = "Normal"
    HOLIDAY = "Holiday"


@related.immutable
class DayData(object):
    date = related.DateField()
    logged_on = related.TimeField("%H:%M")
    open_at = related.TimeField()
    closed_on = related.TimeField()
    customers = related.IntegerField()
    day_type = related.ChildField(DayType)
    sales = related.FloatField(required=False)


@related.immutable
class StoreData(object):
    name = related.StringField()
    id = related.IntegerField()
    created_on = related.DateTimeField("%m/%d/%Y %H:%M:%S")
    data_from = related.DateTimeField()
    data_to = related.DateTimeField()
    days = related.SequenceField(DayData)
    price = related.DecimalField()
