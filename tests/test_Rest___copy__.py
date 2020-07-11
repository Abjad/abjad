import copy

import abjad


def test_Rest___copy___01():
    """
    Copy rest.
    """

    rest_1 = abjad.Rest((1, 4))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2


def test_Rest___copy___02():
    """
    Copy rest with LilyPond multiplier.
    """

    rest_1 = abjad.Rest("r4", multiplier=(1, 2))
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2


def test_Rest___copy___03():
    """
    Copy rest with LilyPond grob overrides and LilyPond context settings.
    """

    rest_1 = abjad.Rest((1, 4))
    abjad.override(rest_1).staff.note_head.color = "red"
    abjad.override(rest_1).accidental.color = "red"
    abjad.setting(rest_1).tuplet_full_length = True
    rest_2 = copy.copy(rest_1)

    assert isinstance(rest_1, abjad.Rest)
    assert isinstance(rest_2, abjad.Rest)
    assert abjad.lilypond(rest_1) == abjad.lilypond(rest_2)
    assert rest_1 is not rest_2
