from abjad.tools import introspectiontools
from experimental.selectortools.Selector import Selector


class BackgroundElementSelector(Selector):
    r'''.. versionadded:: 1.0

    Select one background object with mandatory `klass` and `index`.

    Select segment ``'red'``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> selectortools.BackgroundElementSelector(klass=specificationtools.Segment, index='red')
        BackgroundElementSelector(klass=specificationtools.Segment, index='red')

    Select segment ``0``::

        >>> selectortools.BackgroundElementSelector(klass=specificationtools.Segment, index=0)
        BackgroundElementSelector(klass=specificationtools.Segment, index=0)

    Select measure ``0``::

        >>> selectortools.BackgroundElementSelector(klass=measuretools.Measure, index=0)
        BackgroundElementSelector(klass=measuretools.Measure, index=0)

    Select division ``0``::

        >>> selectortools.BackgroundElementSelector(klass=specificationtools.Division, index=0)
        BackgroundElementSelector(klass=specificationtools.Division, index=0)

    More examples to follow.
    '''

    ### INITIALIZER ###
    
    def __init__(self, klass=None, inequality=None, index=0):
        from experimental import specificationtools
        from experimental import timespantools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(index, (int, str)), repr(index)
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        Selector.__init__(self)
        self._klass = klass
        self._index = index
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
