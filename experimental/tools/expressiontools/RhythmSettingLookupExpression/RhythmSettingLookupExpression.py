import copy
from abjad.tools import rhythmmakertools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.expressiontools.SettingLookupExpression import SettingLookupExpression


class RhythmSettingLookupExpression(SettingLookupExpression):
    '''Rhythm setting lookup.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookupExpression.__init__(self, attribute='rhythm', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PRIVATE METHODS ###

    def _get_timespan_scoped_single_context_rhythm_settings(self):
        result = timespantools.TimespanInventory()
        for timespan_scoped_single_context_rhythm_setting in self.score_specification.timespan_scoped_single_context_rhythm_settings:
            if not timespan_scoped_single_context_rhythm_setting.expression == self:
                result.append(timespan_scoped_single_context_rhythm_setting)
        return result

    ### PUBLIC METHODS ###

    def evaluate(self):
        from experimental.tools import expressiontools
        start_segment_identifier = self.offset.start_segment_identifier
        expression = self.offset.evaluate()
        offset = expression.payload[0]
        timespan_inventory = self._get_timespan_scoped_single_context_rhythm_settings()
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = self.score_specification[start_segment_identifier]
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        assert isinstance(source_command, expressiontools.TimespanScopedSingleContextSetting)
        expression = source_command.expression
        if isinstance(expression, expressiontools.RhythmMakerPayloadExpression):
            expression = self._apply_callbacks(expression)
            return expression
        elif isinstance(expression, expressiontools.StartPositionedRhythmPayloadExpression):
            # clone to prevent callbacks from inadvertantly changing source expression
            expression = expression._clone()
            expression = self._apply_callbacks(expression)
            return expression
        else:
            raise TypeError(expression)
