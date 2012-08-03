from abc import ABCMeta
from abc import abstractmethod
from experimental import helpertools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class BackgroundElementSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select zero or more contiguous background elements.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, klass, inequality=None, start=None, stop=None):
        from experimental import selectortools
        assert helpertools.is_background_element_klass(klass), repr(klass)
        SliceSelector.__init__(self, start=start, stop=stop)
        InequalitySelector.__init__(self, inequality=inequality)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        '''Background element class initialized by user.

        Return class.
        '''
        return self._klass
