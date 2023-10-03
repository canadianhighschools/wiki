import re

from typing import Sequence

from markdown_it import MarkdownIt

from markdown_it.renderer import RendererProtocol
from markdown_it.token import Token
from markdown_it.utils import EnvType, OptionsDict

from markdown_it.rules_block import StateBlock

try:
    from config.renderer import TAG_PREFIX, TAG_VALUES
except ImportError:
    TAG_PREFIX = '#'
    TAG_VALUES = {}

def is_tag(s):
    return s[:len(TAG_PREFIX)] == TAG_PREFIX

def substitute_tag_or_return(s) -> str:
    if (is_tag(s)):
        tag = s[len(TAG_PREFIX):]
        if (tag in TAG_VALUES):
            return TAG_VALUES[tag]
    return s


def split_attribute(s):
    return re.split(r' ?, ?', s)


class MarkdownExtension:
    def __init__(self, name) -> None:
        self.name = name

    def plugin(md: MarkdownIt, *params):
        pass

    def validate(self, state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
        pass

    def render(
        renderer: RendererProtocol,
        tokens: Sequence[Token],
        idx: int,
        _options: OptionsDict,
        env: EnvType,
    ) -> str:
        return renderer.renderToken(tokens, idx, _options, env)