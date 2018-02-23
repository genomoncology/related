"""
Serialization decorator allows for the deserialization of input arguments
and serialization of the output. Useful in the creation of API functions that
need to take a nested-dictionary, transform it into a related object model,
maybe make a new model from that, and then return back a dictionary version
of the response.

Note: this code should also work with Python 3.6 type hints like this:

@related.serializer
def my_function(input: InputMode):
    return OutputModel(
        upper_case=input.lower_case.upper(),
        negative_number=input.positive_number * -1,
        shared=input.shared
    )
"""


import related
from .models import InputModel, OutputModel


@related.serializer(input=InputModel)
def my_function(input):
    return OutputModel(
        upper_case=input.lower_case.upper(),
        negative_number=input.positive_number * -1,
        shared=input.shared
    )


def test_serialization():
    result = my_function(
        input=dict(
            lower_case="hello world.",
            positive_number=123,
            shared=dict(
                one=dict(name="one", some_date="2001-01-01"),
                two=dict(name="two", some_date="2002-02-02"),
            )
        )
    )

    assert result == dict(
        upper_case="HELLO WORLD.",
        negative_number=-123,
        shared=dict(
            one=dict(name="one", some_date="2001-01-01"),
            two=dict(name="two", some_date="2002-02-02"),
        )
    )
