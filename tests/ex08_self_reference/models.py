import related

node_cls = "ex08_self_reference.models.Node"


@related.mutable
class Node(object):
    name = related.StringField()
    node_child = related.ChildField(node_cls, required=False)
    node_list = related.SequenceField(node_cls, required=False)
    node_map = related.MappingField(node_cls, "name", required=False)
