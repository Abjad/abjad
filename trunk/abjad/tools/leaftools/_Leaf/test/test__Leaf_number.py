from abjad import *
import py.test


def test__Leaf_number_01():
    '''Leaves in staff number correctly.'''

    t = Staff("c'8 d'8 e'8")
    assert t[0].leaf_index == 0
    assert t[1].leaf_index == 1
    assert t[2].leaf_index == 2


def test__Leaf_number_02():
    '''Leaves in measure in staff number correctly.'''

    t = Staff([Measure((3, 8), "c'8 d'8 e'8")])
    leaves = t.leaves
    assert leaves[0].leaf_index == 0
    assert leaves[1].leaf_index == 1
    assert leaves[2].leaf_index == 2


def test__Leaf_number_03():
    '''Leaves in multiple measures in staff number corretly.'''

    t = Staff(Measure((2, 8), "c'8 d'8") * 3)
    leaves = t.leaves
    assert leaves[0].leaf_index == 0
    assert leaves[1].leaf_index == 1
    assert leaves[2].leaf_index == 2
    assert leaves[3].leaf_index == 3
    assert leaves[4].leaf_index == 4
    assert leaves[5].leaf_index == 5


def test__Leaf_number_04():
    '''Orphan leaves number correctly.'''

    t = Note("c'4")
    assert t.leaf_index == 0


def test__Leaf_number_05():
    '''Leaves number correctly after contents rotation.'''

    t = Staff("c'8 d'8 e'8 f'8")

    assert t[0].leaf_index == 0
    assert t[1].leaf_index == 1
    assert t[2].leaf_index == 2
    assert t[3].leaf_index == 3

    t[:] = (t[-2:] + t[:2])

    r'''
    \new Staff {
        e'8
        f'8
        c'8
        d'8
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "\\new Staff {\n\te'8\n\tf'8\n\tc'8\n\td'8\n}"

    assert t[0].leaf_index == 0
    assert t[1].leaf_index == 1
    assert t[2].leaf_index == 2
    assert t[3].leaf_index == 3
