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

from .common import get_tag_data

"""
example usage:
:::callout{template="warning"}
This is.. a warning!
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


def callout_plugin(
    md: MarkdownIt,
    name: str = 'callout',
    marker: str = ":",
    templates: dict = {'warning': '⚠️'}
) -> None:

    min_markers = 3
    marker_char = marker[0]
    marker_len = len(marker)

    def callout_func(
        state: StateBlock, startLine: int, endLine: int, silent: bool
    ) -> bool:
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

        tag_data = get_tag_data(tag)
        if (not tag_data): return False
        attributes = tag_data['attributes']
        
        if (attributes == {}): return False
        if (silent): return True

        if (not 'template' in attributes): return False
        template = attributes['template']



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
        state.parentType = name

        # this will prevent lazy continuations from ever going past our end marker
        state.lineMax = nextLine

        # add divs
        # main
        token = state.push(f"{name}_open", "div", 1)
        token.markup = marker
        token.block = True
        token.attrPush(("class", f"callout {name}-style-{template}"))

        # icon wrapper
        token = state.push(f"{name}_{template}_icon_wrapper_open", "div", 1)
        token.block = True
        token.attrPush(("class", f"{name}-icon-wrapper"))

        # icon
        t = attributes['template']
        if (t in templates):
            token = state.push(f"{name}_{template}_icon", "p", 1)
            token.block = True
            token.attrPush(("class", f"{name}-icon {name}-style-{template}-icon"))

            token = state.push(f"text", "", 0)
            token.content = templates[t]

            token = state.push(f"{name}_{template}_icon", "p", -1)
            token.block = True


        token = state.push(f"{name}_{template}_icon_wrapper_close", "div", -1)
        token.block = True

        # content wrapper
        token = state.push(f"{name}_{template}_content_wrapper_open", "div", 1)
        token.block = True
        token.attrPush(("class", f"{name}-content-wrapper"))

        # content
        state.md.block.tokenize(state, startLine + 1, nextLine)

        token = state.push(f"{name}_{template}_content_wrapper_close", "div", -1)
        token.block = True

        # end
        token = state.push(f"{name}_close", "div", -1)
        token.markup = state.src[start:pos]
        token.block = True
        state.parentType = old_parent
        state.lineMax = old_line_max
        state.line = nextLine + (1 if auto_closed else 0)

        return True


    md.block.ruler.before(
        "fence",
        name,
        callout_func
    )
    md.add_render_rule(f"{name}_open", render)
    md.add_render_rule(f"{name}_close", render)