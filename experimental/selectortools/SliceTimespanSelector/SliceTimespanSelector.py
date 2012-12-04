import abc
from experimental import helpertools
from experimental.selectortools.TimespanSelector import TimespanSelector


class SliceTimespanSelector(TimespanSelector):
    '''.. versionadded:: 1.0

    Abstract base class from which concrete slice selectors inherit.
    ''' 

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, start_identifier=None, stop_identifier=None, voice_name=None):
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier
        self._voice_name = voice_name

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def identifiers(self):
        '''Slice selector start- and stop-identifiers.

        Return pair.
        '''
        return self.start_identifier, self.stop_identifier
        
    @property
    def klass(self):
        '''Klass of slice selector.

        Return class or none.
        '''
        return self._klass

    @property
    def start_identifier(self):
        '''Slice selector start identifier.

        Return integer, string, held expression or none.
        '''
        return self._start_identifier

    @property
    def stop_identifier(self):
        '''Slice selector stop identifier.

        Return integer, string, held expression or none.
        '''
        return self._stop_identifier

    @property
    def voice_name(self):
        '''Slice selector voice name.

        If voice name is set then slice selector is "anchored" to a particular voice.

        If voice name is none then then slice selector is effectively "free floating"
        and is not anchored to a particular voice.

        Some documentation somewhere will eventually have to explain what it means
        for a selector to be "anchored" or "free floating".

        Return string or none.
        '''
        return self._voice_name
