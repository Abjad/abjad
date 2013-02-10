import copy
from abjad.tools import rhythmmakertools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.expressiontools.SetExpressionLookupExpression import SetExpressionLookupExpression


class RhythmSetExpressionLookupExpression(SetExpressionLookupExpression):
    '''Set-rhythm lookup expression.
    '''

    ### INITIALIZER ###

    def __init__(self, offset=None, voice_name=None, callbacks=None):
        SetExpressionLookupExpression.__init__(self, attribute='rhythm', 
            offset=offset, voice_name=voice_name, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        expression = self.offset.evaluate()
        if expression is None:
            return
        offset = expression.payload[0]
        timespan_inventory = self._get_timespan_scoped_single_context_set_expressions(self.attribute)
        time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_set_expressions = timespan_inventory.get_timespans_that_satisfy_time_relation(time_relation)
        source_expression_set_expression = \
            self.root_specification._get_first_expression_that_governs_context_name(
            candidate_set_expressions, self.voice_name)
        assert source_expression_set_expression is not None
        assert isinstance(source_expression_set_expression, expressiontools.TimespanScopedSingleContextSetExpression)
        expression = source_expression_set_expression.source_expression
        if isinstance(expression, expressiontools.RhythmMakerPayloadExpression):
            expression = self._apply_callbacks(expression)
            return expression
        elif isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression):
            # clone to prevent callbacks from inadvertantly changing source_expression expression
            expression = expression._clone()
            expression = self._apply_callbacks(expression)
            return expression
        else:
            raise TypeError(expression)
