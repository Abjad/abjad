# -*- encoding: utf-8 -*-
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

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        from abjad.tools import mathtools
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        numbers = [int(_) for _ in numbers]
        gcd = mathtools.greatest_common_divisor(*numbers)
        numbers = [_ // gcd for _ in numbers]
        superclass = super(Ratio, self)
        superclass.__init__(
            numbers=numbers,
            )

    ### SPECIAL METHODS ###

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