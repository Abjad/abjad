from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import introspectiontools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.ItemSelector import ItemSelector


class BackgroundElementSelector(ItemSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select exactly one background element.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###
    
    @abstractmethod
    def __init__(self, klass=None, inequality=None, index=0):
        from experimental import selectortools
        assert selectortools.is_background_element_klass(klass), repr(klass)
        ItemSelector.__init__(self, index=index)
        InequalitySelector.__init__(self, inequality=inequality)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.klass == expr.klass:
                if self.index == expr.index:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def index(self):
        '''Background element selector index initialized by user.

        Return integer or string.
        '''
        return self._index

    @property
    def klass(self):
        '''Background element selector class initialized by user.

        Return segment, measure or division class.
        '''
        return self._klass
