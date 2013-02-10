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
        '''Region expression source.
        
        Return expression.
        '''
        return self._source

    @property
    def start_offset(self):
        '''Region expression start offset.

        Return offset.
        '''
        return self._start_offset

    @property
    def total_duration(self):
        '''Region expression total duration.

        Return duration.
        '''
        return self._total_duration

    @property
    def voice_name(self):
        '''Region expression voice name.
    
        Return string.
        '''
        return self._voice_name
