import abc
from abjad.tools import timerelationtools
from experimental.symbolictimetools.Selector import Selector


class TimeRelationSymbolicTimespan(Selector):
    r'''.. versionadded:: 1.0

    Time relation symbolic timespan.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    def __init__(self, 
        anchor=None, start_identifier=None, stop_identifier=None, voice_name=None, time_relation=None):
        from experimental import symbolictimetools
        assert isinstance(anchor, (symbolictimetools.SymbolicTimespan, str, type(None))), repr(anchor)
        assert isinstance(voice_name, (str, type(None))), repr(voice_name)
        assert isinstance(time_relation, (timerelationtools.TimespanTimespanTimeRelation, type(None)))
        self._anchor = anchor
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier
        self._voice_name = voice_name
        self._time_relation = time_relation

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return self._anchor

    @property
    def identifiers(self):
        '''Slice selector start- and stop-identifiers.

        Return pair.
        '''
        return self.start_identifier, self.stop_identifier

    @property
    def start_identifier(self):
        '''Slice selector start identifier.

        Return integer, string, held expression or none.
        '''
        return self._start_identifier

    @property
    def start_segment_identifier(self):
        '''Return anchor when anchor is a string.

        Otherwise delegate to ``self.time_relation.start_segment_identifier``.

        Return string or none.
        '''
        if isinstance(self.anchor, str):
            return self.anchor
        else:
            return self.anchor.start_segment_identifier

    @property
    def stop_identifier(self):
        '''Slice selector stop identifier.

        Return integer, string, held expression or none.
        '''
        return self._stop_identifier

    @property
    def time_relation(self):
        '''Inequality of selector.
        
        Return time_relation or none.
        '''
        return self._time_relation

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

    ### PUBLIC METHODS ###

    @abc.abstractproperty
    def get_offsets(self):
        pass
