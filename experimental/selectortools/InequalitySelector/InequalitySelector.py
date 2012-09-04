from abc import ABCMeta
from abc import abstractmethod
from experimental import timespantools
from experimental.selectortools.Selector import Selector


class InequalitySelector(Selector):
    r'''.. versionadded:: 1.0

    Inequality selector.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INTIALIZER ###

    @abstractmethod
    def __init__(self, inequality=None):
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        Selector.__init__(self)
        self._inequality = inequality

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        '''Inequality of selector.
        
        Return timespan inequality or none.
        '''
        return self._inequality
