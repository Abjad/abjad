# -*- encoding: utf-8 -*-
from abjad.tools.mathtools.NonreducedRatio import NonreducedRatio


class Ratio(NonreducedRatio):
    '''Ratio of one or more nonzero integers.

    ..  container:: example

        **Example 1a.** Initializes iterable of nonzero integers:

        ::

            >>> mathtools.Ratio((2, 4, 2))
            Ratio((1, 2, 1))

    ..  container:: example

        **Example 2.** Use a tuple to return ratio integers.

        ::

            >>> ratio = mathtools.Ratio((2, 4, 2))
            >>> tuple(ratio)
            (1, 2, 1)

    ..  container:: example

        **Example 3.** Instantiate a ratio from another ratio.

        ::

            >>> ratio = mathtools.Ratio((1, 2, 3))
            >>> mathtools.Ratio(ratio)
            Ratio((1, 2, 3))

    Ratios are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=(1, 1), item_class=None):
        from abjad.tools import mathtools
        items = [int(_) for _ in items]
        gcd = mathtools.greatest_common_divisor(*items)
        items = [_ // gcd for _ in items]
        superclass = super(Ratio, self)
        superclass.__init__(
            items=items,
            )

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of ratio.

        ..  container:: example

            **Example 1.** String representation:

            ::

                >>> str(mathtools.Ratio((3, 4)))
                '3:4'

        Returns string.
        '''
        terms = (str(x) for x in self)
        return ':'.join(terms)

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        r'''Gets multipliers implicit in ratio.

        ..  container:: example

            **Example 1.** Gets mutlipliers:

            ::

                >>> mathtools.Ratio((1, 2, 1)).multipliers
                (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        '''
        from abjad.tools import durationtools
        weight = sum(self) 
        multipliers = [durationtools.Multiplier((_, weight)) for _ in self]
        multipliers = tuple(multipliers)
        return multipliers