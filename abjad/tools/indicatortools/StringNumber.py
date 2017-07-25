# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class StringNumber(AbjadValueObject):
    r'''String number.

    ::

        >>> import abjad

    ..  container:: example

        String I:

        ::

            >>> indicator = abjad.StringNumber(1)
            >>> f(indicator)
            abjad.StringNumber(
                numbers=(1,),
                )

    ..  container:: example
        
        Strings II and III:

        ::

            >>> indicator = abjad.StringNumber((2, 3))
            >>> f(indicator)
            abjad.StringNumber(
                numbers=(2, 3),
                )

    '''

    ### CLASS VARIABLES

    __slots__ = (
        '_numbers',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        numbers=None,
        ):
        numbers = numbers or ()
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        elif not isinstance(numbers, collections.Sequence):
            numbers = (numbers,)
        numbers = tuple(int(x) for x in numbers)
        assert all(0 < x < 7 for x in numbers)
        self._numbers = tuple(numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        r'''Gets numbers of string number indicator:

        ..  container:: example

            String I:

            ::

                >>> indicator = abjad.StringNumber(1)
                >>> indicator.numbers
                (1,)

        ..  container:: example
            
            Strings II and III:

            ::

                >>> indicator = abjad.StringNumber((2, 3))
                >>> indicator.numbers
                (2, 3)

        Set to tuple of zero or more positive integers.

        Defaults to empty tuple.

        Returns tuple of zero or more positive integers.
        '''
        return self._numbers

    @property
    def roman_numerals(self):
        r'''Gets roman numerals of string number indicator.

        ..  container:: example

            String I:

            ::

                >>> indicator = abjad.StringNumber(1)
                >>> indicator.roman_numerals
                ('i',)

        ..  container:: example
            
            Strings II and III:

            ::

                >>> indicator = abjad.StringNumber((2, 3))
                >>> indicator.roman_numerals
                ('ii', 'iii')

        Returns tuple of zero or more strings.
        '''
        numerals = ('i', 'ii', 'iii', 'iv', 'v', 'vi')
        result = []
        for x in self.numbers:
            numeral = numerals[x - 1]
            result.append(numeral)
        return tuple(result)
