"""
bulk of code forked from rules_block/header
(to add a bit of flexibility over the usual import and keep it version independant)
"""

from math import floor
from typing import Sequence, List

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock

from mdit_py_plugins.utils import is_code_block

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from ..common.base import MarkdownExtension
from ..common.attributed_container import ContainerElementWrapper

import re

from markdown_it.common.utils import isStrSpace

"""
example usage:
# This is @ Test!
hello. *world*

{part2}# Part 2
{~smol}## smaller

(please note: https://stackoverflow.com/questions/70579/html-valid-id-attribute-values)
[a-zA-Z]|[0-9]|-|_|:|.
->
<section id="This_is_@_Test!">
    <h1>This is @ Test!</h1>
    <p>hello. <i>world</i></p>
</section>

<section id="part2">
    <h1>Part 2</h1>
    <section id="~smol">
        <h2>smaller</h2>
    </section>
</section>
"""


class SectionElementWrapper:
    def __init__(self, start_line, end_line, section_end_line, level, title, slug) -> None:
        self.start_line = start_line
        self.end_line = end_line
        self.section_end_line = section_end_line
        self.level = level
        self.title = title
        self.slug = slug


class SectionExtension(MarkdownExtension):
    def __init__(self) -> None:
        name = 'section'

        self.start_pattern = r'^\s*(?:{(.+)?})?(#+)\s*(.+)$'
        self.chars = ['{', '#']
        self.parent_type = 'section'

        super().__init__(name=name)

    def plugin(self, md: MarkdownIt, *params):
        md.block.ruler.before(
            "fence",
            self.name,
            self.validate,
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
        if not state.src[start] in self.chars:
            return False

        m = re.match(self.start_pattern, state.src[start:maximum])

        if (not m):
            return False

        if (silent):
            return True

        level = len(m.group(2))
        title = m.group(3)
        _z = m.group(1)
        slug = _z if (_z) else re.sub(r"\s+", '-', title)

        section_end_line = self.find_next_section(state, start_line, end_line, level)

        _ = SectionElementWrapper(
            start_line,
            end_line,
            section_end_line,
            level,
            title,
            slug,
        )

        self.push_elements(state, _)

        return True

    def find_next_section(self, state: StateBlock, start_line: int, end_line: int, level: int) -> int:
        section_end_line = start_line

        # iterate till end
        while True:
            section_end_line += 1
            if (section_end_line > end_line): # beyond end
                break

            new_line_start = state.bMarks[section_end_line] + \
                state.tShift[section_end_line]
            new_line_end = state.eMarks[section_end_line]

            m = re.match(self.start_pattern,
                         state.src[new_line_start:new_line_end])

            # it is another valid section
            if (m != None):
                new_level = len(m.group(2))
                if (level >= new_level):
                    break

        return section_end_line

    def push_elements(self, state: StateBlock, _: SectionElementWrapper):
        _.markup = '#' * _.level
        # if a heading is ||surrounded|| like this, hide the heading
        _.hidden_slug = _.slug[:2] == '||' and _.slug[-2:] == '||'

        state.line = _.start_line + 1 # dont include the "# header" part

        # store previous parent (because new parent is this)
        _.old_parent = state.parentType
        _.old_line_max = state.lineMax

        state.parentType = self.parent_type
        state.lineMax = _.section_end_line - 1

        # distributed through functions to support overriding better
        self.push_open_element(state, _)

        self.push_internal_elements(state, _)

        self.push_close_element(state, _)

    def push_open_element(self, state: StateBlock, _: SectionElementWrapper):
        token = state.push(f"{self.name}_open", "section", 1)
        token.markup = _.markup
        token.block = True
        token.attrPush(("class", f"{self.name} {self.name}-level-{_.level}"))
        token.level = _.level
        token.content = _.title
        if (_.hidden_slug):
            token.info = 'hidden'
            token.attrPush(("id", _.slug[2:-2]))
        else:
            token.attrPush(("id", _.slug))

    def push_close_element(self, state: StateBlock, _: SectionElementWrapper):
        token = state.push(f"{self.name}_close", "section", -1)
        token.markup = _.markup
        token.block = True
        state.parentType = _.old_parent
        state.lineMax = _.old_line_max

    def push_internal_elements(self, state: StateBlock, _: SectionElementWrapper):
        if (not _.hidden_slug):
            token = state.push(f"{self.name}_header_open", f"h{_.level}", 1)
            token.markup = _.markup
            token.map = [_.start_line, state.line]

            token = state.push("inline", "", 0)
            token.content = _.title
            token.map = [_.start_line, state.line]
            token.children = []

            token = state.push(f"{self.name}_header_close", f"h{_.level}", -1)
            token.markup = _.markup

        self.push_content_elements(state, _)

    def push_content_elements(self, state: StateBlock, _: SectionElementWrapper):
        state.md.block.tokenize(state, _.start_line + 1,
                                _.section_end_line - 1)   