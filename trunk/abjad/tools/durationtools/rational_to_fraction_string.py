import fractions


def rational_to_fraction_string(rational):
    '''.. versionadded:: 1.1

    Change `rational` to fraction string::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.rational_to_fraction_string(Fraction(2, 4))
        '1/2'

    Return string.
    '''

    if not isinstance(rational, fractions.Fraction):
        raise TypeError('must be rational.')

    return '%s/%s' % (rational.numerator, rational.denominator)
