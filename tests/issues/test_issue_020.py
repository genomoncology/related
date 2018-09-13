import related


@related.immutable
class ImageOptions(object):
    registry = related.URLField(required=False)
    email = related.StringField(required=True)


def test_non_required_first_no_exceptions():
    ImageOptions(registry='http://example.com',
                 email='email@example.com')
