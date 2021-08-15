# Related

| :exclamation:  This is a fork of [related](https://github.com/genomoncology/related), which is apparently abandoned :exclamation:|
|---------------------------------------------------------------------------------------------------------------------|

`Related` is a Python library for creating nested object models
that can be serialized to and de-serialized from
nested python dictionaries.
When paired with other libraries (e.g. [PyYAML]),
`Related` object models can be used to convert to and from
nested data formats (e.g. JSON, YAML).

Example use cases for `related` object models include:

* Configuration file reading and writing
* REST API message response generation and request processing
* Object-Document Mapping for a document store (e.g. MongoDB, elasticsearch)
* Data import parsing or export generation

<br/>

![flow-image]

<br/>

# Requirements

* Python (2.7, 3.5, 3.6)


# Installation

Install using `pip`...

    TBD


# First Example

```python
import related

@related.immutable
class Person(object):
    first_name = related.StringField()
    last_name = related.StringField()

@related.immutable
class RoleModels(object):
    scientists = related.SetField(Person)

people = [Person(first_name="Grace", last_name="Hopper"),
          Person(first_name="Katherine", last_name="Johnson"),
          Person(first_name="Katherine", last_name="Johnson")]

print(related.to_yaml(RoleModels(scientists=people)))
```

Yields:

```yaml
scientists:
- first_name: Grace
  last_name: Hopper
- first_name: Katherine
  last_name: Johnson
```


# Second Example

The below example is based off of this [Docker Compose example].
It shows how a YAML file can be loaded into an object model, tested, and
then generated back into a string that matches the original YAML.

```yaml
version: '2'
services:
  web:
    build: .
    ports:
    - 5000:5000
    volumes:
    - .:/code
  redis:
    image: redis
```

Below is the `related` object model that represents the above configuration.
Notice how the name-based mapping of services (i.e. web, redis) are
represented by the model.


```python
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
```

The above yaml can then be loaded by using one of the convenience
method and then round-tripped back to yaml to check that the format
has been maintained. The `related` module uses `OrderedDict` objects
in order to maintain sort order by default.

```python
from os.path import join, dirname

from model import Compose
from related import to_yaml, from_yaml, to_model

YML_FILE = join(dirname(__file__), "docker-compose.yml")


def test_compose_from_yml():
    original_yaml = open(YML_FILE).read().strip()
    yml_dict = from_yaml(original_yaml)
    compose = to_model(Compose, yml_dict)

    assert compose.version == '2'
    assert compose.services['web'].ports == ["5000:5000"]
    assert compose.services['redis'].image == "redis"

    generated_yaml = to_yaml(compose,
                             suppress_empty_values=True,
                             suppress_map_key_values=True).strip()

    assert original_yaml == generated_yaml
```


# More Examples

More examples can be found by reviewing the [tests/] folder of this project.
Below are links and descriptions of the tests provided so far.

| Example        | description                                                        |
| -------------- | ------------------------------------------------------------------ |
| [Example 00]   | First example above that shows how SetFields work.                 |
| [Example 01]   | Second example above that demonstrates YAML (de)serialization.     |
| [Example 02]   | Compose v3 with long-form ports and singledispatch to_dict         |
| [Example 03]   | A single class (Company) with a bunch of value fields.             |
| [Example 04]   | A multi-class object model with Enum class value field.            |
| [Example 05]   | Handling of renaming of attributes including Python keywords.      |
| [Example 06]   | Basic JSON (de)serialization with TimeField, DateTimeField and DecimalField.     |
| [Example 07]   | Function decorator that converts inputs to obj and outputs to dict |
| [Example 08]   | Handle self-referencing and out-of-order references using strings. |


# Documentation

Below is a quick version of documentation until more time can be dedicated.


## Overview

The [attrs] library is the underlying engine for `related`.
As explained in [this article by Glyph],
`attrs` cleanly and cleverly
eliminates a lot of the boilerplate
required when creating Python classes
without using inheritance.
Some core functionality provided by attrs:

* Generated initializer method
    (``__init__``)
* Generated comparison methods
    (``__eq__``, ``__ne__``, ``__lt__``, ``__le__``, ``__gt__``, ``__ge__`` )
* Human-readable representation method
    (``__repr__``)
* Attribute converter and validator framework


The `related` project is an opinionated layer
built on top of the `attrs` library
that provides the following:

* Value fields that handle both validation and conversion
  to and from basic data types like
  ``str``, ``float``, and ``bool``.
* Nested fields that support relationships such as
  Child, Sequences, Mappings, and Sets of objects.
* ``to_dict`` function that converts nested object graphs
  to python dictionaries.
  Made customizable (without resorting to [monkey-patching])
  by the [singledispatch library].
* ``to_model`` function that instantiated classes
  used by the de-serialization process going from
  python dictionaries to the related model.
* Conversion helper functions
  (``to_yaml``, ``from_yaml``, ``to_json``, ``from_json``)
  for easily going between
  related models and data formats.
* ``@mutable`` and ``@immutable`` for decorating classes
  as related models without the need for inheritance increasing
  maintainability and flexibility.


## Class Decorators

| decorator             | description                                                      |
| --------------        | ---------------------------------------------------------------- |
| @mutable              | Activate a related class that instantiates changeable objects.   |
| @immutable            | Activate a related class that instantiates unchangeable objects. |

See the [decorators.py] file to view the source code until proper
documentation is generated.


## Field Types

| field type            | description                                                      |
| --------------        | ---------------------------------------------------------------- |
| BooleanField          | `bool` value field.                                              |
| ChildField            | Child object of a specified type `cls`.                          |
| DateField             | `date` field formatted using `formatter`.                        |
| DateTimeField         | `datetime` field formatted using `formatter`.                    |
| TimeField             | `time` field formatted using `formatter`.                    |
| FloatField            | `float` value field.                                             |
| IntegerField          | `int` value field.                                               |
| MappingField(cls,key) | Dictionary of objects of type `cls` index by `key` field values. |
| RegexField(regex)     | `str` value field that is validated by re.match(`regex`).        |
| SequenceField(cls)    | List of objects all of specified type `cls`.                     |
| SetField              | Set of objects all of a specified type `cls`.                    |
| StringField           | `str` value field.                                               |
| URLField              | [ParseResult] object.                                            |
| UUIDField             | [UUID] object, will create [uuid4] by default if not specified.  |


Adding your own field types is fairly straightforward
due to the power of the underlying `attrs` project.
See the [fields.py] file to see how the above are constructed.

All fields support the `kw_only` keyword, which is part of [attrs](https://www.attrs.org/en/stable/changelog.html#id102).
Setting `kw_only=True` makes it possible to have a generated `__init__` with keyword-only arguments,
relaxing the required ordering of default and non-default valued attributes.


## Functions

| function            | description                                           |
| ------------------- | ----------------------------------------------------- |
| from_json(s,cls)    | Convert a JSON string or stream into specified class. |
| from_yaml(s,cls)    | Convert a YAML string or stream into specified class. |
| is_related(obj)     | Returns True if object is @mutable or @immutable.     |
| to_dict(obj)        | Singledispatch function for converting to a dict.     |
| to_json(obj)        | Convert object to a (pretty) JSON string via to_dict. |
| to_model(cls,value) | Convert a value to a `cls` instance.                  |
| to_yaml(obj)        | Convert object to a YAML string via to_dict.          |


See the [functions.py] file to view the source code until proper
documentation is generated.


# Credits/Prior Art

The `related` project has been heavily influenced by the following
projects that might be worth looking at if `related` doesn't meet your needs.

* [attrs] - The engine that powers `related` functionality.
* [Django ORM] - Object-relational mapping for Django that inspired `related's` design.
* [cattrs] - Alternative take for handling nested-objects using `attrs`.
* [addict] and [box] - Python dictionary wrappers that do not require a model.
* [Jackson] - Java-based technology for serializing and de-serializing objects.


# License

The MIT License (MIT)
Copyright (c) 2017 [Ian Maurer], [Genomoncology LLC]




[flow-image]: ./.images/flow.png
[decorators.py]: ./src/related/decorators.py
[fields.py]: ./src/related/fields.py
[functions.py]: ./src/related/functions.py
[attrs]: http://attrs.readthedocs.io/en/stable/
[this article by Glyph]: https://glyph.twistedmatrix.com/2016/08/attrs.html
[Genomoncology LLC]: http://genomoncology.com
[Ian Maurer]: https://github.com/imaurer
[singledispatch library]: https://pypi.python.org/pypi/singledispatch
[monkey-patching]: http://stackoverflow.com/questions/5626193/what-is-a-monkey-patch
[Django ORM]: https://docs.djangoproject.com/en/1.11/topics/db/models/
[UUID]: https://docs.python.org/3/library/uuid.html#uuid.UUID
[uuid4]: https://docs.python.org/3/library/uuid.html#uuid.uuid4
[ParseResult]: https://docs.python.org/2/library/urlparse.html#urlparse.ParseResult
[cattrs]: http://cattrs.readthedocs.io/en/latest/readme.html
[addict]: https://github.com/mewwts/addict
[box]: https://pypi.python.org/pypi/python-box
[Jackson]: https://github.com/FasterXML/jackson
[Docker Compose example]: https://docs.docker.com/compose/gettingstarted/#step-3-define-services-in-a-compose-file
[PyYAML]: https://pypi.python.org/pypi/PyYAML

[tests/]: ./tests/
[Example 00]: ./tests/ex00_sets_hashes
[Example 01]: ./tests/ex01_compose_v2
[Example 02]: ./tests/ex02_compose_v3.2
[Example 03]: ./tests/ex03_company
[Example 04]: ./tests/ex04_contact
[Example 05]: ./tests/ex05_field_names
[Example 06]: ./tests/ex06_json
[Example 07]: ./tests/ex07_serializer
[Example 08]: ./tests/ex08_self_reference
