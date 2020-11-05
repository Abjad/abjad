import pytest

import abjad


def test_Note___init___01():
    """
    Initializes note from empty input.
    """

    note = abjad.Note()

    assert abjad.lilypond(note) == "c'4"


def test_Note___init___02():
    """
    Initializes note with pitch in octave zero.
    """

    note = abjad.Note(-37, (1, 4))

    assert abjad.lilypond(note) == "b,,,4"


def test_Note___init___03():
    """
    Initializes note with non-assignable duration.
    """

    with pytest.raises(abjad.AssignabilityError):
        abjad.Note(0, (5, 8))


def test_Note___init___04():
    """
    Initializes note with LilyPond-style pitch string.
    """

    note = abjad.Note("c,,", (1, 4))

    assert abjad.lilypond(note) == "c,,4"


def test_Note___init___05():
    """
    Initializes note with complete LilyPond-style note string.
    """

    note = abjad.Note("cs8.")

    assert abjad.lilypond(note) == "cs8."


def test_Note___init___06():
    """
    Initializes note from chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    note = abjad.Note(chord)

    assert abjad.lilypond(note) == abjad.String.normalize(
        r"""
        d'4
        """
    )

    assert abjad.wf.wellformed(note)


def test_Note___init___07():
    """
    Initializes note from tupletized chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    chords = abjad.mutate.copy(chord, 3)
    tuplet = abjad.Tuplet((2, 3), chords)
    note = abjad.Note(tuplet[0])

    assert abjad.lilypond(note) == abjad.String.normalize(
        r"""
        d'4
        """
    )

    assert abjad.wf.wellformed(note)


def test_Note___init___08():
    """
    Initializes note from beamed chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 8))
    chords = abjad.mutate.copy(chord, 3)
    staff = abjad.Staff(chords)
    abjad.beam(staff[:])
    note = abjad.Note(staff[0])

    assert abjad.lilypond(note) == abjad.String.normalize(
        r"""
        d'8
        [
        """
    ), print(abjad.lilypond(note))

    assert abjad.wf.wellformed(note)


def test_Note___init___09():
    """
    Initializes note from rest.
    """

    rest = abjad.Rest("r8")
    note = abjad.Note(rest)

    assert abjad.lilypond(note) == abjad.String.normalize(
        r"""
        8
        """
    )

    assert abjad.wf.wellformed(note)


def test_Note___init___10():
    """
    Initializes note from tupletized rest.
    """

    tuplet = abjad.Tuplet((2, 3), "r8 r8 r8")
    duration = tuplet[0].written_duration
    note = abjad.Note(tuplet[0])

    assert isinstance(tuplet[0], abjad.Rest)
    assert isinstance(note, abjad.Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == duration
    assert note._parent is None


def test_Note___init___11():
    """
    Initializes note from beamed rest.
    """

    staff = abjad.Staff(
        [abjad.Note(0, (1, 8)), abjad.Rest((1, 8)), abjad.Note(0, (1, 8))]
    )
    abjad.beam(staff[:])
    note = abjad.Note(staff[1])

    assert isinstance(staff[1], abjad.Rest)
    assert isinstance(note, abjad.Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_Note___init___12():
    """
    Initializes notes from skip.
    """

    skip = abjad.Skip((1, 8))
    duration = skip.written_duration
    note = abjad.Note(skip)

    assert isinstance(note, abjad.Note)
    assert dir(skip) == dir(abjad.Skip((1, 4)))
    assert dir(note) == dir(abjad.Note("c'4"))
    assert note._parent is None
    assert note.written_duration == duration


def test_Note___init___13():
    """
    Initializes note from tupletized skip.
    """

    tuplet = abjad.Tuplet((2, 3), "s8 s8 s8")
    duration = tuplet[0].written_duration
    note = abjad.Note(tuplet[0])

    assert isinstance(tuplet[0], abjad.Skip)
    assert isinstance(note, abjad.Note)
    assert tuplet[0]._parent is tuplet
    assert tuplet[0].written_duration == duration
    assert note._parent is None


def test_Note___init___14():
    """
    Initializes note from beamed skip.
    """

    staff = abjad.Staff(
        [abjad.Note(0, (1, 8)), abjad.Skip((1, 8)), abjad.Note(0, (1, 8))]
    )
    abjad.beam(staff[:])
    note = abjad.Note(staff[1])

    assert isinstance(staff[1], abjad.Skip)
    assert isinstance(note, abjad.Note)
    assert staff[1]._parent is staff
    assert note._parent is None


def test_Note___init___15():
    """
    Initializes note with cautionary accidental.
    """

    note = abjad.Note("c'?4")

    assert abjad.lilypond(note) == "c'?4"


def test_Note___init___16():
    """
    Initializes note with forced accidental.
    """

    note = abjad.Note("c'!4")

    assert abjad.lilypond(note) == "c'!4"


def test_Note___init___17():
    """
    Initializes note with both forced and cautionary accidental.
    """

    note = abjad.Note("c'!?4")

    assert abjad.lilypond(note) == "c'!?4"


def test_Note___init___18():
    """
    Initializes note from chord with forced and cautionary accidental.
    """

    chord = abjad.Chord("<c'!? e' g'>4")
    note = abjad.Note(chord)

    assert abjad.lilypond(note) == "c'!?4"


def test_Note___init___19():
    """
    Initialize note with drum pitch.
    """

    note = abjad.Note("sn4")

    assert abjad.lilypond(note) == "snare4"
