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

    def _get_rhythm_region_commands(self):
        result = timespantools.TimespanInventory()
        for rhythm_region_command in self.score_specification.rhythm_region_commands:
            if not rhythm_region_command.expression == self:
                result.append(rhythm_region_command)
        return result

    def _evaluate(self):
        from experimental.tools import settingtools
        start_segment_identifier = self.offset.start_segment_identifier
        offset = self.offset._evaluate()
        timespan_inventory = self._get_rhythm_region_commands()
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = self.score_specification[start_segment_identifier]
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        assert isinstance(source_command, settingtools.RegionExpression)
        # TODO: the lack of symmtery between these two branches means either:
        #   that the call to self._apply_callbacks() is unnecessary, or
        #   that the call must appear in both branches.
        expression = source_command.expression
        if isinstance(expression, settingtools.RhythmMakerPayloadExpression):
            result = self._apply_callbacks(expression)
            # TODO: eventually return RhythmMakerPayloadExpression instead of rhythm-maker
            rhythm_maker = result.payload
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            return rhythm_maker
        elif isinstance(expression, settingtools.PayloadExpression):
            assert isinstance(expression.payload, str)
            # TODO: Do not return parseable string.
            #       Interpret parseable string, apply callbacks, and return expression instead. 
            return expression.payload
        else:
            raise TypeError(expression)
