from datetime import date, datetime
from uuid import UUID

from future.moves.urllib.parse import ParseResult
from pytest import fixture, raises
from six import string_types

from related import (to_dict, to_yaml, from_yaml,
                     to_json, from_json)

from .models import Company


@fixture
def company():
    return Company(
        name='Acme Inc.',
        url='http://www.acme-inc-website.net/',
        email='info@acme-inc.net',
        meta=dict(key1="value1", key2="value2"),
        nicknames=("Acme", u"Acme", 123),
        temperature=80.4,
        guess=[1, 4, 6, 8, 9, 14, 27, 45],
        established="1/2/1903",
        closed=datetime.strptime('1904-05-06', '%Y-%m-%d'),  # pass datetime
    )


def test_field_getters(company):
    assert company.name == 'Acme Inc.'
    assert isinstance(company.uuid, UUID)
    assert isinstance(company.url, ParseResult)
    assert company.url.geturl() == 'http://www.acme-inc-website.net/'
    assert company.url.netloc == 'www.acme-inc-website.net'
    assert company.url.scheme == 'http'
    assert company.nicknames == ["Acme", "Acme", "123"]
    assert company.guess == {1, 4, 6, 8, 9, 14, 27, 45}
    assert sorted(list(company.guess)) == [1, 4, 6, 8, 9, 14, 27, 45]
    assert company.temperature == 80.4
    assert company.established == date(1903, 1, 2)
    assert company.closed == date(1904, 5, 6)


def test_dictionary(company):
    company_dict = to_dict(company)
    assert company_dict['name'] == 'Acme Inc.'
    assert isinstance(company_dict['uuid'], string_types)
    assert isinstance(company_dict['url'], string_types)
    assert company_dict['established'] == "01/02/1903"
    assert company_dict['closed'] == "1904-05-06"


def test_yaml(company):
    company_yaml = to_yaml(to_dict(company))
    assert ("uuid: %s" % company.uuid) in company_yaml
    assert ("url: %s" % company.url.geturl()) in company_yaml


def test_roundtrip_yaml(company):
    new_company = from_yaml(to_yaml(company), Company)
    assert new_company == company


def test_roundtrip_json(company):
    new_company = from_json(to_json(company), Company)
    assert new_company == company


def test_invalid_regex():
    with raises(TypeError):
        Company(name="fail", email="fail")


def test_invalid_boolean(company):
    with raises(TypeError):
        Company(name="fail", is_active="YES!")
