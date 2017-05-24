from enum import Enum, unique
import related


@unique
class Degree(Enum):
    HIGH_SCHOOL = "High School"
    ASSOCIATES = "Associate's"
    BACHELORS = "Bachelor's"
    MASTERS = "Master's"
    PHD = "Ph.D"
    JD = "J.D."
    MD = "M.D."
    DDS = "D.D.S."
    PHARMD = "Pharm.D."


@related.immutable
class Address(object):
    street = related.StringField()
    city = related.StringField()
    zipcode = related.StringField()
    street_two = related.StringField(required=False)


@related.immutable
class Education(object):
    school = related.StringField()
    degree = related.ChildField(Degree, required=False)
    field_of_study = related.StringField(required=False)
    from_year = related.IntegerField(required=False)
    to_year = related.IntegerField(required=False)


@related.immutable
class Person(object):
    name = related.StringField()
    age = related.IntegerField(required=False)
    address = related.ChildField(Address, required=False, repr=False)
    education = related.SequenceField(Education, required=False, repr=False)
