from abc import ABCMeta
from abc import abstractmethod
from experimental.selectortools.Selector import Selector


class ItemSelector(Selector):
    '''.. versionadded:: 1.0

    Abstract base class from which concrete item selectors inherit.
    '''

    ### INITIALIZER ##

    @abstractmethod
    def __init__(self, identifier=None):
        assert isinstance(identifier, (int, str, type(None))), repr(identifier)
        self._identifier = identifier

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def identifier(self):
        '''Item selector identifier.

        Return integer, string, held expression or none.
        '''
        return self._identifier
