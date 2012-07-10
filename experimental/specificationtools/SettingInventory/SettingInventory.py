from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.specificationtools.Setting import Setting


class SettingInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    Setting inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Setting
