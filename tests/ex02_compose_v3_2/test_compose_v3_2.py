from os.path import join, dirname

from .models import Compose, Port

from related import to_yaml, from_yaml

YML_FILE = join(dirname(__file__), "docker-compose.yml")


def test_compose_from_yml():
    original_yaml = open(YML_FILE).read().strip()
    yml_dict = from_yaml(original_yaml)
    compose = Compose(**yml_dict)

    # basic checks
    assert compose.version == '2'
    assert compose.services['redis'].image == "redis"

    # compare short form vs. long form
    expected = Port(target="5000", published="5000")
    assert expected == compose.services['web'].ports[0]

    # private attributes suppressed
    generated_yaml = to_yaml(compose,
                             suppress_private_attr=True,
                             suppress_empty_values=True,
                             suppress_map_key_values=True).strip()
    assert "_short_form" not in generated_yaml

    # can we make these equal??
    assert original_yaml == generated_yaml
