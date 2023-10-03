import re
from typing import List, Optional

from ..base import substitute_tag_or_return, split_attribute

try:
    from config.renderer import TAG_PREFIX
except ImportError:
    TAG_PREFIX = '#'

def format_value(v):
    """
    v -> "dog" or dog
    returns dog (str)
    """
    if (v[0] == '"'):
        v = v[1:]
    if (v[-1] == '"'):
        v = v[:-1]

    return v


def get_tag_data(unformatted_attributes: Optional[str], default_attributes: dict = {}, all_attributes: List[str] = []) -> dict:
    """
    unformatted_attributes -> key="value", key2="value2"
    default_attributes -> {'key3': 'myvalue'}

    returns {'key': 'value', 'key2': 'value2', 'key3': 'myvalue'}
    """
    attributes = {}
    if (not unformatted_attributes): return attributes
    attribute_list = re.split(r' ', unformatted_attributes)

    wildcarded = '*' in all_attributes

    for i in attribute_list:
        zzz = re.split(r' ?= ?', i)
        if (len(zzz) != 2): 
            return {}
        k, v = zzz
        if (wildcarded or k in all_attributes):
            attributes[k] = v

    for k, v in default_attributes.items():
        if (not k in attributes):
            attributes[k] = format_value(v)

    return attributes


def are_attributes_valid(attributes: Optional[dict], required_attributes: List[str]) -> bool:
    for k in required_attributes:
        if (not k in attributes):
            return False
    return True


def push_attributes(token, prefix: str, attributes: dict, pushable_attributes: List[str]):
    wildcarded = '*' in pushable_attributes

    for k, v in attributes.items():
        if (wildcarded or k in pushable_attributes):
            unquoted_v = format_value(v)
            sub_v = substitute_tag_or_return(unquoted_v)
            arr = split_attribute(sub_v)
            
            for i in arr:
                token.attrJoin("class", f"{prefix}-attribute-{k}-{i}")