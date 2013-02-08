from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxy(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        self._single_context_set_expressions_by_attribute = \
            expressiontools.AttributeDictionary()
        self._timespan_scoped_single_context_division_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_rhythm_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def single_context_set_expressions_by_attribute(self):
        '''Context proxy single-context set expressions by attribute.

        Return attribute dictionary.
        '''
        return self._single_context_set_expressions_by_attribute

    @property
    def timespan_scoped_single_context_division_set_expressions(self):
        '''Context proxy timespan-scoped
        single-context division set expressions.

        Return timespan-scoped single-context set expression inventory.
        '''
        return self._timespan_scoped_single_context_division_set_expressions

    @property
    def timespan_scoped_single_context_rhythm_set_expressions(self):
        '''Context proxy timespan-scoped
        single-context rhythm set expressions.

        Return timespan-scoped single-context set expression inventory.
        '''
        return self._timespan_scoped_single_context_rhythm_set_expressions
