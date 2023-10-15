from django import template

register = template.Library()

from ..elements import Navbar, AuxNavbar

@register.inclusion_tag("nav.html")
def primary_navbar(selected_key):
    return {
        "navbar": Navbar,
        "selected_key": selected_key
    }