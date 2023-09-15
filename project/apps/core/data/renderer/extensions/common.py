import re

def get_tag_data(tag: str, default_attributes: dict = {}) -> dict:
    """
    example:
        tag = "callout{template="warning" hidden="false"}"
    returns: dict?
        {'tag_type': 'callout', 'attributes': {'template': 'warning', 'hidden': 'false'}}
    """

    match = re.match(r"([a-zA-Z]+){(.+)}?", tag)
    if (not match or len(match.groups()) != 2): return False

    tag_type = match.group(1)
    attributes = get_tag_attributes(match.group(2))

    for k, v in default_attributes.items():
        if (not k in attributes):
            attributes[k] = v
    
    return {'tag_type': tag_type, 'attributes': attributes}


def get_tag_attributes(unformatted_attributes: str):
    """
    example:
        unformatted_attributes = "template="warning" hidden="false""
    returns: dict
        {'template': 'warning', 'hidden': 'false'}
    """
        
    attributes = {}
    split_up_attributes = unformatted_attributes.split(' ')

    for a in split_up_attributes:
        split_string = a.split('=', 1)
        val = split_string[1].replace('"', '')
        if (val.lower() in ['false', 'true']): # is bool
            val = True if val.lower() == 'true' else False
        attributes[split_string[0]] = val
    
    return attributes