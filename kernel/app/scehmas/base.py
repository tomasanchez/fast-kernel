"""
 Base Model
"""
from re import sub

from pydantic import BaseModel


def to_camel(s: str) -> str:
    """
    Convert string to camel case
    """
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return ''.join([s[0].lower(), s[1:]])


class CamelCaseModel(BaseModel):
    """
    A generic model that converts all keys to camelCase. A utility for serialization, built on top of Pydantic
    BaseModel.
    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
