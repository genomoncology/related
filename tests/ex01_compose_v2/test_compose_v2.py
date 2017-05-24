from os.path import join, dirname

from .models import Compose
from related import to_yaml, from_yaml, to_model

YML_FILE = join(dirname(__file__), "docker-compose.yml")


def test_compose_from_yml():
    original_yaml = open(YML_FILE).read().strip()
    yml_dict = from_yaml(original_yaml)
    compose = to_model(Compose, yml_dict)

    assert compose.version == '2'
    assert compose.services['web'].ports == ["5000:5000"]
    assert compose.services['redis'].image == "redis"

    generated_yaml = to_yaml(compose,
                             suppress_empty_values=True,
                             suppress_map_key_values=True).strip()

    assert original_yaml == generated_yaml

    yml_dict2 = from_yaml(generated_yaml)

    compose2 = Compose(**yml_dict2)
    assert compose == compose2
    assert original_yaml == generated_yaml


def test_yaml_roundtrip_with_empty_values():
    original_yaml = open(YML_FILE).read().strip()
    yml_dict = from_yaml(original_yaml)
    compose = Compose(**yml_dict)
    generated_yaml = to_yaml(compose, suppress_map_key_values=True,
                             suppress_empty_values=False).strip()
    assert "ports: []" in generated_yaml
