import copy

import pytest

import abjad


def test_Note___copy___01():
    """
    Copies note.
    """

    note_1 = abjad.Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___02():
    """
    Copies note with LilyPond multiplier.
    """

    note_1 = abjad.Note("c''4", multiplier=(1, 2))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___03():
    """
    Copies note with LilyPond grob overrides and LilyPond context settings.
    """

    note_1 = abjad.Note(12, (1, 4))
    abjad.override(note_1).Staff.NoteHead.color = "#red"
    abjad.override(note_1).Accidental.color = "#red"
    abjad.setting(note_1).tupletFullLength = True
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___04():
    """
    Copies note with grace container.
    """

    note_1 = abjad.Note("c'4")
    grace_container_1 = abjad.AfterGraceContainer([abjad.Note("d'32")])
    abjad.attach(grace_container_1, note_1)

    assert abjad.lilypond(note_1) == abjad.string.normalize(
        r"""
        \afterGrace
        c'4
        {
            d'32
        }
        """
    )

    note_2 = copy.copy(note_1)
    grace_container_2 = abjad.get.after_grace_container(note_2)

    assert abjad.lilypond(note_2) == abjad.string.normalize(
        r"""
        \afterGrace
        c'4
        {
            d'32
        }
        """
    )

    assert note_1 is not note_2
    assert grace_container_1 is not grace_container_2
    assert isinstance(grace_container_1, abjad.AfterGraceContainer)


def test_Note___copy___05():
    """
    Deepcopies orphan note.
    """

    note = abjad.Note("c'4")
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, note)
    grace = abjad.BeforeGraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).NoteHead.color = "#red"

    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        \grace {
            d'16
        }
        \once \override NoteHead.color = #red
        c'4
        - \staccato
        """
    )

    new_note = copy.deepcopy(note)

    assert new_note is not note
    assert abjad.lilypond(new_note) == abjad.lilypond(note)


def test_Note___copy___06():
    """
    Deepcopies note in score.
    """

    staff = abjad.Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, note)
    grace = abjad.BeforeGraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).NoteHead.color = "#red"

    assert abjad.lilypond(staff) == abjad.string.normalize(
        r"""
        \new Staff
        {
            \grace {
                d'16
            }
            \once \override NoteHead.color = #red
            c'8
            - \staccato
            [
            c'8
            e'8
            f'8
            ]
        }
        """
    )

    new_note = copy.deepcopy(note)

    assert new_note is not note
    assert abjad.get.parentage(note).get_parent() is staff
    assert abjad.get.parentage(new_note).get_parent() is not staff
    assert isinstance(abjad.get.parentage(new_note).get_parent(), abjad.Staff)
    assert abjad.lilypond(new_note) == abjad.lilypond(note)
    assert abjad.lilypond(abjad.get.parentage(note).get_parent()) == abjad.lilypond(
        abjad.get.parentage(new_note).get_parent()
    )


def test_Note___copy___07():
    """
    Copies note with tweaks in notehead.
    """

    note = abjad.Note("c'4")
    abjad.tweak(note.get_note_head(), r"\tweak color #red")
    abjad.tweak(note.get_note_head(), r"\tweak Accidental.color #red")
    copied_note = copy.copy(note)
    string = abjad.lilypond(copied_note)
    assert string == abjad.string.normalize(
        r"""
        \tweak Accidental.color #red
        \tweak color #red
        c'4
        """
    ), print(string)


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


def test_Note__init__06():
    """
    REGRESSION. Initializes note from other note with multiplier.
    """

    note = abjad.Note("cs''4", multiplier=(1, 1))

    assert abjad.lilypond(note) == "cs''4 * 1/1"

    new_note = abjad.Note(note)

    assert abjad.lilypond(new_note) == "cs''4 * 1/1"


def test_Note__init__07():
    """
    Initializes note with French note names.
    """

    note = abjad.Note("dod''8.", language="français")

    assert abjad.lilypond(note) == "cs''8."


def test_Note___init___08():
    """
    Initializes note from chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    note = abjad.Note(chord)

    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        d'4
        """
    )

    assert abjad.wf.is_wellformed(note)


def test_Note___init___09():
    """
    Initializes note from tupletized chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 4))
    chords = abjad.mutate.copy(chord, 3)
    tuplet = abjad.Tuplet("3:2", chords)
    note = abjad.Note(tuplet[0])

    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        d'4
        """
    )

    assert abjad.wf.is_wellformed(note)


def test_Note___init___10():
    """
    Initializes note from beamed chord.
    """

    chord = abjad.Chord([2, 3, 4], (1, 8))
    chords = abjad.mutate.copy(chord, 3)
    voice = abjad.Voice(chords)
    abjad.beam(voice[:])
    note = abjad.Note(voice[0])

    assert abjad.lilypond(note) == abjad.string.normalize(
        r"""
        d'8
        [
        """
    ), print(abjad.lilypond(note))

    assert abjad.wf.is_wellformed(note)


def test_Note___init___17():
    """
    Initializes note with cautionary accidental.
    """

    note = abjad.Note("c'?4")

    assert abjad.lilypond(note) == "c'?4"


def test_Note___init___18():
    """
    Initializes note with forced accidental.
    """

    note = abjad.Note("c'!4")

    assert abjad.lilypond(note) == "c'!4"


def test_Note___init___19():
    """
    Initializes note with both forced and cautionary accidental.
    """

    note = abjad.Note("c'!?4")

    assert abjad.lilypond(note) == "c'!?4"


def test_Note___init___20():
    """
    Initializes note from chord with forced and cautionary accidental.
    """

    chord = abjad.Chord("<c'!? e' g'>4")
    note = abjad.Note(chord)

    assert abjad.lilypond(note) == "c'!?4"


def test_Note___init___21():
    """
    Initializes note with drum pitch.
    """

    note = abjad.Note("sn4")

    assert abjad.lilypond(note) == "snare4"
