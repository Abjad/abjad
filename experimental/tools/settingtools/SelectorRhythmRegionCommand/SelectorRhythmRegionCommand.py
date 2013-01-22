from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.FinalizedRhythmRegionCommand import FinalizedRhythmRegionCommand


class SelectorRhythmRegionCommand(FinalizedRhythmRegionCommand):
    '''Selector rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, voice_name=None, start_offset=None, total_duration=None):
        self._selector = selector
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification, voice_name=None):
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        result = self.selector._evaluate(score_specification)
        if result is None:
            return
        result._start_offset = self.start_offset
        start_offset, stop_offset = self.start_offset, self.start_offset + self.total_duration
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        assert not keep_timespan.starts_before_timespan_starts(result.timespan), repr((result.timespan, keep_timespan))
        assert result.timespan.start_offset == keep_timespan.start_offset, repr((result.timespan, keep_timespan))
        result = result & keep_timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1
        result = result[0]
        assert isinstance(result, settingtools.StartPositionedRhythmProduct), repr(result)
        result.repeat_to_stop_offset(stop_offset)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def selector(self):
        return self._selector

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name

    ### PUBLIC METHODS ###

    def prolongs_expr(self, expr):
        if isinstance(expr, type(self)):
            if self.selector == expr.selector:
                return True
        return False
