# -*- coding: utf-8 -*-
from abjad.tools.mathtools.NonreducedRatio import NonreducedRatio


class Ratio(NonreducedRatio):
    '''Ratio.

    ..  container:: example

        **Example 1.** Ratio of two numbers:

        ::

            >>> mathtools.Ratio((2, 4))
            Ratio((1, 2))

    ..  container:: example

        **Example 2.** Ratio of three numbers:

        ::

            >>> mathtools.Ratio((2, 4, 2))
            Ratio((1, 2, 1))

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        from abjad.tools import mathtools
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        numbers = [int(_) for _ in numbers]
        gcd = mathtools.greatest_common_divisor(*numbers)
        numbers = [_ // gcd for _ in numbers]
        self._numbers = tuple(numbers)

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        r'''Gets item at `i`.

        ..  container:: example

            ::

                >>> ratio = mathtools.Ratio((2, 4, 2))
                >>> ratio[1]
                2

        Returns integer or tuple.
        '''
        if isinstance(i, slice):
            return tuple(self._numbers[i])
        return self._numbers[i]

    def __len__(self):
        r'''Gets length of ratio.

        ..  container:: example

            ::

                >>> ratio = mathtools.Ratio((2, 4, 2))
                >>> len(ratio)
                3

        Returns integer.
        '''
        return len(self._numbers)

    def __str__(self):
        r'''Gets string representation of ratio.

        ..  container:: example

            **Example 1.** Ratio of two numbers:

            ::

                >>> str(mathtools.Ratio((2, 4)))
                '1:2'

        ..  container:: example

            **Example 2.** Ratio of three numbers:

            ::

                >>> str(mathtools.Ratio((2, 4, 2)))
                '1:2:1'

        Returns string.
        '''
        numbers = (str(x) for x in self.numbers)
        return ':'.join(numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        r'''Gets multipliers of ratio.

        ..  container:: example

            **Example 1.** Ratio of two numbers:

            ::

                >>> ratio = mathtools.Ratio((2, 4))
                >>> ratio.multipliers
                (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            **Example 2.** Ratio of three numbers:

            ::

                >>> ratio = mathtools.Ratio((2, 4, 2))
                >>> ratio.multipliers
                (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        '''
        from abjad.tools import durationtools
        weight = sum(self.numbers)
        multipliers = [
            durationtools.Multiplier((_, weight))
            for _ in self.numbers
            ]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        r'''Gets numbers of ratio.

        ..  container:: example

            **Example 1.** Ratio of two numbers:

            ::

                >>> ratio = mathtools.Ratio((2, 4))
                >>> ratio.numbers
                (1, 2)

        ..  container:: example

            **Example 2.** Ratio of three numbers:

            ::

                >>> ratio = mathtools.Ratio((2, 4, 2))
                >>> ratio.numbers
                (1, 2, 1)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        '''
        return self._numbers
