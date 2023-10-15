from django import template

register = template.Library()

from ..elements import AuxNavbar

@register.inclusion_tag("aux_nav.html")
def wiki_aux_navbar(selected_key):
    return {
        "navbar": AuxNavbar,
        "selected_key": selected_key
    }