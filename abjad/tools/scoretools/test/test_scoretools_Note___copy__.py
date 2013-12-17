# -*- encoding: utf-8 -*-
import copy
from abjad import *


def test_scoretools_Note___copy___01():
    r'''Copy note.
    '''

    note_1 = Note(12, (1, 4))
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___02():
    r'''Copy note with LilyPond multiplier.
    '''

    note_1 = Note("c''4")
    attach(Multiplier(1, 2), note_1)
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___03():
    r'''Copy note with LilyPond grob overrides and LilyPond context settings.
    '''

    note_1 = Note(12, (1, 4))
    override(note_1).staff.note_head.color = 'red'
    override(note_1).accidental.color = 'red'
    contextualize(note_1).tuplet_full_length = True
    note_2 = copy.copy(note_1)

    assert isinstance(note_1, Note)
    assert isinstance(note_2, Note)
    assert format(note_1) == format(note_2)
    assert note_1 is not note_2


def test_scoretools_Note___copy___04():
    r'''Copy note with grace container.
    '''

    note_1 = Note("c'4")
    grace_container_1 = scoretools.GraceContainer([Note("d'32")], kind='after')
    attach(grace_container_1, note_1)

    assert systemtools.TestManager.compare(
        note_1,
        r'''
        \afterGrace
        c'4
        {
            d'32
        }
        '''
        )

    note_2 = copy.copy(note_1)
    grace_container_2 = inspect(note_2).get_grace_containers()[0]

    assert note_1 is not note_2
    assert grace_container_1 is not grace_container_2
    assert grace_container_1.kind == grace_container_2.kind == 'after'
    assert systemtools.TestManager.compare(
        note_2,
        r'''
        \afterGrace
        c'4
        {
            d'32
        }
        '''
        )


def test_scoretools_Note___copy___05():
    r'''Deepcopy orphan note.
    '''

    note = Note("c'4")
    articulation = Articulation('staccato')
    attach(articulation, note)
    grace = scoretools.GraceContainer("d'16")
    attach(grace, note)
    override(note).note_head.color = 'red'

    assert systemtools.TestManager.compare(
        note,
        r'''
        \grace {
            d'16
        }
        \once \override NoteHead #'color = #red
        c'4 -\staccato
        '''
        )

    new_note = copy.deepcopy(note)

    assert not new_note is note
    assert format(new_note) == format(note)


def test_scoretools_Note___copy___06():
    r'''Deepcopy note in score.
    '''

    staff = Staff("c'8 [ c'8 e'8 f'8 ]")
    note = staff[0]
    articulation = Articulation('staccato')
    attach(articulation, note)
    grace = scoretools.GraceContainer("d'16")
    attach(grace, note)
    override(note).note_head.color = 'red'

    assert systemtools.TestManager.compare(
        staff,
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
        )

    new_note = copy.deepcopy(note)

    assert new_note is not note
    assert inspect(note).get_parentage().parent is staff
    assert inspect(new_note).get_parentage().parent is not staff
    assert isinstance(inspect(new_note).get_parentage().parent, Staff)
    assert format(new_note) == format(note)
    assert format(inspect(note).get_parentage().parent) == \
        format(inspect(new_note).get_parentage().parent)


def test_scoretools_Note___copy___07():
    r'''Copying note does note copy hairpin.
    '''

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    crescendo = Crescendo()
    attach(crescendo, staff[:4])

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )

    new_note = copy.copy(staff[0])
    staff.append(new_note)

    assert systemtools.TestManager.compare(
        staff,
        r'''
        \new Staff {
            c'8 \<
            cs'8
            d'8
            ef'8 \!
            e'8
            f'8
            fs'8
            g'8
            c'8
        }
        '''
        )
    assert inspect(staff).is_well_formed()
