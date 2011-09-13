def rational_to_prolation_string(rational):
    r'''.. versionadded:: 2.0

    Change `rational` to prolation string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> generator = durationtools.yield_all_positive_rationals_in_cantor_diagonalized_order_uniquely()
        abjad> for n in range(16): # doctest: +SKIP
        ...     rational = generator.next()
        ...     prolation_string = durationtools.rational_to_prolation_string(rational)
        ...     print '%s\\t%s' % (rational, prolation_string)
        ...
        1         1:1
        2         1:2
        1/2     2:1
        1/3     3:1
        3         1:3
        4         1:4
        3/2     2:3
        2/3     3:2
        1/4     4:1
        1/5     5:1
        5         1:5
        6         1:6
        5/2     2:5
        4/3     3:4
        3/4     4:3
        2/5     5:2

    Return string.
    '''

    return '%s:%s' % (rational.denominator, rational.numerator)
