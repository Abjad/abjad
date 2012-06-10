from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class PartIndicator(AbjadObject):
    r'''.. versionadded:: 1.0

    Indicate ratio of a partition and chosen part or parts of the partition.

    Initialize from ratio and integer::

        >>> from experimental import specificationtools

    ::

        >>> specificationtools.PartIndicator((1, 2, 1), 0)
        PartIndicator(Ratio(1, 2, 1), 0)

    Initialize from ratio and slice::

        >>> specificationtools.PartIndicator((1, 2, 1), slice(0, 1))
        PartIndicator(Ratio(1, 2, 1), slice(0, 1, None))

    Initialize from other part indicator::

        >>> part_indicator = specificationtools.PartIndicator((1, 2, 1), 0)
        >>> specificationtools.PartIndicator(part_indicator)
        PartIndicator(Ratio(1, 2, 1), 0)

    Part indicators are immutable. 
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        if len(args) == 1:
            assert isinstance(args[0], type(self))
            ratio = args[0].ratio
            indicator = args[0].indicator
        elif len(args) == 2:
            ratio = args[0]
            indicator = args[1]
        else:
            raise Exception('can not initialize part indicator from {!r}'.format(args))
        ratio = mathtools.Ratio(ratio)
        assert isinstance(ratio, mathtools.Ratio)
        assert isinstance(indicator, (int, slice))
        self._ratio = ratio
        self._indicator = indicator

    ### SPECIAL METHODS ###
    
    def __eq__(self, other):
        '''True when `other` is a part indicator with `ratio` and `indicator`
        equal to `self`. Otherwise false.

        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        if self.ratio == other.ratio:
            if self.indicator == other.indicator:
                return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return (
            self.ratio,
            self.indicator,
            )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def indicator(self):
        '''Integer or slice indicating part or parts of ratio to chose::

            >>> part_indicator.indicator
            0

        Return integer or slice.
        '''
        return self._indicator

    @property
    def ratio(self):
        '''Ratio of part indicator::

            >>> part_indicator.ratio
            Ratio(1, 2, 1)

        Return ratio.
        '''
        return self._ratio
