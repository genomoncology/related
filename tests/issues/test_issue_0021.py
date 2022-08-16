import related


@related.immutable(strict=True)
class Person(object):
    first_name = related.fields.StringField()
    last_name = related.fields.StringField()

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


person = Person(first_name='John', last_name='Doe')


def test_class_property_attrs():
    property_attrs = getattr(person, '__property_attrs__')
    assert len(property_attrs) == 1
    assert property_attrs[0].name == 'full_name'


def test_to_dict():
    converted_dict = related.to_dict(person)
    assert converted_dict['full_name'] == 'John Doe'
