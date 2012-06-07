from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from specificationtools.AttributeNameEnumeration import AttributeNameEnumeration
from specificationtools.Directive import Directive


class DirectiveInventory(ObjectInventory):

    ### CLASS ATTRIBUTES ###

    attribute_names = AttributeNameEnumeration()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _item_callable(self):
        return Directive
