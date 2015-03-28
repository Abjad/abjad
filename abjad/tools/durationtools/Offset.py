# -*- encoding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Offset(Duration):
    '''A musical offset.

    ::

        >>> durationtools.Offset(121, 16)
        Offset(121, 16)

    Offset inherits from duration (which inherits from built-in ``Fraction``).
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __sub__(self, expr):
        '''Offset taken from offset returns duration:

        ::

            >>> durationtools.Offset(2) - durationtools.Offset(1, 2)
            Duration(3, 2)

        Duration taken from offset returns another offset:

        ::

            >>> durationtools.Offset(2) - durationtools.Duration(1, 2)
            Offset(3, 2)

        Coerce `expr` to offset when `expr` is neither offset nor duration:

        ::

            >>> durationtools.Offset(2) - Fraction(1, 2)
            Duration(3, 2)

        Returns duration or offset.
        '''
        if isinstance(expr, type(self)):
            return Duration(Duration.__sub__(self, expr))
        elif isinstance(expr, Duration):
            return Duration.__sub__(self, expr)
        else:
            expr = type(self)(expr)
            return self - expr