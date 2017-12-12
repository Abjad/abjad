from .Duration import Duration


class Multiplier(Duration):
    '''Multiplier.

    ..  container:: example

        Initializes from integer numerator:

        >>> abjad.Multiplier(3)
        Multiplier(3, 1)

    ..  container:: example

        Initializes from integer numerator and denominator:

        >>> abjad.Multiplier(3, 16)
        Multiplier(3, 16)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator:

        >>> abjad.Multiplier(3.0)
        Multiplier(3, 1)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator and denominator:

        >>> abjad.Multiplier(3.0, 16)
        Multiplier(3, 16)

    ..  container:: example

        Initializes from integer-equivalent singleton:

        >>> abjad.Multiplier((3,))
        Multiplier(3, 1)

    ..  container:: example

        Initializes from integer-equivalent pair:

        >>> abjad.Multiplier((3, 16))
        Multiplier(3, 16)

    ..  container:: example

        Initializes from other duration:

        >>> abjad.Multiplier(abjad.Duration(3, 16))
        Multiplier(3, 16)

    ..  container:: example

        Intializes from fraction:

        >>> abjad.Multiplier(abjad.Fraction(3, 16))
        Multiplier(3, 16)

    ..  container:: example

        Initializes from solidus string:

        >>> abjad.Multiplier('3/16')
        Multiplier(3, 16)

    ..  container:: example

        Initializes from nonreduced fraction:

        >>> abjad.Multiplier(abjad.NonreducedFraction(6, 32))
        Multiplier(3, 16)

    ..  container:: example

        Multipliers inherit from built-in fraction:

        >>> isinstance(abjad.Multiplier(3, 16), abjad.Fraction)
        True

    ..  container:: example

        Multipliers are numbers:

        >>> import numbers

        >>> isinstance(abjad.Multiplier(3, 16), numbers.Number)
        True

    ..  container:: example

        Attaching a multiplier to a score component multiplies that component's
        duration:

        >>> note = abjad.Note("c'1")
        >>> abjad.f(note)
        c'1

        >>> multiplier = abjad.Multiplier(3, 8)
        >>> abjad.attach(multiplier, note)
        >>> abjad.f(note)
        c'1 * 3/8

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

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

        >>> abjad.Multiplier(3, 2).is_proper_tuplet_multiplier
        True

        Returns true or false.
        '''
        return type(self)(1, 2) < self < type(self)(2)
