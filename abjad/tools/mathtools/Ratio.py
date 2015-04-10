# -*- encoding: utf-8 -*-
import collections
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

            >>> ratio = mathtools.Ratio((2, 4, 2))
            >>> tuple(ratio)
            (1, 2, 1)

    Ratios are immutable.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, items=(1, 1), item_class=None):
        from abjad.tools import mathtools
        if not isinstance(items, (list, tuple, mathtools.NonreducedRatio)):
            message = 'ratio must initialize with list or tuple.'
            raise Exception(message)
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