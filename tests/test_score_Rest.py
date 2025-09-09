import copy

import abjad


def test_Rest___cmp___01():
    rest_1 = abjad.Rest("r4")
    rest_2 = abjad.Rest("r4")
    rest_3 = abjad.Rest("r8")

    assert not rest_1 == rest_2
    assert not rest_1 == rest_3
    assert not rest_2 == rest_3


def test_Rest___cmp___02():
    rest_1 = abjad.Rest("r4")
    rest_2 = abjad.Rest("r4")
    rest_3 = abjad.Rest("r8")

    assert rest_1 != rest_2
    assert rest_1 != rest_3
    assert rest_2 != rest_3


def test_Rest___copy___01():
    """
    Copies rest.
    """

    rest_1 = abjad.Rest("r4")
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2


def test_Rest___copy___02():
    """
    Copies rest with LilyPond multiplier.
    """

    rest_1 = abjad.Rest("r4", multiplier=(1, 2))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2


def test_Rest___copy___03():
    """
    Copies rest with LilyPond grob overrides and LilyPond context settings.
    """

    rest_1 = abjad.Rest("r4")
    abjad.override(rest_1).Staff.NoteHead.color = "#red"
    abjad.override(rest_1).Accidental.color = "#red"
    abjad.setting(rest_1).tupletFullLength = True
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2


def test_Rest___init___01():
    """
    Initializes rest from LilyPond input string.
    """

    rest = abjad.Rest("r8.")

    assert rest.written_duration() == abjad.Duration(3, 16)
