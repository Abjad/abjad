def yield_all_assignable_durations():
    '''.. versionadded:: 2.0

    Yield all assignable rationals in Cantor diagonalized order::

        >>> generator = durationtools.yield_all_assignable_durations()
        >>> for n in range(16):
        ...     generator.next()
        ...
        Duration(1, 1)
        Duration(2, 1)
        Duration(1, 2)
        Duration(3, 1)
        Duration(4, 1)
        Duration(3, 2)
        Duration(1, 4)
        Duration(6, 1)
        Duration(3, 4)
        Duration(7, 1)
        Duration(8, 1)
        Duration(7, 2)
        Duration(1, 8)
        Duration(7, 4)
        Duration(3, 8)
        Duration(12, 1)

    Return fraction generator.
    '''
    from abjad.tools import durationtools

    generator = durationtools.yield_all_positive_rationals_uniquely()
    while True:
        duration = generator.next()
        duration = durationtools.Duration(duration)
        if duration.is_assignable:
            yield duration
