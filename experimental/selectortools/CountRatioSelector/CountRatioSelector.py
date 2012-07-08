from abjad.tools import mathtools
from experimental.selectortools.Selector import Selector


class CountRatioSelector(Selector):
    r'''.. versionadded:: 1.0
    
    Partition `reference` by `ratio`. Then select exactly one part.

    Count ratio selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, index):
        assert self._interprets_as_sliceable_selector(reference), repr(reference)
        ratio = mathtools.Ratio(ratio)
        assert isinstance(index, int), repr(index)
        self._reference = reference
        self._ratio = ratio
        self._index = index

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def index(self):
        '''Index of count-ratio selector.

        Return integer.
        '''
        return self._index

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
        self._reference
