import copy
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


def test_duration_ValueOffset___copy__():

    offset_1 = abjad.Offset(
        abjad.Fraction(1, 4),
        displacement=abjad.Duration(-1, 16),
    )
    offset_2 = copy.copy(offset_1)

    assert offset_1 == offset_2
    assert offset_1 is not offset_2


def test_duration_ValueOffset___deepcopy__():

    offset_1 = abjad.Offset(
        abjad.Fraction(1, 4),
        displacement=abjad.Duration(-1, 16),
    )
    offset_2 = copy.deepcopy(offset_1)

    assert offset_1 == offset_2
    assert offset_1 is not offset_2


def test_duration_ValueOffset___eq__():

    # With equal numerators, denominators and displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 == offset_1
    assert offset_1 == offset_2
    assert offset_2 == offset_1
    assert offset_2 == offset_2

    # With equal numerators and denominators but differing grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 == offset_1
    assert not offset_1 == offset_2
    assert not offset_2 == offset_1
    assert offset_2 == offset_2

    # With differing numerators and denominators. Ignores grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2), displacement=abjad.Duration(-99))

    assert offset_1 == offset_1
    assert not offset_1 == offset_2
    assert not offset_2 == offset_1
    assert offset_2 == offset_2


def test_duration_ValueOffset___ge__():

    # With equal numerators, denominators and displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 >= offset_1
    assert offset_1 >= offset_2
    assert offset_2 >= offset_1
    assert offset_2 >= offset_2

    # With equal numerators and denominators but differing grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 >= offset_1
    assert not offset_1 >= offset_2
    assert offset_2 >= offset_1
    assert offset_2 >= offset_2

    # With differing numerators and denominators. Ignores grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2), displacement=abjad.Duration(-99))

    assert offset_1 >= offset_1
    assert not offset_1 >= offset_2
    assert offset_2 >= offset_1
    assert offset_2 >= offset_2


def test_duration_ValueOffset___gt__():

    # With equal numerators, denominators and displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert not offset_1 > offset_1
    assert not offset_1 > offset_2
    assert not offset_2 > offset_1
    assert not offset_2 > offset_2

    # With equal numerators and denominators but differing grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert not offset_1 > offset_1
    assert not offset_1 > offset_2
    assert offset_2 > offset_1
    assert not offset_2 > offset_2

    # With differing numerators and denominators. Ignores grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2), displacement=abjad.Duration(-99))

    assert not offset_1 > offset_1
    assert not offset_1 > offset_2
    assert offset_2 > offset_1
    assert not offset_2 > offset_2


def test_duration_ValueOffset___le__():

    # With equal numerators, denominators and displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 <= offset_1
    assert offset_1 <= offset_2
    assert offset_2 <= offset_1
    assert offset_2 <= offset_2

    # With equal numerators and denominators but differing grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert offset_1 <= offset_1
    assert offset_1 <= offset_2
    assert not offset_2 <= offset_1
    assert offset_2 <= offset_2

    # With differing numerators and denominators. Ignores grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2), displacement=abjad.Duration(-99))

    assert offset_1 <= offset_1
    assert offset_1 <= offset_2
    assert not offset_2 <= offset_1
    assert offset_2 <= offset_2


def test_duration_ValueOffset___lt__():

    # With equal numerators, denominators and displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert not offset_1 < offset_1
    assert not offset_1 < offset_2
    assert not offset_2 < offset_1
    assert not offset_2 < offset_2

    # With equal numerators and denominators but differing nonzero grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 16))

    assert not offset_1 < offset_1
    assert offset_1 < offset_2
    assert not offset_2 < offset_1
    assert not offset_2 < offset_2

    # With equal numerators and denominators but differing zero-valued displacement:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4), displacement=abjad.Duration(-1, 8))
    offset_2 = abjad.Offset(abjad.Fraction(1, 4))

    assert not offset_1 < offset_1
    assert offset_1 < offset_2
    assert not offset_2 < offset_1
    assert not offset_2 < offset_2

    # With differing numerators and denominators. Ignores grace displacements:
    offset_1 = abjad.Offset(abjad.Fraction(1, 4))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2), displacement=abjad.Duration(-99))

    assert not offset_1 < offset_1
    assert offset_1 < offset_2
    assert not offset_2 < offset_1
    assert not offset_2 < offset_2


def test_duration_ValueOffset___sub__():

    # Offset taken from offset returns duration:
    offset_1 = abjad.Offset(abjad.Fraction(2))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2))
    assert offset_1 - offset_2 == abjad.Duration(3, 2)

    # Duration taken from offset returns another offset:
    offset = abjad.Offset(abjad.Fraction(2))
    duration = abjad.Duration(1, 2)
    assert offset - duration == abjad.Offset(abjad.Fraction(3, 2))
