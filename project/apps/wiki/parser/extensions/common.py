import re

def get_tag_data(tag: str) -> dict:
    """
    example:
        callout{template="warning" hidden="false"}
    returns:
        {'tag_type': 'callout', 'attributes': {'template': 'warning', 'hidden': 'false'}}
        or 
        False
    """

    match = re.match("([a-zA-Z]+){(.+)}", tag)
    if (not match or len(match.groups()) != 2): return False

    tag_type = match.group(1)
    attributes = get_tag_attributes(match.group(2))
    
    return {'tag_type': tag_type, 'attributes': attributes}


def get_tag_attributes(unformatted_attributes: str):
    """
    example:
        template="warning" hidden="false"
    returns:
        {'template': 'warning', 'hidden': 'false'}
    """
        
    attributes = {}

    z = unformatted_attributes.split(' ')
    for a in z:
        s = a.split('=', 1)
        attributes[s[0]] = s[1].replace('"', '')
    
    return attributes