from attr import attr, attributes
import re


@attributes(repr=False, slots=True)
class _CompositeValidator(object):
    validators = attr()

    def __call__(self, inst, attr, value):
        for validator in self.validators:
            validator(inst, attr, value)

    def __repr__(self):
        return (
            "<composite validator for validators {!r}>".format(self.validators)
        )


def composite(*validators):
    """A validator that executes each validator passed as arguments.
    """
    return _CompositeValidator(validators)


@attributes(repr=False, slots=True)
class _RegexValidator(object):
    regex = attr()

    def __call__(self, inst, attr, value):
        if not re.match(self.regex, value):
            raise TypeError(
                "'{name}' must match {regex!r} (got {value!r}).".format(
                    name=attr.name, regex=self.regex, value=value), attr,
                self.regex, value)

    def __repr__(self):
        return (
            "<regex validator for {!r}>".format(self.regex)
        )


def regex(match_string):
    """A validator that executes each validator passed as arguments.

    """
    return _RegexValidator(match_string)
