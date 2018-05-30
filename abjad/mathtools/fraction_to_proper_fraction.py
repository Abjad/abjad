from abjad import Fraction


def fraction_to_proper_fraction(rational):
    """
    Changes ``rational`` to proper fraction.

    ..  container:: example

        >>> abjad.mathtools.fraction_to_proper_fraction(abjad.Fraction(116, 8))
        (14, Fraction(1, 2))

    Returns pair.
    """
    assert isinstance(rational, Fraction), repr(rational)
    quotient = int(rational)
    residue = rational - quotient
    return quotient, residue
