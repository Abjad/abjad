import abjad


def test_TimeSignature_is_dyadic_rational_01():
    """
    Make n/12 time_signatures into n/8 time_signatures, where possible.
    """

    assert abjad.TimeSignature((1, 12)).is_dyadic_rational() == (
        1,
        12,
    )
    assert abjad.TimeSignature((2, 12)).is_dyadic_rational() == (
        2,
        12,
    )
    assert abjad.TimeSignature((3, 12)).is_dyadic_rational() == (
        2,
        8,
    )
    assert abjad.TimeSignature((4, 12)).is_dyadic_rational() == (
        4,
        12,
    )
    assert abjad.TimeSignature((5, 12)).is_dyadic_rational() == (
        5,
        12,
    )
    assert abjad.TimeSignature((6, 12)).is_dyadic_rational() == (
        4,
        8,
    )


def test_TimeSignature_is_dyadic_rational_02():
    """
    Make n/14 time_signatures into n/8 time_signatures, where possible.
    """

    assert abjad.TimeSignature((1, 14)).is_dyadic_rational() == (
        1,
        14,
    )
    assert abjad.TimeSignature((2, 14)).is_dyadic_rational() == (
        2,
        14,
    )
    assert abjad.TimeSignature((3, 14)).is_dyadic_rational() == (
        3,
        14,
    )
    assert abjad.TimeSignature((4, 14)).is_dyadic_rational() == (
        4,
        14,
    )
    assert abjad.TimeSignature((5, 14)).is_dyadic_rational() == (
        5,
        14,
    )
    assert abjad.TimeSignature((6, 14)).is_dyadic_rational() == (
        6,
        14,
    )
    assert abjad.TimeSignature((7, 14)).is_dyadic_rational() == (
        4,
        8,
    )


def test_TimeSignature_is_dyadic_rational_03():
    """
    Make n/24 time_signatures into n/16 time_signatures, where possible.
    """

    assert abjad.TimeSignature((1, 24)).is_dyadic_rational() == (
        1,
        24,
    )
    assert abjad.TimeSignature((2, 24)).is_dyadic_rational() == (
        2,
        24,
    )
    assert abjad.TimeSignature((3, 24)).is_dyadic_rational() == (
        2,
        16,
    )
    assert abjad.TimeSignature((4, 24)).is_dyadic_rational() == (
        4,
        24,
    )
    assert abjad.TimeSignature((5, 24)).is_dyadic_rational() == (
        5,
        24,
    )
    assert abjad.TimeSignature((6, 24)).is_dyadic_rational() == (
        4,
        16,
    )
    assert abjad.TimeSignature((7, 24)).is_dyadic_rational() == (
        7,
        24,
    )
    assert abjad.TimeSignature((8, 24)).is_dyadic_rational() == (
        8,
        24,
    )


def test_TimeSignature_is_dyadic_rational_04():
    """
    Make n/24 time_signatures into n/8 time_signatures, where possible.
    """

    assert abjad.TimeSignature((1, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        1,
        24,
    )
    assert abjad.TimeSignature((2, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        2,
        24,
    )
    assert abjad.TimeSignature((3, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        1,
        8,
    )
    assert abjad.TimeSignature((4, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        4,
        24,
    )
    assert abjad.TimeSignature((5, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        5,
        24,
    )
    assert abjad.TimeSignature((6, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        2,
        8,
    )
    assert abjad.TimeSignature((7, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        7,
        24,
    )
    assert abjad.TimeSignature((8, 24)).is_dyadic_rational(abjad.Multiplier(99)) == (
        8,
        24,
    )
