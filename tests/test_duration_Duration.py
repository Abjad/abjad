import fractions
import numbers

import abjad


def test_duration_Duration_01():
    """
    Initializer patterns.
    """

    # Initializes from integer numerator
    assert abjad.Duration(3) == abjad.Duration(3, 1)

    # Initializes from integer numerator and denominator
    assert abjad.Duration(3, 16) == abjad.Duration(3, 16)

    # Initializes from integer-equivalent numeric numerator
    assert abjad.Duration(3.0) == abjad.Duration(3, 1)

    # Initializes from other duration
    assert abjad.Duration(abjad.Duration(3, 16)) == abjad.Duration(3, 16)

    # Intializes from fraction
    assert abjad.Duration(fractions.Fraction(3, 16)) == abjad.Duration(3, 16)

    # Initializes from solidus string
    assert abjad.Duration("3/16") == abjad.Duration(3, 16)


def test_duration_Duration_02():
    """
    Durations inherit from built-in fraction.
    """

    assert isinstance(abjad.Duration(3, 16), fractions.Fraction)


def test_durtion_Duration_03():
    """
    Durations are numbers.
    """

    assert isinstance(abjad.Duration(3, 16), numbers.Number)
