# -*- coding: utf-8 -*-
import abjad
import pytest


def test_scoretools_Leaf__split_by_duration_01():
    r'''Splits note into assignable notes.

    Does not fracture spanners. Does not tie split notes.
    '''

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32
            d'16.
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_02():
    r'''Splits note into assignable notes.

    Fractures spanners. Does not tie split notes.
    '''

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ]
            d'16. [
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_03():
    r'''Splits note into assignable notes.

    Does not fracture spanners. Does tie split notes.
    '''

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'8
            e'8 ]
        }
        '''
        )

    halves = staff[1]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=False,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ~
            d'16.
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_04():
    r'''Splits note into assignable notes.

    Fractures spanners. Ties split notes.
    '''

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    halves = staff[1]._split_by_duration(
        abjad.Duration(1, 32),
        fracture_spanners=True,
        tie_split_notes=True,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            d'32 ~ ]
            d'16. [
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_05():
    r'''Splits note into tuplet monads.

    Does not fracture spanners. Does not tie split notes.
    '''

    staff = abjad.Staff("c'8 [ d'8 e'8 ]")

    halves = staff[1]._split_by_duration(
        abjad.Duration(1, 24),
        tie_split_notes=False,
        )

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            c'8 [
            \times 2/3 {
                d'16
                d'8
            }
            e'8 ]
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_06():
    r'''REGRESSION.
    
    Splits note into tuplet monads and then fuses monads.

    Does not fracture spanners. Ties split notes.

    This test comes from #272 in GitHub.
    '''

    staff = abjad.Staff(r"\times 2/3 { c'8 [ d'8 e'8 ] }")
    leaf = abjad.inspect(staff).get_leaf(0)
    halves = leaf._split_by_duration((1, 20))

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \times 2/3 {
                \times 4/5 {
                    c'16. ~ [
                    c'16
                }
                d'8
                e'8 ]
            }
        }
        '''
        )

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_07():
    r'''Aassignable duration produces two notes.

    This test comes from a container-crossing spanner bug.
    '''

    voice = abjad.Voice(r"c'8 \times 2/3 { d'8 e'8 f'8 }")
    leaves = abjad.select(voice).by_leaf()
    beam = abjad.Beam()
    abjad.attach(beam, leaves)

    assert format(voice) == abjad.String.normalize(
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
        abjad.Duration(1, 24),
        tie_split_notes=False,
        )

    assert format(voice) == abjad.String.normalize(
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

    assert abjad.inspect(voice).is_well_formed()


def test_scoretools_Leaf__split_by_duration_08():
    r'''Zero-duration produces no change.
    '''

    note = abjad.Note("c'4")

    halves = note._split_by_duration(abjad.Duration(0))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 0
    assert len(right) == 1
    assert isinstance(right[0], abjad.Note)
    assert right[0].written_duration == abjad.Duration(1, 4)


def test_scoretools_Leaf__split_by_duration_09():
    r'''Leaf duration less than split duration produces no change.
    '''

    note = abjad.Note("c'4")

    halves = note._split_by_duration(abjad.Duration(3, 4))
    left, right = halves

    assert len(halves) == 2
    assert len(left) == 1
    assert isinstance(left[0], abjad.Note)
    assert left[0].written_duration == abjad.Duration(1, 4)
    assert len(right) == 0


def test_scoretools_Leaf__split_by_duration_10():
    r'''Returns two lists of zero or more leaves.
    '''

    note = abjad.Note("c'4")

    halves = note._split_by_duration(
        abjad.Duration(1, 8),
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert halves[0][0] is note
    assert halves[1][0] is not note
    assert isinstance(halves[0][0], abjad.Note)
    assert isinstance(halves[1][0], abjad.Note)
    assert halves[0][0].written_duration == abjad.Duration(1, 8)
    assert halves[1][0].written_duration == abjad.Duration(1, 8)
    assert len(abjad.inspect(halves[0][0]).get_logical_tie()) == 1
    assert len(abjad.inspect(halves[1][0]).get_logical_tie()) == 1


def test_scoretools_Leaf__split_by_duration_11():
    r'''Returns two lists of zero or more leaves.
    '''

    note = abjad.Note("c'4")
    halves = note._split_by_duration(abjad.Duration(1, 16))

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], abjad.Note)
    assert isinstance(halves[1][0], abjad.Note)
    assert halves[0][0].written_duration == abjad.Duration(1, 16)
    assert halves[1][0].written_duration == abjad.Duration(3, 16)


def test_scoretools_Leaf__split_by_duration_12():
    r'''Nonassignable power-of-two duration produces two lists.

    Left list contains two notes tied together.

    Right list contains only one note.
    '''

    note = abjad.Note("c'4")

    halves = note._split_by_duration(
        abjad.Duration(5, 32),
        tie_split_notes=False,
        )

    assert isinstance(halves, tuple)
    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    assert isinstance(halves[0][0], abjad.Note)
    assert isinstance(halves[0][1], abjad.Note)
    assert isinstance(halves[1][0], abjad.Note)
    assert halves[0][0].written_duration == abjad.Duration(4, 32)
    assert halves[0][1].written_duration == abjad.Duration(1, 32)
    assert halves[1][0].written_duration == abjad.Duration(3, 32)
    assert len(abjad.inspect(halves[0][0]).get_logical_tie()) == 2
    assert len(abjad.inspect(halves[0][1]).get_logical_tie()) == 2
    assert len(abjad.inspect(halves[1][0]).get_logical_tie()) == 1


def test_scoretools_Leaf__split_by_duration_13():
    r'''Lone spanned leaf results in two spanned leaves.
    '''

    staff = abjad.Staff([abjad.Note("c'4")])
    tie = abjad.Tie()
    abjad.attach(tie, staff[:])
    halves = staff[0]._split_by_duration(abjad.Duration(1, 8))

    assert len(staff) == 2
    for leaf in staff[:]:
        assert abjad.inspect(leaf).get_spanners() == set([tie])
        prototype = (abjad.Tie,)
        assert abjad.inspect(leaf).get_spanner(prototype) is tie

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_14():
    r'''Leaves spanners unchanged.
    '''

    staff = abjad.Staff("c'8 c'8 c'8 c'8")
    beam = abjad.Beam()
    abjad.attach(beam, staff[:])

    halves = staff[0]._split_by_duration(
        abjad.Duration(1, 16),
        tie_split_notes=False,
        )

    assert len(staff) == 5
    for l in staff:
        assert abjad.inspect(l).get_spanners() == set([beam])
        assert l._get_spanner(abjad.Beam) is beam

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_15():
    r'''Returns three leaves with two tied.

    Spanner is shared by all 3 leaves.
    '''

    staff = abjad.Staff([abjad.Note("c'4")])
    tie = abjad.Tie()
    abjad.attach(tie, staff[:])
    halves = staff[0]._split_by_duration(abjad.Duration(5, 32))

    assert len(halves) == 2
    assert len(halves[0]) == 2
    assert len(halves[1]) == 1
    for l in staff:
        assert abjad.inspect(l).get_spanners() == set([tie])
        assert abjad.inspect(l).get_spanner(abjad.Tie) is tie

    assert abjad.inspect(staff).is_well_formed()


def test_scoretools_Leaf__split_by_duration_16():
    r'''After grace notes are removed from first split leaf.
    '''

    note = abjad.Note("c'4")
    after_grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(after_grace, note)
    halves = note._split_by_duration(abjad.Duration(1, 8))

    assert abjad.inspect(halves[0][0]).get_after_grace_container() is None
    assert len(abjad.inspect(halves[1][0]).get_after_grace_container()) == 1


def test_scoretools_Leaf__split_by_duration_17():
    r'''After grace notes are removed from first split leaf.
    '''

    note = abjad.Note("c'4")
    grace = abjad.AfterGraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)
    halves = note._split_by_duration(abjad.Duration(5, 32))

    assert len(halves) == 2
    assert getattr(halves[0][0], 'after_grace', None) is None
    assert getattr(halves[0][1], 'after_grace', None) is None
    assert len(halves[1]) == 1
    after_grace = abjad.inspect(halves[1][0]).get_after_grace_container()
    assert len(after_grace) == 1


def test_scoretools_Leaf__split_by_duration_18():
    r'''Grace notes are removed from second split leaf.
    '''

    note = abjad.Note("c'4")
    grace = abjad.GraceContainer([abjad.Note(0, (1, 32))])
    abjad.attach(grace, note)
    halves = note._split_by_duration(abjad.Duration(1, 16))

    assert len(halves[0]) == 1
    assert len(halves[1]) == 1
    grace_container = abjad.inspect(halves[0][0]).get_grace_container()
    assert len(grace_container) == 1
    assert not hasattr(halves[1][0], 'grace') is None
