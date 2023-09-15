"""
bulk of code forked from mdit_py_plugins.container_plugin
(to add a bit of flexibility over the usual import and keep it version independant)
"""

from math import floor
from typing import Sequence

from markdown_it import MarkdownIt
from markdown_it.rules_block import StateBlock

from mdit_py_plugins.utils import is_code_block

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from ..common import get_tag_data

"""
example usage:
:::lock[grades="9,12" districts="peel"]
This message is only avaliable to those who have set the above filter targets.
They will still recieve - as an example: "89 words hidden based on your filters" - at the bottom.
:::

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
    marker: str = ":",
    default_attributes: dict = {}
) -> None:

    min_markers = 3
    marker_char = marker[0]
    marker_len = len(marker)

    def lock_func(
        state: StateBlock, startLine: int, endLine: int, silent: bool
    ):
        if is_code_block(state, startLine):
            return False

        auto_closed = False
        start = state.bMarks[startLine] + state.tShift[startLine]
        maximum = state.eMarks[startLine]

        # Check out the first character quickly,
        # this should filter out most of non-callouts
        if marker_char != state.src[start]:
            return False

        # Check out the rest of the marker string
        pos = start + 1
        while pos <= maximum:
            try:
                character = state.src[pos]
            except IndexError:
                break
            if marker[(pos - start) % marker_len] != character:
                break
            pos += 1

        marker_count = floor((pos - start) / marker_len)
        if marker_count < min_markers:
            return False
        pos -= (pos - start) % marker_len

        tag = state.src[pos:maximum].strip()

        tag_data = get_tag_data(tag, default_attributes)
        if (not tag_data): return False
        attributes = tag_data['attributes']
        
        if (attributes == {}): return False
        if (silent): return True

        # Search for the end of the block
        nextLine = startLine

        while True:
            nextLine += 1
            if nextLine >= endLine:
                # unclosed block should be autoclosed by end of document.
                # also block seems to be autoclosed by end of parent
                break

            start = state.bMarks[nextLine] + state.tShift[nextLine]
            maximum = state.eMarks[nextLine]

            if start < maximum and state.sCount[nextLine] < state.blkIndent:
                # non-empty line with negative indent should stop the list:
                # - ```
                #  test
                break

            if marker_char != state.src[start]:
                continue

            if is_code_block(state, nextLine):
                continue

            pos = start + 1
            while pos <= maximum:
                try:
                    character = state.src[pos]
                except IndexError:
                    break
                if marker[(pos - start) % marker_len] != character:
                    break
                pos += 1

            # closing code fence must be at least as long as the opening one
            if floor((pos - start) / marker_len) < marker_count:
                continue

            # make sure tail has spaces only
            pos -= (pos - start) % marker_len
            pos = state.skipSpaces(pos)

            if pos < maximum:
                continue

            # found!
            auto_closed = True
            break

        old_parent = state.parentType
        old_line_max = state.lineMax
        state.parentType = "lock"

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = nextLine


        # main
        token = state.push(f"lock_open", "div", 1)
        token.markup = marker
        token.block = True

        s = "lock"
        for k, v in attributes.items():
            s += f" lock-{k}"

            targets = v.split(',')
            for t in targets:
                s += f" lock-{k}-{t}"
        
        token.attrPush(("class", s))

        # content
        state.md.block.tokenize(state, startLine+1, nextLine)

        # end
        token = state.push(f"lock_close", "div", -1)
        token.markup = state.src[start:pos]
        token.block = True
        state.parentType = old_parent
        state.lineMax = old_line_max
        state.line = nextLine + (1 if auto_closed else 0)

        return True


    md.block.ruler.before(
        "fence",
        "lock",
        lock_func
    )
    md.add_render_rule(f"lock_open", render)
    md.add_render_rule(f"lock_close", render)