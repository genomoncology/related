import related


@related.mutable
class Company(object):
    name = related.StringField()
    uuid = related.UUIDField()
    email = related.RegexField("[^@]+@[^@]+", required=False)
    is_active = related.BooleanField(required=False)
    url = related.URLField(required=False)
    meta = related.ChildField(dict, required=False)
    nicknames = related.SequenceField(str, required=False)
    temperature = related.FloatField(required=False)
    guess = related.SetField(int, required=False)
    established = related.DateField('%m/%d/%Y', required=False)
    closed = related.DateField(required=False)  # default formatter (%Y-%m-%d)
