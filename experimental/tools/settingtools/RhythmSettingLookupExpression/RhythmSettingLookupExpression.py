import copy
from abjad.tools import rhythmmakertools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.SettingLookupExpression import SettingLookupExpression


class RhythmSettingLookupExpression(SettingLookupExpression):
    '''Rhythm setting lookup.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookupExpression.__init__(self, attribute='rhythm', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        start_segment_identifier = self.offset.start_segment_identifier
        expression = self.offset._evaluate()
        offset = expression.payload[0]
        timespan_inventory = self._get_rhythm_region_expressions()
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = self.score_specification[start_segment_identifier]
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        assert isinstance(source_command, settingtools.TimespanScopedSingleContextSetting)
        expression = source_command.expression
        if isinstance(expression, settingtools.RhythmMakerPayloadExpression):
            expression = self._apply_callbacks(expression)
            return expression
        elif isinstance(expression, settingtools.StartPositionedRhythmPayloadExpression):
            # clone to prevent callbacks from inadvertantly changing source expression
            expression = expression._clone()
            expression = self._apply_callbacks(expression)
            return expression
        else:
            raise TypeError(expression)

    def _get_rhythm_region_expressions(self):
        result = timespantools.TimespanInventory()
        for rhythm_region_expression in self.score_specification.rhythm_region_expressions:
            if not rhythm_region_expression.expression == self:
                result.append(rhythm_region_expression)
        return result
