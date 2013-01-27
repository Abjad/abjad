from collections import OrderedDict
from abjad.tools.abctools.AbjadObject import AbjadObject


# TODO: Change to *have a* set expressions OrderedDict rather than *being an* OrderedDict.
#       This will mean adding a 'settings' property.
class ContextProxy(AbjadObject, OrderedDict):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        OrderedDict.__init__(self)
        self._division_payload_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._rhythm_payload_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_set_division_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_set_rhythm_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._voice_division_list = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return OrderedDict.__repr__(self)

    def __setitem__(self, key, value):
        assert isinstance(key, str)
        OrderedDict.__setitem__(self, key, value)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return self.items()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_payload_expressions(self):
        '''Context proxy division payload expressions.

        Return inventory.
        '''
        return self._division_payload_expressions

    @property
    def rhythm_payload_expressions(self):
        '''Context proxy rhythm payload expressions.

        Return inventory.
        '''
        return self._rhythm_payload_expressions

    @property
    def timespan_scoped_single_context_set_division_expressions(self):
        '''Context proxy timespan-scoped
        single-context set-division expressions.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_set_division_expressions

    @property
    def timespan_scoped_single_context_set_rhythm_expressions(self):
        '''Context proxy timespan-scoped
        single-context set-rhythm expressions.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_set_rhythm_expressions

    @property
    def voice_division_list(self):
        '''Context proxy voice division list.

        Return voice division list.
        '''
        return self._voice_division_list

    ### PUBLIC METHODS ###

    def get_set_expression(self, attribute=None):
        set_expressions = self.get_set_expressions(attribute=attribute)
        if not settings:
            raise Exception('no set expressions for {!r} found.'.format(attribute))
        elif 1 < len(settings):
            raise Exception('multiple set expressions for {!r} found.'.format(attribute))
        assert len(settings) == 1
        return settings[0]

    def get_set_expressions(self, attribute=None):
        result = []
        for key, value in self.iteritems():
            if attribute is None or key == attribute:
                result.extend(value)
        return result
