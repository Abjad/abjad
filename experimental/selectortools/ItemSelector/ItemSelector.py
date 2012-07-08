from abc import ABCMeta
from abc import abstractmethod
from experimental.selectortools.Selector import Selector


class ItemSelector(Selector):
    '''.. versionadded:: 1.0

    Abstract base class from which concrete item selectors inherit.
    '''

    ### INITIALIZER ##

    @abstractmethod
    def __init__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def index(self):
        '''Index of item selector.

        Return integer, string, held expression or none.
        '''
        return self._index
