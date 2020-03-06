from enum import Enum, unique
import related


@unique
class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"


@unique
class Mode(Enum):
    HOST = "host"
    INGRESS = "ingress"


@related.immutable
class Port(object):
    """ https://docs.docker.com/compose/compose-file/#ports """
    _short_form = related.StringField(required=False, repr=False, eq=False)
    target = related.IntegerField(required=False)
    published = related.IntegerField(required=False)
    protocol = related.ChildField(Protocol, default=Protocol.TCP)
    mode = related.ChildField(Mode, default=Mode.HOST)

    def __attrs_post_init__(self):
        if self._short_form:
            # todo: handle protocol and mode parsing
            published, target = map(int, self._short_form.split(":"))

            # set methods won't work because the class is immutable.
            # workaround: https://github.com/python-attrs/attrs/issues/120
            object.__setattr__(self, "published", published)
            object.__setattr__(self, "target", target)


@related.to_dict.register(Port)
def _(inst, **kwargs):
    if inst._short_form:
        return inst._short_form
    else:
        return related.to_dict.dispatch(object)(inst, **kwargs)


@related.immutable
class Service(object):
    name = related.StringField()
    image = related.StringField(required=False)
    build = related.StringField(required=False)
    ports = related.SequenceField(Port, required=False)
    volumes = related.SequenceField(str, required=False)
    command = related.StringField(required=False)


@related.immutable
class Compose(object):
    version = related.StringField(required=False, default=None)
    services = related.MappingField(Service, "name", required=False)
