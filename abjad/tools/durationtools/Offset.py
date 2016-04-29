# -*- coding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Offset(Duration):
    '''A musical offset.

    ..  container:: example

        **Example 1.** Initializes from integer numerator:

        ::

            >>> Offset(3)
            Offset(3, 1)

    ..  container:: example

        **Example 2.** Initializes from integer numerator and denominator:

        ::

            >>> Offset(3, 16)
            Offset(3, 16)

    ..  container:: example

        **Example 3.** Initializes from integer-equivalent numeric numerator:

        ::

            >>> Offset(3.0)
            Offset(3, 1)

    ..  container:: example

        **Example 4.** Initializes from integer-equivalent numeric numerator
        and denominator:

        ::

            >>> Offset(3.0, 16)
            Offset(3, 16)

    ..  container:: example

        **Example 5.** Initializes from integer-equivalent singleton:

        ::

            >>> Offset((3,))
            Offset(3, 1)

    ..  container:: example

        **Example 6.** Initializes from integer-equivalent pair:

        ::

            >>> Offset((3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 7.** Initializes from other duration:

        ::

            >>> Offset(Duration(3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 8.** Intializes from fraction:

        ::

            >>> Offset(Fraction(3, 16))
            Offset(3, 16)

    ..  container:: example

        **Example 9.** Initializes from solidus string:

        ::

            >>> Offset('3/16')
            Offset(3, 16)

    ..  container:: example

        **Example 10.** Initializes from nonreduced fraction:

        ::

            >>> Offset(mathtools.NonreducedFraction(6, 32))
            Offset(3, 16)

    ..  container:: example

        **Example 11.** Durations inherit from built-in fraction:

        ::

            >>> isinstance(Offset(3, 16), Fraction)
            True

    ..  container:: example

        **Example 12.** Durations are numeric:

        ::

            >>> import numbers

        ::

            >>> isinstance(Offset(3, 16), numbers.Number)
            True

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
