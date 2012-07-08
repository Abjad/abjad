from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import mathtools
from experimental.selectortools.Selector import Selector


class RatioSelector(Selector):
    r'''.. versionadded:: 1.0
    
    Abstract count-ratio selector class from which concrete count-ratio selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, reference, ratio):
        assert self._interprets_as_sliceable_selector(reference), repr(reference)
        ratio = mathtools.Ratio(ratio)
        self._reference = reference
        self._ratio = ratio

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def ratio(self):
        '''Ratio of count-ratio selector.

        Return ratio.
        '''
        return self._ratio

    @property
    def reference(self):
        '''Reference of count-ratio selector.

        Return voice name or sliceable selector.
        '''
        return self._reference
