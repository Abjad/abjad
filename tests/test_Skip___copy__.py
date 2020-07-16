import copy

import abjad


def test_Skip___copy___01():
    """
    Copy skip.
    """

    skip_1 = abjad.Skip((1, 4))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___copy___02():
    """
    Copy skip with LilyPond multiplier.
    """

    skip_1 = abjad.Skip("s4", multiplier=(1, 2))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___copy___03():
    """
    Copy skip with LilyPond grob overrides and LilyPond context settings.
    """

    skip_1 = abjad.Skip((1, 4))
    abjad.override(skip_1).staff.note_head.color = "red"
    abjad.override(skip_1).accidental.color = "red"
    abjad.setting(skip_1).tuplet_full_length = True
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2
