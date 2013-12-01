# -*- encoding: utf-8 -*-
from abjad.tools.mathtools.NonreducedRatio import NonreducedRatio


class Ratio(NonreducedRatio):
    '''Ratio of one or more nonzero integers.

    Initializes from one or more nonzero integers:

    ::

        >>> mathtools.Ratio(2, 4, 2)
        Ratio(1, 2, 1)

    Initializes from a tuple or list:

    ::

        >>> ratio = mathtools.Ratio((2, 4, 2))
        >>> ratio
        Ratio(1, 2, 1)

    Uses a tuple to return ratio integers.

        >>> tuple(ratio)
        (1, 2, 1)

    Ratios are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(cls, *args):
        from abjad.tools import sequencetools
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        elif len(args) == 0:
            args = (1, 1)
        assert args, repr(args)
        assert all(x != 0 for x in args), repr(args)
        args = \
            sequencetools.divide_sequence_elements_by_greatest_common_divisor(
            args)
        self = NonreducedRatio.__new__(cls, args)
        return self

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''String representation of ratio.

        Returns string.
        '''
        terms = (str(x) for x in self)
        return ':'.join(terms)
