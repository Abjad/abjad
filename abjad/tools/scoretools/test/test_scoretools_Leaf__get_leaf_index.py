# -*- coding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_Leaf__get_leaf_index_01():
    r'''Leaves in staff number correctly.
    '''

    staff = Staff("c'8 d'8 e'8")
    assert staff[0]._get_leaf_index() == 0
    assert staff[1]._get_leaf_index() == 1
    assert staff[2]._get_leaf_index() == 2


def test_scoretools_Leaf__get_leaf_index_02():
    r'''Leaves in measure in staff number correctly.
    '''

    staff = Staff([Measure((3, 8), "c'8 d'8 e'8")])
    leaves = select(staff).by_leaf()
    assert leaves[0]._get_leaf_index() == 0
    assert leaves[1]._get_leaf_index() == 1
    assert leaves[2]._get_leaf_index() == 2


def test_scoretools_Leaf__get_leaf_index_03():
    r'''Leaves in multiple measures in staff number corretly.
    '''

    staff = Staff(Measure((2, 8), "c'8 d'8") * 3)
    leaves = select(staff).by_leaf()
    assert leaves[0]._get_leaf_index() == 0
    assert leaves[1]._get_leaf_index() == 1
    assert leaves[2]._get_leaf_index() == 2
    assert leaves[3]._get_leaf_index() == 3
    assert leaves[4]._get_leaf_index() == 4
    assert leaves[5]._get_leaf_index() == 5


def test_scoretools_Leaf__get_leaf_index_04():
    r'''Orphan leaves number correctly.
    '''

    note = Note("c'4")
    assert note._get_leaf_index() == 0


def test_scoretools_Leaf__get_leaf_index_05():
    r'''Leaves number correctly after contents rotation.
    '''

    staff = Staff("c'8 d'8 e'8 f'8")

    assert staff[0]._get_leaf_index() == 0
    assert staff[1]._get_leaf_index() == 1
    assert staff[2]._get_leaf_index() == 2
    assert staff[3]._get_leaf_index() == 3

    staff[:] = (staff[-2:] + staff[:2])

    r'''
    \new Staff {
        e'8
        f'8
        c'8
        d'8
    }
    '''

    assert inspect_(staff).is_well_formed()
    assert format(staff) == stringtools.normalize(
        r'''
        \new Staff {
            e'8
            f'8
            c'8
            d'8
        }
        '''
        )

    assert staff[0]._get_leaf_index() == 0
    assert staff[1]._get_leaf_index() == 1
    assert staff[2]._get_leaf_index() == 2
    assert staff[3]._get_leaf_index() == 3
