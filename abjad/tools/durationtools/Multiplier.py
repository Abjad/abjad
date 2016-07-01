# -*- coding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Multiplier(Duration):
    '''Multiplier.

    ..  container:: example

        **Example 1.** Initializes from integer numerator:

        ::

            >>> Multiplier(3)
            Multiplier(3, 1)

    ..  container:: example

        **Example 2.** Initializes from integer numerator and denominator:

        ::

            >>> Multiplier(3, 16)
            Multiplier(3, 16)

    ..  container:: example

        **Example 3.** Initializes from integer-equivalent numeric numerator:

        ::

            >>> Multiplier(3.0)
            Multiplier(3, 1)

    ..  container:: example

        **Example 4.** Initializes from integer-equivalent numeric numerator
        and denominator:

        ::

            >>> Multiplier(3.0, 16)
            Multiplier(3, 16)

    ..  container:: example

        **Example 5.** Initializes from integer-equivalent singleton:

        ::

            >>> Multiplier((3,))
            Multiplier(3, 1)

    ..  container:: example

        **Example 6.** Initializes from integer-equivalent pair:

        ::

            >>> Multiplier((3, 16))
            Multiplier(3, 16)

    ..  container:: example

        **Example 7.** Initializes from other duration:

        ::

            >>> Multiplier(Duration(3, 16))
            Multiplier(3, 16)

    ..  container:: example

        **Example 8.** Intializes from fraction:

        ::

            >>> Multiplier(Fraction(3, 16))
            Multiplier(3, 16)

    ..  container:: example

        **Example 9.** Initializes from solidus string:

        ::

            >>> Multiplier('3/16')
            Multiplier(3, 16)

    ..  container:: example

        **Example 10.** Initializes from nonreduced fraction:

        ::

            >>> Multiplier(mathtools.NonreducedFraction(6, 32))
            Multiplier(3, 16)

    ..  container:: example

        **Example 11.** Multipliers inherit from built-in fraction:

        ::

            >>> isinstance(Multiplier(3, 16), Fraction)
            True

    ..  container:: example

        **Example 12.** Multipliers are numeric:

        ::

            >>> import numbers

        ::

            >>> isinstance(Multiplier(3, 16), numbers.Number)
            True

    ..  container:: example

        **Example 13.** Attaching a multiplier to a score component multiplies
        that component's duration:

        ::

            >>> note = Note("c'1")
            >>> print(format(note))
            c'1

        ::

            >>> multiplier = Multiplier(3, 8)
            >>> attach(multiplier, note)
            >>> print(format(note))
            c'1 * 3/8

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __mul__(self, *args):
        r'''Multiplier times duration gives duration.

        Returns duration.
        '''
        if len(args) == 1 and type(args[0]) is Duration:
            return Duration(Duration.__mul__(self, *args))
        else:
            return Duration.__mul__(self, *args)

    ### PUBLIC PROPERTIES ###

    @property
    def is_proper_tuplet_multiplier(self):
        '''Is true when mutliplier is greater than ``1/2`` and less than ``2``.
        Otherwise false:

        ::

            >>> Multiplier(3, 2).is_proper_tuplet_multiplier
            True

        Returns true or false.
        '''
        return type(self)(1, 2) < self < type(self)(2)