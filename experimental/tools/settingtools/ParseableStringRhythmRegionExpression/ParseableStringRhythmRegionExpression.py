from abjad.tools import iotools
from abjad.tools import timespantools
from experimental.tools.settingtools.RhythmRegionExpression import RhythmRegionExpression


class ParseableStringRhythmRegionExpression(RhythmRegionExpression):
    '''Parseable string rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, parseable_string=None, voice_name=None, start_offset=None, total_duration=None):
        self._parseable_string = parseable_string
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._total_duration = total_duration

    ### PRIVATE METHODS ###

    def _evaluate(self):
        from experimental.tools import settingtools
        component = iotools.p(self.parseable_string)
        expression = settingtools.StartPositionedRhythmPayloadExpression(
            [component], start_offset=self.start_offset)
        stop_offset = self.start_offset + self.total_duration
        if expression.timespan.stops_before_offset(stop_offset):
            expression.repeat_to_stop_offset(stop_offset)
        elif expression.timespan.stops_after_offset(stop_offset):
            expression.set_offsets(stop_offset=stop_offset)
        expression._voice_name = self.voice_name
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def parseable_string(self):
        return self._parseable_string

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
