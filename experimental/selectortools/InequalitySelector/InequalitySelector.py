from abc import ABCMeta
from abc import abstractmethod
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
        from experimental import timespantools
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        Selector.__init__(self)
        self._inequality = inequality

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        return self._inequality
