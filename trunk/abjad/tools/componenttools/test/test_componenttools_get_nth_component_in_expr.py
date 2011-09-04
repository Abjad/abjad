from abjad import *
from abjad.tools import sequencetools


def test_componenttools_get_nth_component_in_expr_01():

    staff = Staff([])
    durations = [Duration(n, 16) for n in range(1, 5)]
    notes = notetools.make_notes([0, 2, 4, 5], durations)
    rests = resttools.make_rests(durations)
    leaves = sequencetools.interlace_sequences(notes, rests)
    staff.extend(leaves)

    r'''
    \new Staff {
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
    }
    '''

    assert componenttools.get_nth_component_in_expr(staff, Note, 0) is notes[0]
    assert componenttools.get_nth_component_in_expr(staff, Note, 1) is notes[1]
    assert componenttools.get_nth_component_in_expr(staff, Note, 2) is notes[2]
    assert componenttools.get_nth_component_in_expr(staff, Note, 3) is notes[3]

    assert componenttools.get_nth_component_in_expr(staff, Rest, 0) is rests[0]
    assert componenttools.get_nth_component_in_expr(staff, Rest, 1) is rests[1]
    assert componenttools.get_nth_component_in_expr(staff, Rest, 2) is rests[2]
    assert componenttools.get_nth_component_in_expr(staff, Rest, 3) is rests[3]

    assert componenttools.get_nth_component_in_expr(staff, Staff, 0) is staff


def test_componenttools_get_nth_component_in_expr_02():
    '''Iterates backwards with negative values of n.'''

    staff = Staff([])
    durations = [Duration(n, 16) for n in range(1, 5)]
    notes = notetools.make_notes([0, 2, 4, 5], durations)
    rests = resttools.make_rests(durations)
    leaves = sequencetools.interlace_sequences(notes, rests)
    staff.extend(leaves)

    r'''
    \new Staff {
        c'16
        r16
        d'8
        r8
        e'8.
        r8.
        f'4
        r4
    }
    '''

    assert componenttools.get_nth_component_in_expr(staff, Note, -1) is notes[3]
    assert componenttools.get_nth_component_in_expr(staff, Note, -2) is notes[2]
    assert componenttools.get_nth_component_in_expr(staff, Note, -3) is notes[1]
    assert componenttools.get_nth_component_in_expr(staff, Note, -4) is notes[0]

    assert componenttools.get_nth_component_in_expr(staff, Rest, -1) is rests[3]
    assert componenttools.get_nth_component_in_expr(staff, Rest, -2) is rests[2]
    assert componenttools.get_nth_component_in_expr(staff, Rest, -3) is rests[1]
    assert componenttools.get_nth_component_in_expr(staff, Rest, -4) is rests[0]
