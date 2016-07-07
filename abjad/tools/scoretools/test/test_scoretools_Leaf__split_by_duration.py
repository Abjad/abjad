# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Leaf__split_by_duration_01():
    r'''Split note into assignable notes.
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32
            d'16.
            e'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_02():
    r'''Split note into assignable notes.
    Fracture spanners. But don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ]
            d'16. [
            e'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_03():
    r'''Split note into assignable notes.
    Don't fracture spanners. But do tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ~
            d'16.
            e'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_04():
    r'''Split note into assignable notes.
    Fracture spanners and tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    halves = staff[1]._split_by_duration(
        Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ~ ]
            d'16. [
            e'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_05():
    r'''Split note into tuplet monads.
    Don't fracture spanners. Don't tie split notes.
    '''

    staff = Staff("c'8 [ d'8 e'8 ]")

    halves = staff[1]._split_by_duration(
        Duration(1, 24),
        tie_split_notes=False,
        )

    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            c'8 [
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'16
            }
            \tweak edge-height #'(0.7 . 0)
            \times 2/3 {
                d'8
            }
            e'8 ]
        }
        '''
        )

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_06():
    r'''Notehead-assignable duration produces two notes.
    This test comes from a container-crossing spanner bug.
    '''

    voice = Voice(r"c'8 \times 2/3 { d'8 e'8 f'8 }")
    leaves = select(voice).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'8
                e'8
                f'8 ]
            }
        }
        '''
        )

    halves = leaves[1]._split_by_duration(
        Duration(1, 24),
        tie_split_notes=False,
        )

    assert format(voice) == stringtools.normalize(
        r'''
        \new Voice {
            c'8 [
            \times 2/3 {
                d'16
                d'16
                e'8
                f'8 ]
            }
        }
        '''
        )

    assert inspect_(voice).is_well_formed()


def test_scoretools_Leaf__split_by_duration_07():
    r'''Split duration equal to zero produces no change.
    '''

    note = Note("c'4")

    halves = note._split_by_duration(Duration(0))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 0
    assert len(right) == 1
    assert isinstance(right[0], Note)
    assert right[0].written_duration == Duration(1, 4)


def test_scoretools_Leaf__split_by_duration_08():
    r'''Leaf duration less than split duration produces no change.
    '''

    note = Note("c'4")

    halves = note._split_by_duration(Duration(3, 4))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 1
    assert isinstance(left[0], Note)
    assert left[0].written_duration == Duration(1, 4)
    assert len(right) == 0


def test_scoretools_Leaf__split_by_duration_09():
    r'''Split returns two lists of zero or more leaves.
    '''

    note = Note("c'4")

    halves = note._split_by_duration(
        Duration(1, 8),
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert halves[0][0] is note
    assert halves[1][0] is not note
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 8)
    assert halves[1][0].written_duration == Duration(1, 8)
    assert len(inspect_(halves[0][0]).get_logical_tie()) == 1
    assert len(inspect_(halves[1][0]).get_logical_tie()) == 1


def test_scoretools_Leaf__split_by_duration_10():
    r'''Split returns two lists of zero or more.
    '''

    note = Note("c'4")
    halves = note._split_by_duration(Duration(1, 16))

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(1, 16)
    assert halves[1][0].written_duration == Duration(3, 16)


def test_scoretools_Leaf__split_by_duration_11():
    r'''Nonassignable split duration with power-of-two denominator
    produces two lists.
    Left list contains two notes tied together.
    Right list contains only one note.
    '''

    note = Note("c'4")

    halves = note._split_by_duration(
        Duration(5, 32),
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], Note)
    assert isinstance(halves[0][1], Note)
    assert isinstance(halves[1][0], Note)
    assert halves[0][0].written_duration == Duration(4, 32)
    assert halves[0][1].written_duration == Duration(1, 32)
    assert halves[1][0].written_duration == Duration(3, 32)
    assert len(inspect_(halves[0][0]).get_logical_tie()) == 2
    assert len(inspect_(halves[0][1]).get_logical_tie()) == 2
    assert len(inspect_(halves[1][0]).get_logical_tie()) == 1


def test_scoretools_Leaf__split_by_duration_12():
    r'''Lone spanned Leaf results in two spanned leaves.
    '''

    staff = Staff([Note("c'4")])
    tie = spannertools.Tie()
    attach(tie, staff[:])
    halves = staff[0]._split_by_duration(Duration(1, 8))

    assert len(staff) == 2
    for leaf in staff[:]:
        assert inspect_(leaf).get_spanners() == set([tie])
        prototype = (spannertools.Tie,)
        assert inspect_(leaf).get_spanner(prototype) is tie

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_13():
    r'''Spanners are unaffected by leaf split.
    '''

    staff = Staff("c'8 c'8 c'8 c'8")
    beam = Beam()
    attach(beam, staff[:])

    halves = staff[0]._split_by_duration(
        Duration(1, 16),
        tie_split_notes=False,
        )

    assert len(staff) == 5
    for l in staff:
        assert inspect_(l).get_spanners() == set([beam])
        assert l._get_spanner(Beam) is beam

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_14():
    r'''Split returns three leaves, two are tied.
    Spanner is shared by all 3 leaves.
    '''

    staff = Staff([Note("c'4")])
    tie = spannertools.Tie()
    attach(tie, staff[:])
    halves = staff[0]._split_by_duration(Duration(5, 32))

    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    for l in staff:
        assert inspect_(l).get_spanners() == set([tie])
        assert inspect_(l).get_spanner(spannertools.Tie) is tie

    assert inspect_(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_15():
    r'''After grace notes are removed from first leaf in bipartition.
    '''

    note = Note("c'4")
    grace = scoretools.GraceContainer([Note(0, (1, 32))], kind='after')
    attach(grace, note)
    halves = note._split_by_duration(Duration(1, 8))

    assert not hasattr(halves[0][0], 'after_grace')
    after_grace = inspect_(halves[1][0]).get_grace_container()
    assert len(after_grace) == 1


def test_scoretools_Leaf__split_by_duration_16():
    r'''After grace notes are removed from first tied leaves in bipartition.
    '''

    note = Note("c'4")
    grace = scoretools.GraceContainer([Note(0, (1, 32))], kind='after')
    attach(grace, note)
    halves = note._split_by_duration(Duration(5, 32))

    assert len(halves) == 2
    assert getattr(halves[0][0], 'after_grace', None) is None
    assert getattr(halves[0][1], 'after_grace', None) is None
    assert len(halves[1]) == 1
    after_grace = inspect_(halves[1][0]).get_grace_container()
    assert len(after_grace) == 1


def test_scoretools_Leaf__split_by_duration_17():
    r'''Grace notes are removed from second leaf in bipartition.
    '''

    note = Note("c'4")
    grace = scoretools.GraceContainer([Note(0, (1, 32))])
    attach(grace, note)
    halves = note._split_by_duration(Duration(1, 16))

    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    grace_container = inspect_(halves[0][0]).get_grace_container()
    assert len(grace_container) == 1
    assert not hasattr(halves[1][0], 'grace') is None
