"""
bulk of code forked from mdit_py_plugins.container_plugin
(to add a bit of flexibility over the usual import and keep it version independant)
"""

from markdown_it.rules_block import StateBlock
from ..common import AttributedContainer, ContainerElementWrapper
from ..common.attributed_container import TemplatableMixin

"""
example usage:
:::callout{template="warning"}
This is.. a warning!
:::

"""

class CalloutExtension(AttributedContainer, TemplatableMixin):

    def __init__(self) -> None:
        name = 'callout'
        all_attributes = ['template', 'toggled']
        required_attributes = ['template']
        pushable_attributes = ['template']
        default_attributes = {'toggled': 'false'}

        self.template_values = {
        'default': {
            'icon': 'C',
        },
        'warning': {
            'icon': 'W',
        },
        'info': {
            'icon': 'I',
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
        