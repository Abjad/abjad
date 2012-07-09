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

    ### PRIVATE METHODS ###

    def _process_contexts(self, contexts):
        from experimental import specificationtools
        if contexts is None:
            return contexts
        result = []
        for context in contexts:
            component_name = specificationtools.expr_to_component_name(context)
            result.append(component_name)
        return result

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
