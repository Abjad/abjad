# -*- coding: utf-8 -*-
import fractions


def fraction_to_proper_fraction(rational):
    '''Changes `rational` to proper fraction.

    ::

        >>> mathtools.fraction_to_proper_fraction(Fraction(116, 8))
        (14, Fraction(1, 2))

    Returns pair.
    '''

    if not isinstance(rational, fractions.Fraction):
        raise TypeError

    quotient = int(rational)
    residue = rational - quotient

    return quotient, residue
