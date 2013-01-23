import copy
from abjad.tools import rhythmmakertools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.settingtools.SettingLookup import SettingLookup


class RhythmSettingLookup(SettingLookup):
    '''Rhythm setting lookup.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name=None, offset=None, callbacks=None):
        SettingLookup.__init__(self, attribute='rhythm', voice_name=voice_name, 
            offset=offset, callbacks=callbacks)

    ### PUBLIC METHODS ###

    def _evaluate(self, score_specification):
        from experimental.tools import settingtools
        start_segment_identifier = self.offset.start_segment_identifier
        offset = self.offset._evaluate(score_specification)
        timespan_inventory = timespantools.TimespanInventory()
        for rhythm_region_command in score_specification.rhythm_region_commands:
            if not rhythm_region_command.expression == self:
                timespan_inventory.append(rhythm_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = score_specification[start_segment_identifier]
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        assert isinstance(source_command, settingtools.RegionCommand)
        # TODO: the lack of symmtery between these two branches means either:
        #   that the call to self._apply_callbacks() is unnecessary, or
        #   that the call must appear in both branches.
        if isinstance(source_command.expression, settingtools.RhythmMakerExpression):
            result = self._apply_callbacks(source_command.expression)
            # TODO: eventually return RhythmMakerExpression instead of rhythm-maker
            rhythm_maker = result.payload
            assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
            return rhythm_maker
        elif isinstance(source_command.expression, settingtools.AbsoluteExpression):
            assert isinstance(source_command.expression.payload, str)
            return source_command.expression.payload
        else:
            raise TypeError(source_command.expression)
