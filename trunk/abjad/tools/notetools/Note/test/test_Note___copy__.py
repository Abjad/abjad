# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_Note___copy___01():
    r'''Copy note.
    '''

    note_1 = Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.lilypond_format == note_2.lilypond_format
    assert note_1 is not note_2


def test_Note___copy___02():
    r'''Copy note with LilyPond multiplier.
    '''

    note_1 = Note(12, (1, 4), (1, 2))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert note_1.lilypond_format == note_2.lilypond_format
    assert note_1 is not note_2


def test_Note___copy___03():
    r'''Copy note with LilyPond grob overrides and LilyPond context settings.
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
    r'''Copy note with grace container.
    '''

    note_1 = Note("c'4")
    grace_container_1 = leaftools.GraceContainer(
        [Note("d'32")], kind='after')
    grace_container_1(note_1)

    r'''
    \afterGrace
    c'4
    {
        d'32
    }
    '''

    note_2 = copy.copy(note_1)
    grace_container_2 = note_2.get_grace_containers()[0]

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
    assert testtools.compare(
        note_2.lilypond_format,
        r'''
        \afterGrace
        c'4
        {
            d'32
        }
        '''
        )


def test_Note___copy___05():
    r'''Deepcopy orphan note.
    '''

    note = Note("c'4")
    marktools.Articulation('staccato')(note)
    leaftools.GraceContainer("d'16")
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
    r'''Deepcopy note in score.
    '''

    staff = Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    marktools.Articulation('staccato')(note)
    leaftools.GraceContainer("d'16")
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
    assert note.select_parentage().parent is staff
    assert new_note.select_parentage().parent is not staff
    assert isinstance(new_note.select_parentage().parent, Staff)
    assert new_note.lilypond_format == note.lilypond_format
    assert note.select_parentage().parent.lilypond_format == \
        new_note.select_parentage().parent.lilypond_format
