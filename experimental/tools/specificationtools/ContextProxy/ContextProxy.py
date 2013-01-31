from abjad.tools import timespantools
from abjad.tools.abctools.AbjadObject import AbjadObject


class ContextProxy(AbjadObject):

    ### INITIALIZER ###

    def __init__(self):
        from experimental.tools import expressiontools
        from experimental.tools import specificationtools
        self._division_payload_expressions = \
            timespantools.TimespanInventory()
        self._single_context_set_expressions_by_attribute = \
            specificationtools.SingleContextSetExpressionAttributeDictionary()
        self._rhythm_payload_expressions = \
            timespantools.TimespanInventory()
        self._timespan_scoped_single_context_division_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        self._timespan_scoped_single_context_rhythm_set_expressions = \
            expressiontools.TimespanScopedSingleContextSetExpressionInventory()
        # TODO: maybe add self._timespan_scoped_single_context_set_expressions inventory?
        self._voice_division_list = None

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
    def voice_division_list(self):
        '''Context proxy voice division list.

        Return voice division list.
        '''
        return self._voice_division_list
