from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools.expressiontools.AttributeNameEnumeration import AttributeNameEnumeration


class SingleContextSetExpressionAttributeDictionary(AbjadObject, OrderedDict):
    '''Single-context set expression attribute dictionary.
    '''

    ### CLASS ATTRIBUTES ##

    attributes = AttributeNameEnumeration()

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        OrderedDict.__init__(self)
        for attribute in self.attributes:
            self[attribute] = expressiontools.SetExpressionInventory()

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)

    def __setitem__(self, key, value):
        assert isinstance(key, str), repr(key)
        assert isinstance(value, list), repr(value)
        OrderedDict.__setitem__(self, key, value)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return self.items()
