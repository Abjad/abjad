# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_Leaf_number_01():
    r'''Leaves in staff number correctly.
    '''

    staff = Staff("c'8 d'8 e'8")
    assert staff[0].leaf_index == 0
    assert staff[1].leaf_index == 1
    assert staff[2].leaf_index == 2


def test_Leaf_number_02():
    r'''Leaves in measure in staff number correctly.
    '''

    staff = Staff([Measure((3, 8), "c'8 d'8 e'8")])
    leaves = staff.select_leaves()
    assert leaves[0].leaf_index == 0
    assert leaves[1].leaf_index == 1
    assert leaves[2].leaf_index == 2


def test_Leaf_number_03():
    r'''Leaves in multiple measures in staff number corretly.
    '''

    staff = Staff(Measure((2, 8), "c'8 d'8") * 3)
    leaves = staff.select_leaves()
    assert leaves[0].leaf_index == 0
    assert leaves[1].leaf_index == 1
    assert leaves[2].leaf_index == 2
    assert leaves[3].leaf_index == 3
    assert leaves[4].leaf_index == 4
    assert leaves[5].leaf_index == 5


def test_Leaf_number_04():
    r'''Orphan leaves number correctly.
    '''

    note = Note("c'4")
    assert note.leaf_index == 0


def test_Leaf_number_05():
    r'''Leaves number correctly after contents rotation.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff[0].leaf_index == 0
    assert staff[1].leaf_index == 1
    assert staff[2].leaf_index == 2
    assert staff[3].leaf_index == 3

    staff[:] = (staff[-2:] + staff[:2])

    r'''
    \new Staff {
        e'8
        f'8
        c'8
        d'8
    }
    '''

    assert select(staff).is_well_formed()
    assert testtools.compare(
        staff.lilypond_format,
        r'''
        \new Staff {
            e'8
            f'8
            c'8
            d'8
        }
        '''
        )

    assert staff[0].leaf_index == 0
    assert staff[1].leaf_index == 1
    assert staff[2].leaf_index == 2
    assert staff[3].leaf_index == 3
