from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import mathtools
from experimental.selectortools.Selector import Selector


class RatioPartSelector(Selector):
    r'''.. versionadded:: 1.0
    
    Abstract count-ratio selector class from which concrete count-ratio selectors inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, selector, ratio, part):
        ratio = mathtools.Ratio(ratio)
        self._selector = selector
        self._ratio = ratio
        self._part = part

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def part(self):
        '''Ratio-part selector part.

        Return integer.
        '''
        return self._part

    @property
    def ratio(self):
        '''Ratio-part selector ratio.

        Return ratio.
        '''
        return self._ratio

    @property
    def selector(self):
        '''Ratio-part selector selector.

        Return sliceable selector.
        '''
        return self._selector

    @property
    def segment_identifier(self):
        '''Delegate to ``self.selector.segment_identifier``.
        '''
        return self.selector.segment_identifier
