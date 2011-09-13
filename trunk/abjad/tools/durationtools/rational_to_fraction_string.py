from fractions import Fraction


def rational_to_fraction_string(rational):
    '''.. versionadded:: 1.1

    Change `rational` to fraction string::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.rational_to_fraction_string(Fraction(2, 4))
        '1/2'

    Return string.
    '''

    if not isinstance(rational, Fraction):
        raise TypeError('must be rational.')

    return '%s/%s' % (rational.numerator, rational.denominator)
