from fractions import Fraction


def multiply_duration_pair_and_try_to_preserve_numerator(pair, multiplier):
    '''.. versionadded:: 1.1

    Multiply duration `pair` by rational `multiplier` and try to preserve numerator::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.multiply_duration_pair_and_try_to_preserve_numerator((9, 16), Fraction(2, 3))
        (9, 24)

    Intended for certain types of meter multiplication.

    Return integer pair.

    .. versionchanged:: 2.0
        renamed ``durationtools.pair_multiply_constant_numerator()`` to
        ``durationtools.multiply_duration_pair_and_try_to_preserve_numerator()``.
    '''

    assert isinstance(pair, tuple)
    assert isinstance(multiplier, Fraction)

    pair_denominator = pair[1]
    candidate_result_denominator = pair_denominator / multiplier

    if candidate_result_denominator.denominator == 1:
        return pair[0], candidate_result_denominator.numerator
    else:
        result_numerator = pair[0] * candidate_result_denominator.denominator
        result_denominator = candidate_result_denominator.numerator
        return result_numerator, result_denominator
