import abc
from abjad.tools import timerelationtools
from experimental.selectortools.Selector import Selector


class InequalitySelector(Selector):
    r'''.. versionadded:: 1.0

    Inequality selector.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self, time_relation=None):
        assert isinstance(time_relation, (timerelationtools.TimespanTimespanTimeRelation, type(None)))
        Selector.__init__(self)
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
