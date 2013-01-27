import abc
from abjad.tools import durationtools
from experimental.tools.expressiontools.Expression import Expression


class RegionExpression(Expression):
    '''Region expression.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    # TODO: change to self.__init__(payload, timespan, voice_name)
    def __init__(self, payload=None, start_offset=None, total_duration=None, voice_name=None):
        assert isinstance(voice_name, str), repr(voice_name)
        start_offset = durationtools.Offset(start_offset)
        total_duration = durationtools.Duration(total_duration)
        self._payload = payload
        self._start_offset = start_offset
        self._total_duration = total_duration
        self._voice_name = voice_name

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
