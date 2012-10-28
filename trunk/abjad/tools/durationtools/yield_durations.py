from abjad.tools import mathtools


def yield_durations(unique=False):
    r'''.. versionadded:: 2.0

    Example 1. Yield all positive durations in Cantor diagonalized order::

        >>> generator = durationtools.yield_durations()
        >>> for n in range(16):
        ...     generator.next()
        ...
        Duration(1, 1)
        Duration(2, 1)
        Duration(1, 2)
        Duration(1, 3)
        Duration(1, 1)
        Duration(3, 1)
        Duration(4, 1)
        Duration(3, 2)
        Duration(2, 3)
        Duration(1, 4)
        Duration(1, 5)
        Duration(1, 2)
        Duration(1, 1)
        Duration(2, 1)
        Duration(5, 1)
        Duration(6, 1)

    Example 2. Yield all positive durations in Cantor diagonalized order uniquely::

        >>> generator = durationtools.yield_durations(unique=True)
        >>> for n in range(16):
        ...     generator.next()
        ...
        Duration(1, 1)
        Duration(2, 1)
        Duration(1, 2)
        Duration(1, 3)
        Duration(3, 1)
        Duration(4, 1)
        Duration(3, 2)
        Duration(2, 3)
        Duration(1, 4)
        Duration(1, 5)
        Duration(5, 1)
        Duration(6, 1)
        Duration(5, 2)
        Duration(4, 3)
        Duration(3, 4)
        Duration(2, 5)

    Return generator.
    '''
    from abjad.tools import durationtools

    generator = mathtools.yield_nonreduced_fractions()
    while True:
        integer_pair = generator.next()
        duration = durationtools.Duration(integer_pair)
        if not unique:
            yield duration
        elif duration.pair == integer_pair:
            yield duration
