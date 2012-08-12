def duration_tokens_to_duration_pairs_with_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to duration pairs with least common denominator::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
        ... [Fraction(2, 4), 3, '8.', (5, 16)])
        [(8, 16), (48, 16), (3, 16), (5, 16)]

    Return new object of `duration_tokens` type.
    '''
    from abjad.tools import durationtools

    rationals = durationtools.duration_tokens_to_rationals(duration_tokens)
    lcd = durationtools.duration_tokens_to_least_common_denominator(duration_tokens)

    duration_pairs = [
        durationtools.rational_to_duration_pair_with_specified_integer_denominator(x, lcd) 
        for x in rationals]

    return type(duration_tokens)(duration_pairs)
