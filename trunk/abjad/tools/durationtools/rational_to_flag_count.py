import math


def rational_to_flag_count(rational):
    '''.. versionadded:: 2.0

    Change `rational` to number of flags required to notate::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.rational_to_flag_count(Fraction(1, 32))
        3

    Return nonnegative integer.
    '''

    flag_count = max(-int(math.floor(math.log(float(rational.numerator) /
        rational.denominator, 2))) - 2, 0)

    return flag_count
