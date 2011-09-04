from abjad import *
from abjad.tools import sequencetools
import py.test


def test_sequencetools_yield_all_rotations_of_sequence_01():
    '''Yield all rotations of list.
    '''

    rotations = list(sequencetools.yield_all_rotations_of_sequence([1, 2, 3, 4], -1))
    assert rotations == [[1, 2, 3, 4], [2, 3, 4, 1], [3, 4, 1, 2], [4, 1, 2, 3]]


def test_sequencetools_yield_all_rotations_of_sequence_02():
    '''Yield all rotations of tuple.
    '''

    rotations = list(sequencetools.yield_all_rotations_of_sequence((1, 2, 3, 4), -1))
    assert rotations == [(1, 2, 3, 4), (2, 3, 4, 1), (3, 4, 1, 2), (4, 1, 2, 3)]


def test_sequencetools_yield_all_rotations_of_sequence_03():
    '''Yield all rotations of Abjad container.
    '''

    container = Container("c'8 d'8 e'8")
    rotations = list(sequencetools.yield_all_rotations_of_sequence(container, -1))
    staff = Staff(rotations)

    r'''
    \new Staff {
        {
            c'8
            d'8
            e'8
        }
        {
            d'8
            e'8
            c'8
        }
        {
            e'8
            c'8
            d'8
        }
    }
    '''

    assert componenttools.is_well_formed_component(staff)
    assert staff.format == "\\new Staff {\n\t{\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t{\n\t\td'8\n\t\te'8\n\t\tc'8\n\t}\n\t{\n\t\te'8\n\t\tc'8\n\t\td'8\n\t}\n}"
