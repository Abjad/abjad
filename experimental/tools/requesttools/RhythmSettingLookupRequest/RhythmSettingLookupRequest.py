import copy
from abjad.tools import rhythmmakertools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.requesttools.SettingLookupRequest import SettingLookupRequest


class RhythmSettingLookupRequest(SettingLookupRequest):
    '''Rhythm setting lookup request.
    '''

    ### INITIALIZER ###

    def __init__(self, voice_name, offset, payload_callbacks=None):
        SettingLookupRequest.__init__(self, 'rhythm', voice_name, offset,
            payload_callbacks=payload_callbacks)

    ### PUBLIC METHODS ###

    def _get_payload(self, score_specification, voice_name):
        from experimental.tools import requesttools
        from experimental.tools import settingtools
        requested_segment_identifier = self.offset.start_segment_identifier
        requested_offset = self.offset._get_offset(score_specification, voice_name)
        timespan_inventory = timespantools.TimespanInventory()
        for rhythm_region_command in score_specification.rhythm_region_commands:
            if not rhythm_region_command.request == self:
                timespan_inventory.append(rhythm_region_command)
        timespan_time_relation = timerelationtools.offset_happens_during_timespan(offset=requested_offset)
        candidate_commands = timespan_inventory.get_timespans_that_satisfy_time_relation(timespan_time_relation)
        segment_specification = score_specification[requested_segment_identifier]
        source_command = segment_specification._get_first_element_in_expr_by_parentage(
            candidate_commands, self.voice_name, include_improper_parentage=True)
        assert source_command is not None
        assert isinstance(source_command, settingtools.RegionCommand)
        # TODO: the lack of symmtery between these two branches means either:
        #   that the call to self._apply_payload_callbacks() is unnecessary, or
        #   that the call must appear in both branches.
        if isinstance(source_command.request, requesttools.RhythmMakerRequest):
            assert isinstance(source_command.request.payload, rhythmmakertools.RhythmMaker)
            rhythm_maker = copy.deepcopy(source_command.request.payload)
            rhythm_maker, start_offset = self._apply_payload_callbacks(
                rhythm_maker, source_command.timespan.start_offset)
            return rhythm_maker
        elif isinstance(source_command.request, requesttools.AbsoluteRequest):
            assert isinstance(source_command.request.payload, str)
            return source_command.request.payload
        else:
            raise TypeError(source_command.request)
