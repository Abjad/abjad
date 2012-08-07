from abc import ABCMeta
from abc import abstractmethod
from experimental import helpertools
from experimental.selectortools.Selector import Selector


class SliceSelector(Selector):
    '''.. versionadded:: 1.0

    Abstract base class from which concrete slice selectors inherit.
    ''' 

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, start_identifier=None, stop_identifier=None):
        self._start_identifier = start_identifier
        self._stop_identifier = stop_identifier

    ### READ-ONLY PUBLIC PROPERTIES ###

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
    def stop_identifier(self):
        '''Slice selector stop identifier.

        Return integer, string, held expression or none.
        '''
        return self._stop_identifier
