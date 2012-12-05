import abc
from abjad.tools import timerelationtools
from experimental.symbolictimetools.SliceSymbolicTimespan import SliceSymbolicTimespan


class TimeRelationSymbolicTimespan(SliceSymbolicTimespan):
    r'''.. versionadded:: 1.0

    Time relation symbolic timespan.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self, start_identifier=None, stop_identifier=None, voice_name=None, time_relation=None):
        SliceSymbolicTimespan.__init__(
            self, start_identifier=start_identifier, stop_identifier=stop_identifier, voice_name=voice_name)
        assert isinstance(time_relation, (timerelationtools.TimespanTimespanTimeRelation, type(None)))
        self._time_relation = time_relation

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def time_relation(self):
        '''Inequality of selector.
        
        Return time_relation or none.
        '''
        return self._time_relation

    @property
    def start_segment_identifier(self):
        '''Delegate to ``self.time_relation.start_segment_identifier``.

        Return string or none.
        '''
        return self.time_relation.start_segment_identifier
