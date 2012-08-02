from abc import ABCMeta
from abc import abstractmethod
from experimental.selectortools.Selector import Selector


class TimespanSelector(Selector):
    r'''.. versionadded:: 1.0

    Timespan selector.
    '''
    
    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INTIALIZER ###

    @abstractmethod
    def __init__(self, timespan):
        from experimental import timespantools
        timespan = timespantools.expr_to_timespan(timespan)
        Selector.__init__(self)
        self._timespan = timespan

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def timespan(self):
        '''Timespan of inequality.
    
        Return timespan or none.
        '''
        return self._timespan
