import fractions


def rational_to_proper_fraction(rational):
    '''.. versionadded:: 2.0

    Change `rational` to proper fraction::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.rational_to_proper_fraction(Fraction(116, 8))
        (14, Fraction(1, 2))

    Return pair.
    '''

    if not isinstance(rational, fractions.Fraction):
        raise TypeError

    quotient = int(rational)
    residue = rational - quotient

    return quotient, residue
