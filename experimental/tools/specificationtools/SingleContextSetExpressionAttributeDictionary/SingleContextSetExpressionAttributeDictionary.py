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

    ### PUBLIC METHODS ###

    # TODO: remove in favor of self[attribute]
    def get_set_expression(self, attribute=None):
        #raise Exception('deprecated')
        set_expressions = self.get_set_expressions(attribute=attribute)
        if not set_expressions:
            raise Exception('no set expressions for {!r} found.'.format(attribute))
        elif 1 < len(set_expressions):
            raise Exception('multiple set expressions for {!r} found.'.format(attribute))
        assert len(set_expressions) == 1
        return set_expressions[0]

    # TODO: remove in favor of self[attribute]
    def get_set_expressions(self, attribute=None):
        #raise Exception('deprecated')
        result = []
        for key, value in self.iteritems():
            if attribute is None or key == attribute:
                result.extend(value)
        return result
