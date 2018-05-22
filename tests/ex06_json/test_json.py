from os.path import join, dirname
from datetime import datetime, time

from decimal import Decimal

from .models import StoreData, DayType
from related import to_json, from_json, to_model

JSON_FILE = join(dirname(__file__), "store-data.json")


def test_store_data_from_json():
    original_json = open(JSON_FILE).read().strip()
    json_dict = from_json(original_json)
    store_data = to_model(StoreData, json_dict)

    assert store_data.name == "Acme store"
    assert store_data.id == 982
    assert store_data.price == Decimal('98237.448')
    assert store_data.data_from == datetime(2017, 12, 18, 0, 0)
    assert store_data.data_to == datetime(2017, 12, 19, 23, 59, 59)
    assert len(store_data.days) == 2

    assert isinstance(store_data.days[0].open_at, time)
    assert store_data.days[0].date == datetime(2017, 12, 18).date()
    assert store_data.days[0].open_at == time(8, 0, 0)
    assert store_data.days[0].closed_on == time(19, 0, 0)
    assert store_data.days[0].customers == int(487)
    assert store_data.days[0].day_type == DayType.NORMAL
    assert store_data.days[0].sales == float(27223.65)

    assert store_data.days[1].date == datetime(2017, 12, 19).date()
    assert store_data.days[1].open_at == time(10, 30, 0)
    assert store_data.days[1].closed_on == time(17, 30, 0)
    assert store_data.days[1].customers == int(192)
    assert store_data.days[1].day_type == DayType.HOLIDAY
    assert store_data.days[1].sales is None

    generated_json = to_json(store_data,
                             suppress_empty_values=True,
                             suppress_map_key_values=True).replace(" ", "")
    # print(original_json)
    # print(generated_json)
    assert original_json.replace(" ", "") == generated_json
