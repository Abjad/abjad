from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.settingtools.MultipleContextSetting import MultipleContextSetting


class MultipleContextSettingInventory(ObjectInventory):
    r'''.. versionadded:: 1.0

    MultipleContextSetting inventory.
    '''

    ### CLASS ATTRIBUTES ###

    attributes = AttributeNameEnumeration()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return MultipleContextSetting
