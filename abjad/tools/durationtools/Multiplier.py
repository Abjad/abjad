# -*- coding: utf-8 -*-
from abjad.tools.durationtools.Duration import Duration


class Multiplier(Duration):
    '''Multiplier.

    ..  container:: example

        Initializes from integer numerator:

        ::

            >>> Multiplier(3)
            Multiplier(3, 1)

    ..  container:: example

        Initializes from integer numerator and denominator:

        ::

            >>> Multiplier(3, 16)
            Multiplier(3, 16)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator:

        ::

            >>> Multiplier(3.0)
            Multiplier(3, 1)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator and denominator:

        ::

            >>> Multiplier(3.0, 16)
            Multiplier(3, 16)

    ..  container:: example

        Initializes from integer-equivalent singleton:

        ::

            >>> Multiplier((3,))
            Multiplier(3, 1)

    ..  container:: example

        Initializes from integer-equivalent pair:

        ::

            >>> Multiplier((3, 16))
            Multiplier(3, 16)

    ..  container:: example

        Initializes from other duration:

        ::

            >>> Multiplier(Duration(3, 16))
            Multiplier(3, 16)

    ..  container:: example

        Intializes from fraction:

        ::

            >>> Multiplier(Fraction(3, 16))
            Multiplier(3, 16)

    ..  container:: example

        Initializes from solidus string:

        ::

            >>> Multiplier('3/16')
            Multiplier(3, 16)

    ..  container:: example

        Initializes from nonreduced fraction:

        ::

            >>> Multiplier(mathtools.NonreducedFraction(6, 32))
            Multiplier(3, 16)

    ..  container:: example

        Multipliers inherit from built-in fraction:

        ::

            >>> isinstance(Multiplier(3, 16), Fraction)
            True

    ..  container:: example

        Multipliers are numeric:

        ::

            >>> import numbers

        ::

            >>> isinstance(Multiplier(3, 16), numbers.Number)
            True

    ..  container:: example

        Attaching a multiplier to a score component multiplies that component's
        duration:

        ::

            >>> note = Note("c'1")
            >>> f(note)
            c'1

        ::

            >>> multiplier = Multiplier(3, 8)
            >>> attach(multiplier, note)
            >>> f(note)
            c'1 * 3/8

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __mul__(self, *arguments):
        r'''Multiplier times duration gives duration.

        Returns duration.
        '''
        if len(arguments) == 1 and type(arguments[0]) is Duration:
            return Duration(Duration.__mul__(self, *arguments))
        else:
            return Duration.__mul__(self, *arguments)

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
