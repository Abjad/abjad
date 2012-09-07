import fractions


def yield_prolation_rewrite_pairs(prolated_duration, minimum_written_duration=None):
    r'''.. versionadded:: 2.0

    Yield all prolation rewrite pairs of `prolated_duration` in Cantor diagonalized order.

    Ensure written duration never less than `minimum_written_duration`.

    The different ways to notate a prolated duration of ``1/8``::

        >>> from abjad.tools import durationtools

    ::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(
        ... Fraction(1, 8))

    ::

        >>> for pair in pairs: pair
        ...
        (Fraction(1, 1), Fraction(1, 8))
        (Fraction(2, 3), Fraction(3, 16))
        (Fraction(4, 3), Fraction(3, 32))
        (Fraction(4, 7), Fraction(7, 32))
        (Fraction(8, 7), Fraction(7, 64))
        (Fraction(8, 15), Fraction(15, 64))
        (Fraction(16, 15), Fraction(15, 128))
        (Fraction(16, 31), Fraction(31, 128))

    The different ways to notate a prolated duration of ``1/12``::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(
        ... Fraction(1, 12))

    ::

        >>> for pair in pairs: pair
        ...
        (Fraction(2, 3), Fraction(1, 8))
        (Fraction(4, 3), Fraction(1, 16))
        (Fraction(8, 9), Fraction(3, 32))
        (Fraction(16, 9), Fraction(3, 64))
        (Fraction(16, 21), Fraction(7, 64))
        (Fraction(32, 21), Fraction(7, 128))
        (Fraction(32, 45), Fraction(15, 128))

    The different ways to notate a prolated duration of ``5/48``::

        >>> pairs = durationtools.yield_prolation_rewrite_pairs(
        ... Fraction(5, 48))

    ::

        >>> for pair in pairs: pair
        ...
        (Fraction(5, 6), Fraction(1, 8))
        (Fraction(5, 3), Fraction(1, 16))
        (Fraction(5, 9), Fraction(3, 16))
        (Fraction(10, 9), Fraction(3, 32))
        (Fraction(20, 21), Fraction(7, 64))
        (Fraction(40, 21), Fraction(7, 128))
        (Fraction(8, 9), Fraction(15, 128))

    When `minimum_written_duration` is none set to ``1/128``.

    Return generator of paired fractions.
    '''
    from abjad.tools import durationtools

    if minimum_written_duration is None:
        minimum_written_duration = fractions.Fraction(1, 128)

    generator = durationtools.yield_all_assignable_rationals()
    pairs = []

    while True:
        written_duration = generator.next()
        if written_duration < minimum_written_duration:
            pairs = tuple(pairs)
            return pairs
        prolation = prolated_duration / written_duration
        if durationtools.is_proper_tuplet_multiplier(prolation):
            pair = (prolation, written_duration)
            pairs.append(pair)
