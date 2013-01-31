from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject


class SingleContextSetExpressionAttributeDictionary(AbjadObject, OrderedDict):
    '''Single-context set expression attribute dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self):
        OrderedDict.__init__(self)

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
