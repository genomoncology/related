import related


@related.immutable
class ImageOptions(object):
    registry = related.URLField()
    email = related.StringField()


def test_image_options():
    options = ImageOptions(
        registry="https://imgur.com/gallery/GAhlfKS", email="black@knight.com"
    )
    assert options.registry
    assert options.email
