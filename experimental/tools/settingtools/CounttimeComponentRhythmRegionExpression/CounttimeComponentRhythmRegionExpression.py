from abjad.tools import componenttools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.FinalizedRhythmRegionExpression import FinalizedRhythmRegionExpression


# TODO: maybe inherit from SelectorRhythmRegionExpression?
class CounttimeComponentRhythmRegionExpression(FinalizedRhythmRegionExpression):
    '''Counttime component rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(self, payload=None, voice_name=None, start_offset=None, total_duration=None):
        self._payload = payload
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        result = settingtools.StartPositionedRhythmPayloadExpression(
            [], start_offset=self.start_offset, voice_name=self.voice_name)
        wrapped_component = componenttools.copy_components_and_covered_spanners([self.payload])[0]
        result._payload = wrapped_component
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        assert not keep_timespan.starts_before_timespan_starts(result.timespan), repr((result.timespan, keep_timespan))
        assert result.timespan.start_offset == keep_timespan.start_offset, repr((result.timespan, keep_timespan))
        result = result & keep_timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1
        result = result[0]
        assert isinstance(result, settingtools.StartPositionedRhythmPayloadExpression), repr(result)
        result.repeat_to_stop_offset(stop_offset)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def payload(self):
        return self._payload

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
