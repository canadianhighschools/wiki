"""
bulk of code forked from mdit_py_plugins.container_plugin
(to add a bit of flexibility over the usual import and keep it version independant)
"""

from markdown_it.rules_block import StateBlock
from ..common import AttributedContainer, ContainerElementWrapper
from ..common.attributed_container.data import push_attributes

"""
example usage:
:::callout{template="warning"}
This is.. a warning!
:::

"""


class LockExtension(AttributedContainer):
    def __init__(self) -> None:
        name = 'lock'
        all_attributes = ['*']
        required_attributes = []
        pushable_attributes = all_attributes
        default_attributes = {}

        super().__init__(name=name, all_attributes=all_attributes, required_attributes=required_attributes,
                         pushable_attributes=pushable_attributes, default_attributes=default_attributes)