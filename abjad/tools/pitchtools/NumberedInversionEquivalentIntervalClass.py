# -*- coding: utf-8 -*-
import numbers
from abjad.tools import mathtools
from abjad.tools.pitchtools.NumberedIntervalClass import NumberedIntervalClass


class NumberedInversionEquivalentIntervalClass(NumberedIntervalClass):
    '''Numbered inversion-equivalent interval-class.

    ::

        >>> import abjad

    ..  container:: example

        Initializes from integer:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(0)
            NumberedInversionEquivalentIntervalClass(0)

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(1)
            NumberedInversionEquivalentIntervalClass(1)

    ..  container:: example

        Initializes from float:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass(1.5)
            NumberedInversionEquivalentIntervalClass(1.5)

    ..  container:: example

        Initializes from string:

        ::

            >>> abjad.NumberedInversionEquivalentIntervalClass('1')
            NumberedInversionEquivalentIntervalClass(1)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_number',
        )

    ### INITIALIZER ###

    # TODO: clean up
    def __init__(self, number=0):
        from abjad.tools import pitchtools
        if isinstance(number, type(self)):
            number = number.number
        elif isinstance(number, numbers.Number):
            if not 0 <= number <= 6:
                message = 'must be between 0 and 6, inclusive.'
                raise ValueError(message)
        elif getattr(number, 'semitones', None) is not None:
            number = number.semitones
            number %= 12
            if 6 < number:
                number = 12 - number
        elif isinstance(number, str):
            number = float(number)
            if mathtools.is_integer_equivalent(number):
                number = int(number)
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, number)
            raise TypeError(message)
        self._number = number

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Gets absolute value of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            ::

                >>> abs(abjad.NumberedInversionEquivalentIntervalClass(0))
                NumberedInversionEquivalentIntervalClass(0)

            ::

                >>> abs(abjad.NumberedInversionEquivalentIntervalClass(1.5))
                NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        '''
        return type(self)(abs(self.number))

    def __lt__(self, argument):
        r'''Is true when `argument` is a numbered inversion-equivalent
        interval-class with a number less than this numbered
        inversion-equivalent interval-class.
        '''
        if isinstance(argument, type(self)):
            return self.number < argument.number
        return False

    def __neg__(self):
        r'''Negates numbered inversion-equivalent interval-class.

        ..  container:: example

            ::

                >>> -abjad.NumberedInversionEquivalentIntervalClass(0)
                NumberedInversionEquivalentIntervalClass(0)

            ::

                >>> -abjad.NumberedInversionEquivalentIntervalClass(1.5)
                NumberedInversionEquivalentIntervalClass(1.5)

        Returns new numbered inversion-equivalent interval-class.
        '''
        return type(self)(self.number)

    def __str__(self):
        r'''Gets string representation of numbered inversion-equivalent
        interval-class.

        ..  container:: example

            ::

                >>> str(abjad.NumberedInversionEquivalentIntervalClass(0))
                '0'

            ::

                >>> str(abjad.NumberedInversionEquivalentIntervalClass(1.5))
                '1.5'

        Returns string.
        '''
        return str(self.number)
