import related


@related.immutable
class SharedModel(object):
    name = related.StringField()
    some_date = related.DateField()


@related.immutable
class InputModel(object):
    lower_case = related.StringField()
    positive_number = related.IntegerField()
    shared = related.MappingField(SharedModel, "name")


@related.immutable
class OutputModel(object):
    upper_case = related.StringField()
    negative_number = related.IntegerField()
    shared = related.MappingField(SharedModel, "name")
