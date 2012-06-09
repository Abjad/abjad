from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from experimental.specificationtools.Directive import Directive


class DirectiveInventory(ObjectInventory):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Directive
