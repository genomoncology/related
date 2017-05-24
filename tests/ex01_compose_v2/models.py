import related


@related.immutable
class Service(object):
    name = related.StringField()
    image = related.StringField(required=False)
    build = related.StringField(required=False)
    ports = related.SequenceField(str, required=False)
    volumes = related.SequenceField(str, required=False)
    command = related.StringField(required=False)


@related.immutable
class Compose(object):
    version = related.StringField(required=False, default=None)
    services = related.MappingField(Service, "name", required=False)
