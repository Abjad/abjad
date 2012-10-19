from abjad.tools import mathtools


def duration_token_to_assignable_rationals(duration_token):
    '''Change `duration_token` to big-endian tuple of assignable Durations:

    ::

        >>> duration_tokens = [(n, 16) for n in range(10, 20)]
        >>> for duration_token in duration_tokens:
        ...     pairs = durationtools.duration_token_to_assignable_rationals(
        ...         duration_token)
        ...     print duration_token, pairs
        (10, 16) (Duration(1, 2), Duration(1, 8))
        (11, 16) (Duration(1, 2), Duration(3, 16))
        (12, 16) (Duration(3, 4),)
        (13, 16) (Duration(3, 4), Duration(1, 16))
        (14, 16) (Duration(7, 8),)
        (15, 16) (Duration(15, 16),)
        (16, 16) (Duration(1, 1),)
        (17, 16) (Duration(1, 1), Duration(1, 16))
        (18, 16) (Duration(1, 1), Duration(1, 8))
        (19, 16) (Duration(1, 1), Duration(3, 16))

    Also handles very large durations:

    ::

        >>> for x in durationtools.duration_token_to_assignable_rationals(250):
        ...     x
        ...
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(8, 1)
        Duration(2, 1)

    Return tuple of integer pairs.
    '''

    from abjad.tools import durationtools

    rational = durationtools.Duration(duration_token)

    if 0 == rational:
        return (durationtools.Duration(0),)

    def recurse(rational):
        result = []
        if durationtools.is_assignable_rational(rational):
            result.append(rational)
        elif 8 < rational:
            result.append(durationtools.Duration(8))
            result.extend(recurse(rational - 8))
        else:
            numerator, denominator = rational.numerator, rational.denominator
            result.extend([durationtools.Duration(n, denominator)
                for n in mathtools.partition_integer_into_canonic_parts(numerator)])
        return result    

    result = recurse(rational)

    if 1 < len(result):
        result.sort(reverse=True)

    return tuple(result)
