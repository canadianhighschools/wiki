"""
bulk of code forked from mdit_py_plugins.container_plugin
(to add a bit of flexibility over the usual import and keep it version independant)
"""

import re
from typing import Optional

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock

from mdit_py_plugins.utils import is_code_block

from .data import get_tag_data, are_attributes_valid, push_attributes

from ..base import MarkdownExtension

"""
example usage:
:::name[key="value"]
Internal contents
:::
"""

class ContainerElementWrapper:
    def __init__(self, start_line, end_line, container_end_line) -> None:
        self.start_line = start_line
        self.end_line = end_line
        self.container_end_line = container_end_line


class AttributedContainer(MarkdownExtension):
    def __init__(self, name, markup=':::', all_attributes=[], required_attributes=[], pushable_attributes=[], default_attributes={}) -> None:
        super().__init__(name=name)

        self.markup = ':::'
        self.char = markup[0]
        self.all_attributes = all_attributes
        self.required_attributes = required_attributes
        self.pushable_attributes = pushable_attributes
        self.default_attributes = default_attributes
        self.parent_type = 'formatblock'

        self.validate_patterns()

        self.start_pattern = re.compile(r'^' + self.markup + self.name + r'(?:{(.+)})?$')
        self.end_pattern = re.compile(r'^' + self.markup + r'$')

    def validate_patterns(self):
        for k in self.default_attributes.keys():
            if (k in self.required_attributes):
                assert ValueError("Default attribute cannot be required attribute!")
                
        for i in self.all_attributes:
            if (i == '*'): break # wildcard
            if (not i in self.required_attributes and not i in self.default_attributes):
                assert ValueError("Attribute must be either default or required!")


    def plugin(self, md: MarkdownIt):
        md.block.ruler.before(
            "fence",
            self.name,
            self.validate
        )
        md.add_render_rule(f"{self.name}_open", self.render)
        md.add_render_rule(f"{self.name}_close", self.render)


    def pre_logic(self, state: StateBlock, start_line: int, end_line: int, silent: bool) -> bool:
        if (is_code_block(state, start_line)):
            return False
        return True


    def validate(self, state: StateBlock, start_line: int, end_line: int, silent: bool) -> bool:
        if (not self.pre_logic(state, start_line, end_line, silent)):
            return False
    
        start = state.bMarks[start_line] + state.tShift[start_line]
        maximum = state.eMarks[start_line]

        # check if first character matches before applying regex for optimization reasons
        if self.char != state.src[start]:
            return False


        m = re.match(self.start_pattern, state.src[start:maximum])

        if (not m):
            return False

        # attributes (if any)
        unformatted_attributes = m.group(1)
        attributes = get_tag_data(unformatted_attributes, self.default_attributes, self.all_attributes)

        if (not are_attributes_valid(attributes, self.required_attributes)):
            return False

        if (silent):
            return True


        # get to the end of the container
        container_end_line = start_line
        while True:
            container_end_line += 1
            
            if (container_end_line > end_line):
                break

            start = state.bMarks[container_end_line] + state.tShift[container_end_line]
            maximum = state.eMarks[container_end_line]

            # blank line
            if (start == maximum):
                continue

            if (self.char == state.src[start]):
                m = re.match(self.end_pattern, state.src[start:maximum])
                if (m):
                    break

        wrapper = ContainerElementWrapper(start_line, end_line, container_end_line)
        self.push_elements(state, attributes, wrapper)

        return True


    def push_elements(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):        
        # store previous parent (because new parent is this)
        _.old_parent = state.parentType
        _.old_line_max = state.lineMax

        state.parentType = self.parent_type
        state.lineMax = _.container_end_line

        # distributed through functions to support overriding better
        self.push_open_element(state, attributes, _)

        self.push_internal_elements(state, attributes, _)

        self.push_close_element(state, attributes, _)

    def push_open_element(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):
        token = state.push(f"{self.name}_open", "div", 1)
        token.markup = self.markup
        token.block = True
        token.attrPush(("class", f"{self.name}"))
        push_attributes(token, self.name, attributes, self.pushable_attributes)

    def push_close_element(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):
        token = state.push(f"{self.name}_close", "div", -1)
        token.markup = self.markup
        token.block = True
        state.parentType = _.old_parent
        state.lineMax = _.old_line_max
        state.line = _.container_end_line + 1


    def push_internal_elements(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):
        self.push_content_elements(state, attributes, _)

    def push_content_elements(self, state: StateBlock, attributes: dict, _: ContainerElementWrapper):
        state.md.block.tokenize(state, _.start_line + 1, _.container_end_line - 1)


class TemplatableMixin:
    primary_key = 'template'
    default_template_key = 'default'
    # implement this or it will throw an error
    # dont wanna do anything too complicated right now so just pretending it exists works
    # template_values = {}

    def get_template_value(self, t) -> Optional[str]:
        if (t in self.template_values):
            return self.template_values[t]
        return self.template_values[self.default_template_key]