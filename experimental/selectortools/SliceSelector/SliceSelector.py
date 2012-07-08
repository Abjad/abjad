from abc import ABCMeta
from abc import abstractmethod
from experimental.selectortools.Selector import Selector


class SliceSelector(Selector):
    '''.. versionadded:: 1.0

    Abstract base class from which concrete slice selectors inherit.
    ''' 

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, start=None, stop=None):
        self._start = start
        self._stop = stop

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def start(self):
        '''Start index of slice selector.

        Return integer, string, held expression or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Stop index of slice selector.

        Return integer, string, held expression or none.
        '''
        return self._stop
