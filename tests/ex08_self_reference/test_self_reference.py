import related
from .models import Node

original_json = """
{
  "name": "root",
  "node_list": [
    {
      "name": "A"
    },
    {
      "name": "B"
    }
  ],
  "node_child": {
    "name": "C"
  },
  "node_map": {
    "E": {},
    "F": {
      "node_child": {
        "name": "G"
      }
    }
  }
}
"""


def test_self_reference():
    root_node = related.from_json(original_json, Node)
    assert root_node.name == "root"
    assert root_node.node_list[0].name == "A"
    assert root_node.node_list[1].name == "B"
    assert root_node.node_child.name == "C"
    assert len(root_node.node_map) == 2
    assert root_node.node_map["F"].name == "F"
    assert root_node.node_map["F"].node_child.name == "G"
