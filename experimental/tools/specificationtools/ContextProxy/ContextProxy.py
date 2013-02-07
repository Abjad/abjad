from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxy(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        # TODO: it's not at all clear that these need to be stored by attribute;
        #       maybe just store in SetExpressionInventory?
        self._single_context_set_expressions_by_attribute = \
            expressiontools.SingleContextSetExpressionAttributeDictionary()
        self._timespan_scoped_single_context_division_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_rhythm_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def single_context_set_expressions_by_attribute(self):
        '''Context proxy input set expressions by attribute.

        Return input set expression dictionary.
        '''
        return self._single_context_set_expressions_by_attribute

    @property
    def timespan_scoped_single_context_division_set_expressions(self):
        '''Context proxy timespan-scoped
        single-context division set expressions.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_division_set_expressions

    @property
    def timespan_scoped_single_context_rhythm_set_expressions(self):
        '''Context proxy timespan-scoped
        single-context rhythm set expressions.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_rhythm_set_expressions

    @property
    def timespan_scoped_single_context_set_expressions(self):
        '''Context proxy timespan-scoped
        single-context set expressions.

        Return inventory.
        '''
        return self._timespan_scoped_single_context_set_expressions
