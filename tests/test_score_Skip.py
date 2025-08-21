import copy

import abjad


def test_Skip___copy___01():
    """
    Copies skip.
    """

    skip_1 = abjad.Skip("s4")
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___copy___02():
    """
    Copies skip with LilyPond multiplier.
    """

    skip_1 = abjad.Skip("s4", multiplier=(1, 2))
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___copy___03():
    """
    Copies skip with LilyPond grob overrides and LilyPond context settings.
    """

    skip_1 = abjad.Skip("s4")
    abjad.override(skip_1).Staff.NoteHead.color = "#red"
    abjad.override(skip_1).Accidental.color = "#red"
    abjad.setting(skip_1).tupletFullLength = True
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___eq___01():
    """
    Compares skips by equality.
    """

    skip_1 = abjad.Skip("s4")
    skip_2 = abjad.Skip("s4")
    skip_3 = abjad.Skip("s8")

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3


def test_Skip___init___01():
    """
    Initializes skip from LilyPond input string.
    """

    skip = abjad.Skip("s8.")

    assert isinstance(skip, abjad.Skip)


def test_Skip___ne___01():
    """
    Compares skips by inequality.
    """

    skip_1 = abjad.Skip("s4")
    skip_2 = abjad.Skip("s4")
    skip_3 = abjad.Skip("s8")

    assert skip_1 != skip_2
    assert skip_1 != skip_3
    assert skip_2 != skip_3


def test_Skip_tag_01():
    """
    Skips may be tagged.
    """

    skip = abjad.Skip("s8.", tag=abjad.Tag("GLOBAL_SKIP"))

    assert abjad.lilypond(skip, tags=True) == abjad.string.normalize(
        """
          %! GLOBAL_SKIP
        s8.
        """
    )
