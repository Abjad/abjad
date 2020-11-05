import copy

import abjad


def test_Note___copy___01():
    """
    Copy note.
    """

    note_1 = abjad.Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___02():
    """
    Copy note with LilyPond multiplier.
    """

    note_1 = abjad.Note("c''4", multiplier=(1, 2))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___03():
    """
    Copy note with LilyPond grob abjad.overrides and LilyPond context settings.
    """

    note_1 = abjad.Note(12, (1, 4))
    abjad.override(note_1).staff.note_head.color = "red"
    abjad.override(note_1).accidental.color = "red"
    abjad.setting(note_1).tuplet_full_length = True
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, abjad.Note)
    assert isinstance(note_2, abjad.Note)
    assert abjad.lilypond(note_1) == abjad.lilypond(note_2)
    assert note_1 is not note_2


def test_Note___copy___04():
    """
    Copy note with grace container.
    """

    note_1 = abjad.Note("c'4")
    grace_container_1 = abjad.AfterGraceContainer([abjad.Note("d'32")])
    abjad.attach(grace_container_1, note_1)

    assert abjad.lilypond(note_1) == abjad.String.normalize(
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

    assert abjad.lilypond(note_2) == abjad.String.normalize(
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
    Deepcopy orphan note.
    """

    note = abjad.Note("c'4")
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, note)
    grace = abjad.BeforeGraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).note_head.color = "red"

    assert abjad.lilypond(note) == abjad.String.normalize(
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
    Deepcopy note in score.
    """

    staff = abjad.Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    articulation = abjad.Articulation("staccato")
    abjad.attach(articulation, note)
    grace = abjad.BeforeGraceContainer("d'16")
    abjad.attach(grace, note)
    abjad.override(note).note_head.color = "red"

    assert abjad.lilypond(staff) == abjad.String.normalize(
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
    assert abjad.get.parentage(note).parent is staff
    assert abjad.get.parentage(new_note).parent is not staff
    assert isinstance(abjad.get.parentage(new_note).parent, abjad.Staff)
    assert abjad.lilypond(new_note) == abjad.lilypond(note)
    assert abjad.lilypond(abjad.get.parentage(note).parent) == abjad.lilypond(
        abjad.get.parentage(new_note).parent
    )
