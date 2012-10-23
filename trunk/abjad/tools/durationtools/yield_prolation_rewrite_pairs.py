def yield_prolation_rewrite_pairs(prolated_duration, minimum_written_duration=None):
    r'''.. versionadded:: 2.0

    Yield all prolation rewrite pairs of `prolated_duration` in Cantor diagonalized order.

    Ensure written duration never less than `minimum_written_duration`.

    The different ways to notate a prolated duration of ``1/8``::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(Duration(1, 8))

    ::

        >>> for pair in pairs: pair
        ...
        (Multiplier(1, 1), Duration(1, 8))
        (Multiplier(2, 3), Duration(3, 16))
        (Multiplier(4, 3), Duration(3, 32))
        (Multiplier(4, 7), Duration(7, 32))
        (Multiplier(8, 7), Duration(7, 64))
        (Multiplier(8, 15), Duration(15, 64))
        (Multiplier(16, 15), Duration(15, 128))
        (Multiplier(16, 31), Duration(31, 128))

    The different ways to notate a prolated duration of ``1/12``::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(Duration(1, 12))

    ::

        >>> for pair in pairs: pair
        ...
        (Multiplier(2, 3), Duration(1, 8))
        (Multiplier(4, 3), Duration(1, 16))
        (Multiplier(8, 9), Duration(3, 32))
        (Multiplier(16, 9), Duration(3, 64))
        (Multiplier(16, 21), Duration(7, 64))
        (Multiplier(32, 21), Duration(7, 128))
        (Multiplier(32, 45), Duration(15, 128))

    The different ways to notate a prolated duration of ``5/48``::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(Duration(5, 48))

    ::

        >>> for pair in pairs: pair
        ...
        (Multiplier(5, 6), Duration(1, 8))
        (Multiplier(5, 3), Duration(1, 16))
        (Multiplier(5, 9), Duration(3, 16))
        (Multiplier(10, 9), Duration(3, 32))
        (Multiplier(20, 21), Duration(7, 64))
        (Multiplier(40, 21), Duration(7, 128))
        (Multiplier(8, 9), Duration(15, 128))

    When `minimum_written_duration` is none set to ``1/128``.

    Return generator.
    '''
    from abjad.tools import durationtools

    if minimum_written_duration is None:
        minimum_written_duration = durationtools.Duration(1, 128)
    else:
        minimum_written_duration = durationtools.Duration(minimum_written_duration)

    generator = durationtools.yield_all_assignable_durations()
    pairs = []

    while True:
        written_duration = generator.next()
        if written_duration < minimum_written_duration:
            pairs = tuple(pairs)
            return pairs
        #prolation = prolated_duration / written_duration
        prolation = durationtools.Multiplier(prolated_duration / written_duration)
        if durationtools.is_proper_tuplet_multiplier(prolation):
            pair = (prolation, written_duration)
            pairs.append(pair)
