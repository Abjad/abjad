# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class RotationExpression(abctools.AbjadObject):
    r'''Rotation indicator.

    ::

        >>> rotation_indicator = musicexpressiontools.RotationExpression(
        ...     index=-1, level=2, fracture_spanners=False)

    ::

        >>> print format(rotation_indicator)
        musicexpressiontools.RotationExpression(
            index=-1,
            level=2,
            fracture_spanners=False,
            )

    Rotation indicators are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, index=None, level=None, fracture_spanners=None):
        from abjad.tools import durationtools
        assert isinstance(index, (int, durationtools.Duration))
        assert isinstance(level, (int, type(None)))
        assert isinstance(fracture_spanners, (bool, type(None)))
        self._index = index
        self._level = level
        self._fracture_spanners = fracture_spanners

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats rotation indicator.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print format(rotation_indicator)
            musicexpressiontools.RotationExpression(
                index=-1,
                level=2,
                fracture_spanners=False,
                )

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def fracture_spanners(self):
        r'''Fracture spanners when true.
        Otherwise do not fracture spanners.

        ::

            >>> rotation_indicator.fracture_spanners
            False

        Returns boolean or none.
        '''
        return self._fracture_spanners

    @property
    def index(self):
        r'''Rotation indicator index.

        ::

            >>> rotation_indicator.index
            -1

        Returns integer.
        '''
        return self._index

    @property
    def level(self):
        r'''Rotation indicator level.

        ::

            >>> rotation_indicator.level
            2

        Returns integer.
        '''
        return self._level
