import abc
from abjad.tools import durationtools
from experimental.tools.expressiontools.Expression import Expression


class RegionExpression(Expression):
    '''Region expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, source=None, start_offset=None, total_duration=None, voice_name=None):
        assert isinstance(voice_name, str), repr(voice_name)
        start_offset = durationtools.Offset(start_offset)
        total_duration = durationtools.Duration(total_duration)
        self._source = source
        self._start_offset = start_offset
        self._total_duration = total_duration
        self._voice_name = voice_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
