# -*- encoding: utf-8 -*-
from abjad.tools import abctools


class RotationExpression(abctools.AbjadObject):
    r'''Rotation expression.

    ::

        >>> rotation_expression = musicexpressiontools.RotationExpression(
        ...     index=-1, level=2, fracture_spanners=False)

    ::

        >>> print format(rotation_expression)
        musicexpressiontools.RotationExpression(
            index=-1,
            level=2,
            fracture_spanners=False,
            )

    Rotation expressions are immutable.
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
        r'''Formats rotation expression.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> print format(rotation_expression)
            musicexpressiontools.RotationExpression(
                index=-1,
                level=2,
                fracture_spanners=False,
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def fracture_spanners(self):
        r'''Fracture spanners when true.
        Otherwise do not fracture spanners.

        ::

            >>> rotation_expression.fracture_spanners
            False

        Returns boolean or none.
        '''
        return self._fracture_spanners

    @property
    def index(self):
        r'''Rotation expression index.

        ::

            >>> rotation_expression.index
            -1

        Returns integer.
        '''
        return self._index

    @property
    def level(self):
        r'''Rotation expression level.

        ::

            >>> rotation_expression.level
            2

        Returns integer.
        '''
        return self._level
