"""
bulk of code forked from mdit_py_plugins.container_plugin
(to add a bit of flexibility over the usual import and keep it version independant)
"""

from markdown_it.rules_block import StateBlock
from ..common import AttributedContainer, ContainerElementWrapper
from ..common.attributed_container import TemplatableMixin

"""
example usage:
:::opinion{template="personal"}
This is.. a warning!
:::

"""


class OpinionExtension(AttributedContainer, TemplatableMixin):
    def __init__(self) -> None:
        name = 'opinion'
        all_attributes = ['template', 'toggled']
        required_attributes = ['template']
        pushable_attributes = ['template']
        default_attributes = {'toggled': 'false'}

        self.template_values = {
            'default': {
                'icon': 'D',
                'description': 'This is an opinion, please note it may be biased.',
            },
            'personal': {
                'icon': 'P',
                'description': 'This is a personal opinion.',
            },
            'experience': {
                'icon': 'E',
                'description': 'This is an opinion coming from someone who has experienced XYZ.',
            }
        }

        super().__init__(name=name, all_attributes=all_attributes, required_attributes=required_attributes,
                         pushable_attributes=pushable_attributes, default_attributes=default_attributes)

    def push_internal_elements(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):
        token = state.push(f"{self.name}_header_open", "h1", 1)
        token.markup = self.markup
        token.map = [_.start_line, state.line]

        token = state.push("inline", "", 0)
        token.content = f'{self.get_template_value(attributes["template"][1:-1])["icon"]} {self.name}'
        token.map = [_.start_line, state.line]
        token.children = []

        token = state.push(f"{self.name}_header_close", "h1", -1)
        token.markup = self.markup

        self.push_content_elements(state, attributes, _)
