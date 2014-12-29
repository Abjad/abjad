# -*- encoding: utf-8 -*-
import collections
from abjad.tools.abctools import AbjadValueObject


class StringNumber(AbjadValueObject):
    r'''String number indicator.

    ::

        >>> indicator = indicatortools.StringNumber(1)
        >>> print(format(indicator))
        indicatortools.StringNumber(
            numbers=(1,),
            )

    ::

        >>> indicator = indicatortools.StringNumber((2, 3))
        >>> print(format(indicator))
        indicatortools.StringNumber(
            numbers=(2, 3),
            )

    '''

    ### CLASS VARIABLES

    __slots__ = (
        '_numbers',
        )

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
        r'''Gets string numbers.

        ::

            >>> indicator = indicatortools.StringNumber((2, 3))
            >>> indicator.numbers
            (2, 3)

        '''
        return self._numbers

    @property
    def roman_numerals(self):
        r'''Gets string numbers as roman numerals.

            >>> indicator = indicatortools.StringNumber((3, 4))
            >>> indicator.roman_numerals
            ('iii', 'iv')

        '''
        numerals = ('i', 'ii', 'iii', 'iv', 'v', 'vi')
        result = []
        for x in self.numbers:
            numeral = numerals[x - 1]
            result.append(numeral)
        return tuple(result)