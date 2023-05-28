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
    abjad.override(skip_1).Staff.NoteHead.color = "#red"
    abjad.override(skip_1).Accidental.color = "#red"
    abjad.setting(skip_1).tupletFullLength = True
    skip_2 = copy.copy(skip_1)

    assert isinstance(skip_1, abjad.Skip)
    assert isinstance(skip_2, abjad.Skip)
    assert abjad.lilypond(skip_1) == abjad.lilypond(skip_2)
    assert skip_1 is not skip_2


def test_Skip___eq___01():
    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

    assert not skip_1 == skip_2
    assert not skip_1 == skip_3
    assert not skip_2 == skip_3


def test_Skip___init___01():
    """
    Initialize skip from LilyPond input string.
    """

    skip = abjad.Skip("s8.")
    assert isinstance(skip, abjad.Skip)


def test_Skip___init___02():
    """
    Initialize skip from containerize note.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    duration = chord.written_duration
    skip = abjad.Skip(chord)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(chord) == dir(abjad.Chord([2, 3, 4], (1, 4)))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == duration


def test_Skip___init___03():
    """
    Initialize skip from tupletized note.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    chords = abjad.mutate.copy(chord, 3)
    tuplet = abjad.Tuplet((2, 3), chords)
    duration = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(tuplet[0], abjad.Chord)
    assert isinstance(skip, abjad.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == duration
    assert skip._parent is None


def test_Skip___init___04():
    """
    Initialize skip from beamed chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    chords = abjad.mutate.copy(chord, 3)
    staff = abjad.Staff(chords)
    abjad.beam(staff[:])
    skip = abjad.Skip(staff[0])
    assert isinstance(staff[0], abjad.Chord)
    assert isinstance(skip, abjad.Skip)
    assert staff[0]._parent is staff
    assert skip._parent is None


def test_Skip___init___05():
    note = abjad.Note(2, (1, 8))
    duration = note.written_duration
    skip = abjad.Skip(note)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(note) == dir(abjad.Note("c'4"))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert abjad.lilypond(skip) == "s8"
    assert skip._parent is None
    assert skip.written_duration == duration


def test_Skip___init___06():
    tuplet = abjad.Tuplet((2, 3), "c'8 c'8 c'8")
    duration = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(tuplet[0], abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == duration


def test_Skip___init___07():
    """
    Initialize skip from beamed note.
    """

    voice = abjad.Voice("c'8 c'8 c'8")
    abjad.beam(voice[:])
    skip = abjad.Skip(voice[0])
    assert isinstance(voice[0], abjad.Note)
    assert isinstance(skip, abjad.Skip)
    assert voice[0]._parent is voice


def test_Skip___init___08():
    """
    Initialize skip from unincorporaed rest.
    """

    rest = abjad.Rest((1, 8))
    duration = rest.written_duration
    skip = abjad.Skip(rest)
    assert isinstance(skip, abjad.Skip)
    # check that attributes have not been removed or added.
    assert dir(rest) == dir(abjad.Rest((1, 4)))
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert skip._parent is None
    assert skip.written_duration == duration


def test_Skip___init___09():
    """
    Initialize skip from tupletized rest.
    """

    tuplet = abjad.Tuplet((2, 3), "r8 r8 r8")
    duration = tuplet[0].written_duration
    skip = abjad.Skip(tuplet[0])
    assert isinstance(skip, abjad.Skip)
    assert isinstance(tuplet[0], abjad.Rest)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == duration
    assert skip._parent is None


def test_Skip___init___10():
    """
    Initialize skip from spanned rest.
    """

    voice = abjad.Voice(
        [abjad.Note(0, (1, 8)), abjad.Rest((1, 8)), abjad.Note(0, (1, 8))]
    )
    abjad.beam(voice[:])
    skip = abjad.Skip(voice[1])
    assert isinstance(skip, abjad.Skip)
    assert isinstance(voice[1], abjad.Rest)
    assert voice[1]._parent is voice
    assert skip._parent is None


def test_Skip___ne___01():
    skip_1 = abjad.Skip((1, 4))
    skip_2 = abjad.Skip((1, 4))
    skip_3 = abjad.Skip((1, 8))

    assert skip_1 != skip_2
    assert skip_1 != skip_3
    assert skip_2 != skip_3
