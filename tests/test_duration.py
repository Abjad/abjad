import copy

import abjad


def test_duration_Duration___abs__():

    assert abs(abjad.Duration(-1, 4)) == abjad.Duration(1, 4)


def test_duration_Duration___add__():

    duration = abjad.Duration(1, 4) + abjad.Duration(2, 4)
    assert duration == abjad.Duration(3, 4)

    durations = abjad.duration.value_durations([(1, 8), (2, 8), (3, 8)])
    assert sum(durations) == abjad.Duration(3, 4)


def test_duration_Duration___eq__():

    assert abjad.Duration(1, 4) == abjad.Duration(1, 4)
    assert abjad.Duration(1, 4) == abjad.Duration(2, 8)
    assert not abjad.Duration(1, 4) == abjad.Fraction(1, 4)


def test_duration_Duration___ge__():

    assert abjad.Duration(1, 4) >= abjad.Duration(1, 4)


def test_duration_Duration___gt__():

    assert abjad.Duration(2, 4) > abjad.Duration(1, 4)


def test_duration_Duration___le__():

    assert abjad.Duration(1, 4) <= abjad.Duration(1, 4)


def test_duration_Duration___lt__():

    assert abjad.Duration(1, 4) < abjad.Duration(2, 4)


def test_duration_Duration___ne__():

    assert abjad.Duration(1, 4) != abjad.Duration(2, 4)
    assert abjad.Duration(1, 4) != abjad.Fraction(1, 4)


def test_duration_Duration___neg__():

    assert -abjad.Duration(1, 4) == abjad.Duration(-1, 4)
    assert -abjad.Duration(-1, 4) == abjad.Duration(1, 4)


def test_duration_Duration___rmul__():

    assert 3 * abjad.Duration(1, 4) == abjad.Duration(3, 4)


def test_duration_Duration___sub__():

    result = abjad.Duration(5, 4) - abjad.Duration(4, 4)
    assert result == abjad.Duration(1, 4)

    result = abjad.Duration(4, 4) - abjad.Duration(5, 4)
    assert result == abjad.Duration(-1, 4)


def test_duration_Duration___truediv__():

    result = abjad.Duration(3, 4) / abjad.Duration(1, 4)
    assert result == abjad.Fraction(3, 1)

    result = abjad.Duration(3, 4) / abjad.Fraction(1, 4)
    assert result == abjad.Duration(3, 1)

    result = abjad.Duration(3, 4) / abjad.Duration(3, 1)
    assert result == abjad.Fraction(1, 4)

    result = abjad.Duration(3, 4) / abjad.Fraction(3, 1)
    assert result == abjad.Duration(1, 4)


def test_duration_Offset___copy__():

    offset_1 = abjad.Offset(
        abjad.Fraction(1, 4),
        displacement=abjad.Duration(-1, 16),
    )
    offset_2 = copy.copy(offset_1)

    assert offset_1 == offset_2
    assert offset_1 is not offset_2


def test_duration_Offset___deepcopy__():

    offset_1 = abjad.Offset(
        abjad.Fraction(1, 4),
        displacement=abjad.Duration(-1, 16),
    )
    offset_2 = copy.deepcopy(offset_1)

    assert offset_1 == offset_2
    assert offset_1 is not offset_2


def test_duration_Offset___eq__():

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


def test_duration_Offset___ge__():

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


def test_duration_Offset___gt__():

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


def test_duration_Offset___le__():

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


def test_duration_Offset___lt__():

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


def test_duration_Offset___sub__():

    # Offset taken from offset returns duration:
    offset_1 = abjad.Offset(abjad.Fraction(2))
    offset_2 = abjad.Offset(abjad.Fraction(1, 2))
    assert offset_1 - offset_2 == abjad.Duration(3, 2)

    # Duration taken from offset returns another offset:
    offset = abjad.Offset(abjad.Fraction(2))
    duration = abjad.Duration(1, 2)
    assert offset - duration == abjad.Offset(abjad.Fraction(3, 2))
