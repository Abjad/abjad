from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import introspectiontools
from experimental.selectortools.ItemSelector import ItemSelector


class BackgroundElementSelector(ItemSelector):
    r'''.. versionadded:: 1.0

    Select exactly one background element.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = ABCMeta

    ### INITIALIZER ###
    
    @abstractmethod
    def __init__(self, klass=None, inequality=None, index=0):
        from experimental import specificationtools
        from experimental import timespantools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        ItemSelector.__init__(self, index=index)
        self._klass = klass
        self._inequality = inequality

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
    def inequality(self):
        '''Background element selector inequality initialized by user.

        Value of none is taken equal to the timespan of the entire score.

        Return timespan inequality or none.
        '''
        return self._inequality

    @property
    def klass(self):
        '''Background element selector class initialized by user.

        Return segment, measure or division class.
        '''
        return self._klass
