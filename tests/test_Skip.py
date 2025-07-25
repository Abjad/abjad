import copy

import abjad


def test_Skip___copy___01():
    """
    Copies skip.
    """

    skip_1 = abjad.Skip((1, 4))
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

    skip_1 = abjad.Skip((1, 4))
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

    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3


def test_Skip___init___01():
    """
    Initializes skip from LilyPond input string.
    """

    skip = abjad.Skip("s8.")

    assert isinstance(skip, abjad.Skip)


def test_Skip___init___02():
    """
    Initializes skip from orphan chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    skip = abjad.Skip(chord)

    assert isinstance(skip, abjad.Skip)
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert abjad.get.parentage(skip).get_parent() is None
    assert skip.get_written_duration() == chord.get_written_duration()


def test_Skip___init___03():
    """
    Initializes skip from chord with parent.
    """

    tuplet = abjad.Tuplet("3:2", "<d' ef' e'>4 f' g'")
    skip = abjad.Skip(tuplet[0])

    assert isinstance(tuplet[0], abjad.Chord)
    assert isinstance(skip, abjad.Skip)
    assert abjad.get.parentage(tuplet[0]).get_parent() is tuplet
    assert abjad.get.parentage(skip).get_parent() is None
    assert tuplet[0].get_written_duration() == skip.get_written_duration()


def test_Skip___init___05():
    """
    Initializes skip from orphan note.
    """

    note = abjad.Note(2, (1, 8))
    skip = abjad.Skip(note)

    assert isinstance(note, abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert dir(note) == dir(abjad.Note("c'4"))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert abjad.get.parentage(note).get_parent() is None
    assert abjad.get.parentage(skip).get_parent() is None
    assert note.get_written_duration() == skip.get_written_duration()


def test_Skip___init___06():
    """
    Initializes skip from tupletized note.
    """

    tuplet = abjad.Tuplet("3:2", "c'8 c'8 c'8")
    skip = abjad.Skip(tuplet[0])

    assert isinstance(tuplet[0], abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert abjad.get.parentage(tuplet[0]).get_parent() is tuplet
    assert abjad.get.parentage(skip).get_parent() is None
    assert tuplet[0].get_written_duration() == skip.get_written_duration()


def test_Skip___init___07():
    """
    Initializes skip from orphan rest.
    """

    rest = abjad.Rest((1, 8))
    skip = abjad.Skip(rest)

    assert isinstance(skip, abjad.Skip)
    assert dir(rest) == dir(abjad.Rest((1, 4)))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert abjad.get.parentage(skip).get_parent() is None
    assert skip.get_written_duration() == rest.get_written_duration()


def test_Skip___init___08():
    """
    Initializes skip from tupletized rest.
    """

    tuplet = abjad.Tuplet("3:2", "r8 r8 r8")
    skip = abjad.Skip(tuplet[0])

    assert isinstance(tuplet[0], abjad.Rest)
    assert isinstance(skip, abjad.Skip)
    assert abjad.get.parentage(tuplet[0]).get_parent() is tuplet
    assert abjad.get.parentage(skip).get_parent() is None
    assert tuplet[0].get_written_duration() == skip.get_written_duration()


def test_Skip___ne___01():
    """
    Compares skips by inequality.
    """

    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

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
