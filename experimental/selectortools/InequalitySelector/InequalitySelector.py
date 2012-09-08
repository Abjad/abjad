import abc
from experimental import timespaninequalitytools
from experimental.selectortools.Selector import Selector


class InequalitySelector(Selector):
    r'''.. versionadded:: 1.0

    Inequality selector.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INTIALIZER ###

    @abc.abstractmethod
    def __init__(self, inequality=None):
        assert isinstance(inequality, (timespaninequalitytools.TimespanInequality, type(None))), repr(inequality)
        Selector.__init__(self)
        self._inequality = inequality

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        '''Inequality of selector.
        
        Return timespan inequality or none.
        '''
        return self._inequality
