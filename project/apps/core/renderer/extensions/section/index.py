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

from ..common import get_tag_data

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

def render(
    self: RendererProtocol,
    tokens: Sequence[Token],
    idx: int,
    _options: OptionsDict,
    env: EnvType,
) -> str:
    return self.renderToken(tokens, idx, _options, env)


def execute(
    md: MarkdownIt,
    name: str = 'section'
) -> None:
    

    def find_next_section(state: StateBlock, start_line: int, end_line: int) -> int:
        next_line = start_line

        # iterate till end
        while True:
            next_line += 1
            if next_line >= end_line:
                break

            
            new_line_start = state.bMarks[next_line] + state.tShift[next_line]
            new_line_end = state.eMarks[next_line]

            m = match_section(state.src[new_line_start:new_line_end])

            # it is another valid section
            if (m != None): break

        return next_line
    

    def match_section(s):
        pattern = r'^\s*(?:{(.+)?})?(#+)\s*(.+)$'
        return re.match(pattern, s)


    def section_func(
        state: StateBlock, start_line: int, end_line: int, silent: bool
    ) -> bool:
        pos = state.bMarks[start_line] + state.tShift[start_line]
        maximum = state.eMarks[start_line]

        # stop if code block or position is out of maximum (i think it means its blank?)
        if (state.is_code_block(start_line) or pos >= maximum):
            return False
        

        m = match_section(state.src[pos:maximum])
        if (m):
            level = len(m.group(2))
            title = m.group(3)
            z = m.group(1)
            slug: str = z if (z) else re.sub(r"\s+", '-', title)
    
            if (silent): return True

            state.line = start_line + 1

            markup = '#' * level


            hidden_slug = slug[:2] == '__' and slug[-2:] == '__'

            token = state.push(f"{name}_open", "section", 1)
            token.markup = markup
            token.map = [start_line, state.line]
            token.attrPush(("id", slug))
            token.level = level
            token.content = title
            if (hidden_slug): token.info = 'hidden'
            
            # header (only renders if slug is not hidden)

            if (not hidden_slug):
                token = state.push(f"{name}_header_open", "h" + str(level), 1)
                token.markup = markup
                token.map = [start_line, state.line]

                token = state.push("inline", "", 0)
                token.content = title
                token.map = [start_line, state.line]
                token.children = []

                token = state.push(f"{name}_header_close", "h" + str(level), -1)
                token.markup = markup

            # content (till next section) is placed in here
            next_line = find_next_section(state, start_line, end_line)
            state.md.block.tokenize(state, start_line+1, next_line)

            token = state.push(f"{name}_header_close", "section", -1)
            token.markup = markup

            return True
        return False


    md.block.ruler.before(
        "fence",
        name,
        section_func
    )
    md.add_render_rule(f"{name}_open", render)
    md.add_render_rule(f"{name}_close", render)