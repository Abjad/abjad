from abjad.tools import abctools


class RotationIndicator(abctools.AbjadObject):
    r'''Rotation indicator.

    ::

        >>> rotation_indicator = musicexpressiontools.RotationIndicator(
        ...     index=-1, level=2, fracture_spanners=False)

    ::

        >>> z(rotation_indicator)
        musicexpressiontools.RotationIndicator(
            index=-1,
            level=2,
            fracture_spanners=False
            )

    Rotation indicators are immutable.
    '''

    def __init__(self, index=None, level=None, fracture_spanners=None):
        from abjad.tools import durationtools
        assert isinstance(index, (int, durationtools.Duration))
        assert isinstance(level, (int, type(None)))
        assert isinstance(fracture_spanners, (bool, type(None)))
        self._index = index
        self._level = level
        self._fracture_spanners = fracture_spanners

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fracture_spanners(self):
        '''Fracture spanners when true.
        Otherwise do not fracture spanners.

        ::

            >>> rotation_indicator.fracture_spanners
            False

        Return boolean or none.
        '''
        return self._fracture_spanners

    @property
    def index(self):
        '''Rotation indicator index.

        ::

            >>> rotation_indicator.index
            -1

        Return integer.
        '''
        return self._index

    @property
    def level(self):
        '''Rotation indicator level.

        ::

            >>> rotation_indicator.level
            2

        Return integer.
        '''
        return self._level
