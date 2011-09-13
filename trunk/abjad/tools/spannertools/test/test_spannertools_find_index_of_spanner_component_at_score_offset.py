from abjad import *


def test_spannertools_find_index_of_spanner_component_at_score_offset_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(staff.leaves)

    r'''
    \new Staff {
        c'8 [
        d'8
        e'8
        f'8 ]
    }
    '''

    assert spannertools.find_index_of_spanner_component_at_score_offset(beam, Duration(3, 8)) == 3
