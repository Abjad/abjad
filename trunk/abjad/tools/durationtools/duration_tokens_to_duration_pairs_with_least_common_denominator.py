from abjad.tools.durationtools.duration_tokens_to_least_common_denominator import duration_tokens_to_least_common_denominator
from abjad.tools.durationtools.duration_tokens_to_rationals import duration_tokens_to_rationals
from abjad.tools.durationtools.rational_to_duration_pair_with_specified_integer_denominator import rational_to_duration_pair_with_specified_integer_denominator


def duration_tokens_to_duration_pairs_with_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to duration pairs with least common denominator::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator([Fraction(2, 4), 3, '8.', (5, 16)])
        [(8, 16), (48, 16), (3, 16), (5, 16)]

    Return new object of `duration_tokens` type.
    '''

    rationals = duration_tokens_to_rationals(duration_tokens)
    lcd = duration_tokens_to_least_common_denominator(duration_tokens)

    duration_pairs = [
        rational_to_duration_pair_with_specified_integer_denominator(x, lcd) for x in rationals]

    return type(duration_tokens)(duration_pairs)
