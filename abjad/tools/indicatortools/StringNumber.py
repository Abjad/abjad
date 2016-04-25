# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class StringNumber(AbjadValueObject):
    r'''String number indicator.

    ..  container:: example

        **Example 1.** String I:

        ::

            >>> indicator = indicatortools.StringNumber(1)
            >>> print(format(indicator))
            indicatortools.StringNumber(
                numbers=(1,),
                )

    ..  container:: example
        
        **Example 2.** Strings II and III:

        ::

            >>> indicator = indicatortools.StringNumber((2, 3))
            >>> print(format(indicator))
            indicatortools.StringNumber(
                numbers=(2, 3),
                )

    '''

    ### CLASS VARIABLES

    __slots__ = (
        '_default_scope',
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        numbers=None,
        ):
        self._default_scope = None
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
    def default_scope(self):
        r'''Gets default scope of string number indicator.

        ..  container:: example

            **Example 1.** String I:

            ::

                >>> indicator = indicatortools.StringNumber(1)
                >>> indicator.default_scope is None
                True

        ..  container:: example
            
            **Example 2.** Strings II and III:

            ::

                >>> indicator = indicatortools.StringNumber((2, 3))
                >>> indicator.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope
        
    @property
    def numbers(self):
        r'''Gets numbers of string number indicator:

        ..  container:: example

            **Example 1.** String I:

            ::

                >>> indicator = indicatortools.StringNumber(1)
                >>> indicator.numbers
                (1,)

        ..  container:: example
            
            **Example 2.** Strings II and III:

            ::

                >>> indicator = indicatortools.StringNumber((2, 3))
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

            **Example 1.** String I:

            ::

                >>> indicator = indicatortools.StringNumber(1)
                >>> indicator.roman_numerals
                ('i',)

        ..  container:: example
            
            **Example 2.** Strings II and III:

            ::

                >>> indicator = indicatortools.StringNumber((2, 3))
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
