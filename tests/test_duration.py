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


def test_duration_Duration___add__():

    duration_1 = abjad.Duration(1, 2)
    duration_2 = abjad.Duration(3, 2)
    assert duration_1 + duration_2 == abjad.Duration(2, 1)


def test_duration_Offset_constructor():
    """
    Constructor patterns.
    """

    # Initializes from integer numerator:
    assert abjad.Offset(3) == abjad.Offset(3, 1)

    # Initializes from integer-equivalent numeric numerator:

    assert abjad.Offset(3.0) == abjad.Offset(3, 1)

    # Initializes from duration:
    assert abjad.Offset(abjad.Duration(3, 16)) == abjad.Offset(3, 16)

    # Initializes from other offset:
    assert abjad.Offset(abjad.Offset(3, 16)) == abjad.Offset(3, 16)

    # Initializes from other offset with displacement:
    offset_1 = abjad.Offset(3, 16, displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(3, 16, displacement=abjad.Duration(-1, 16))
    assert abjad.Offset(offset_1) == offset_2

    # Intializes from fraction:
    assert abjad.Offset(fractions.Fraction(3, 16)) == abjad.Offset(3, 16)

    # Initializes from solidus string:
    assert abjad.Offset("3/16") == abjad.Offset(3, 16)


def test_duration_Offset_inheritance():
    """
    Offset inheritance.
    """

    assert isinstance(abjad.Offset(3, 16), fractions.Fraction)
    assert isinstance(abjad.Offset(3, 16), numbers.Number)
