import related


@related.immutable()
class Child(object):
    name = related.StringField(default="!")


@related.immutable()
class Model(object):
    # non-child fields
    sequence_field = related.SequenceField(str, default=set())
    set_field = related.SetField(str, default=[])
    mapping_field = related.MappingField(Child, "name", default={})

    # child fields
    child_list = related.ChildField(list, default=list)
    child_set = related.ChildField(set, default=set)
    child_dict = related.ChildField(dict, default=dict)
    child_obj = related.ChildField(Child, default=Child)


def test_sequence_field_ok():
    obj_1 = Model()

    obj_1.sequence_field.append("a")
    obj_1.sequence_field.append("b")
    obj_1.sequence_field.append("c")
    obj_1.sequence_field.append("c")

    assert len(obj_1.sequence_field) == 4
    assert len(Model().sequence_field) == 0


def test_set_field_ok():
    obj_1 = Model()

    obj_1.set_field.add("a")
    obj_1.set_field.add("b")
    obj_1.set_field.add("c")
    obj_1.set_field.add("c")

    assert len(obj_1.set_field) == 3
    assert len(Model().set_field) == 0


def test_mapping_field_ok():
    obj_1 = Model()

    obj_1.mapping_field.add(Child("a"))
    obj_1.mapping_field.add(Child("b"))
    obj_1.mapping_field.add(Child("c"))
    obj_1.mapping_field.add(Child("c"))

    assert len(obj_1.mapping_field) == 3
    assert len(Model().mapping_field) == 0


def test_child_list_ok():
    obj_1 = Model()

    obj_1.child_list.append(Child("a"))
    obj_1.child_list.append(Child("b"))
    obj_1.child_list.append(Child("c"))
    obj_1.child_list.append(Child("c"))

    assert len(obj_1.child_list) == 4
    assert len(Model().child_list) == 0


def test_child_set_ok():
    obj_1 = Model()

    obj_1.child_set.add(Child("a"))
    obj_1.child_set.add(Child("b"))
    obj_1.child_set.add(Child("c"))
    obj_1.child_set.add(Child("c"))

    assert len(obj_1.child_set) == 3
    assert len(Model().child_set) == 0


def test_child_dict_ok():
    obj_1 = Model()

    obj_1.child_dict['a'] = Child("a")
    obj_1.child_dict['b'] = Child("b")
    obj_1.child_dict['c'] = Child("c")

    assert len(obj_1.child_dict) == 3
    assert len(Model().child_dict) == 0


def test_child_obj_ok():
    obj_1 = Model(child_obj=Child("a"))

    assert obj_1.child_obj == Child("a")
    assert Model().child_obj != obj_1.child_obj
    assert Model().child_obj == Child()
