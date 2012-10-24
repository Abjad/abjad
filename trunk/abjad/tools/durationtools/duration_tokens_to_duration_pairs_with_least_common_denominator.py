def duration_tokens_to_duration_pairs_with_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to duration pairs with least common denominator::

        >>> durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
        ... [Fraction(2, 4), 3, '8.', (5, 16)])
        [NonreducedFraction(8, 16), NonreducedFraction(48, 16), NonreducedFraction(3, 16), NonreducedFraction(5, 16)]

    Return new object of `duration_tokens` type.
    '''
    from abjad.tools import durationtools

    rationals = [durationtools.Duration(x) for x in duration_tokens]
    lcd = durationtools.duration_tokens_to_least_common_denominator(duration_tokens)

    duration_pairs = [
        durationtools.rational_to_duration_pair_with_specified_integer_denominator(x, lcd) 
        for x in rationals]

    return type(duration_tokens)(duration_pairs)
