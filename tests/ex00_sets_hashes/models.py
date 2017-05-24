import related


# removing the frozen gives you (TypeError: unhashable type: 'Person')
@related.immutable
class Person(object):
    first_name = related.StringField()
    last_name = related.StringField()


@related.immutable
class RoleModels(object):
    scientists = related.SetField(Person)
