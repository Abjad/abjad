from abjad import *
import copy


def test_Note___copy___01():
    '''Copy note.
    '''

    note_1 = Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.lilypond_format == note_2.lilypond_format
    assert note_1 is not note_2


def test_Note___copy___02():
    '''Copy note with LilyPond multiplier.
    '''

    note_1 = Note(12, (1, 4), (1, 2))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.lilypond_format == note_2.lilypond_format
    assert note_1 is not note_2


def test_Note___copy___03():
    '''Copy note with LilyPond grob overrides and LilyPond context settings.
    '''

    note_1 = Note(12, (1, 4))
    note_1.override.staff.note_head.color = 'red'
    note_1.override.accidental.color = 'red'
    note_1.set.tuplet_full_length = True
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.lilypond_format == note_2.lilypond_format
    assert note_1 is not note_2


def test_Note___copy___04():
    '''Copy note with grace container.
    '''

    note_1 = Note("c'4")
    grace_container_1 = gracetools.GraceContainer([Note("d'32")], kind = 'after')
    grace_container_1(note_1)

    r'''
    \afterGrace
    c'4
    {
        d'32
    }
    '''

    note_2 = copy.copy(note_1)
    grace_container_2 = gracetools.get_grace_containers_attached_to_leaf(note_2)[0]

    r'''
    \afterGrace
    c'4
    {
        d'32
    }
    '''

    assert note_1 is not note_2
    assert grace_container_1 is not grace_container_2
    assert grace_container_1.kind == grace_container_2.kind == 'after'
    assert note_2.lilypond_format == "\\afterGrace\nc'4\n{\n\td'32\n}"


def test_Note___copy___05():
    '''Deepcopy orphan note.
    '''

    note = Note("c'4")
    marktools.Articulation('staccato')(note)
    gracetools.GraceContainer("d'16")
    note.override.note_head.color = 'red'

    r'''
    \grace {
        d'16
    }
    \once \override NoteHead #'color = #red
    c'4 -\staccato
    '''

    new_note = copy.deepcopy(note)

    assert not new_note is note
    assert new_note.lilypond_format == note.lilypond_format


def test_Note___copy___06():
    '''Deepcopy note in score.
    '''

    staff = Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    marktools.Articulation('staccato')(note)
    gracetools.GraceContainer("d'16")
    note.override.note_head.color = 'red'

    r'''
    \new Staff {
        \grace {
            d'16
        }
        \once \override NoteHead #'color = #red
        c'8 -\staccato [
        c'8
        e'8
        f'8 ]
    }
    '''

    new_note = copy.deepcopy(note)

    assert new_note is not note
    assert note.parent is staff
    assert new_note.parent is not staff
    assert isinstance(new_note.parent, Staff)
    assert new_note.lilypond_format == note.lilypond_format
    assert note.parent.lilypond_format == new_note.parent.lilypond_format
