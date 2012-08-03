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

    ### PRIVATE METHODS ###

    def _process_contexts(self, contexts):
        from experimental import selectortools
        if contexts is None:
            return contexts
        result = []
        for context in contexts:
            component_name = helpertools.expr_to_component_name(context)
            result.append(component_name)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

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
