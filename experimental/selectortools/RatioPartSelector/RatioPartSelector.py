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
    def __init__(self, reference, ratio, part):
        ratio = mathtools.Ratio(ratio)
        self._reference = reference
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
        '''Ratio of count-ratio selector.

        Return ratio.
        '''
        return self._ratio

    # TODO: perhaps change name to 'self.selector'?
    @property
    def reference(self):
        '''Reference of count-ratio selector.

        Return sliceable selector.
        '''
        return self._reference

    @property
    def segment_identifier(self):
        '''Delegate to ``self.reference.segment_identifier``.
        '''
        return self.reference.segment_identifier
