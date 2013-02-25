from abjad.tools.mathtools.NonreducedRatio import NonreducedRatio


class Ratio(NonreducedRatio):
    '''.. versionadded:: 2.10

    Ratio of one or more nonzero integers.

    Initialize from one or more nonzero integers::

        >>> mathtools.Ratio(2, 4, 2)
        Ratio(1, 2, 1)

    Or initialize from a tuple or list::

        >>> ratio = mathtools.Ratio((2, 4, 2))
        >>> ratio
        Ratio(1, 2, 1)

    Use a tuple to return ratio integers.

        >>> tuple(ratio)
        (1, 2, 1)

    Ratios are immutable.
    '''

    ### INITIALIZER ###

    def __new__(klass, *args):
        from abjad.tools import sequencetools
        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        assert args, repr(args)
        assert all([x != 0 for x in args]), repr(args)
        args = sequencetools.divide_sequence_elements_by_greatest_common_divisor(args)
        self = NonreducedRatio.__new__(klass, args)
        return self
