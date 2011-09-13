from abjad import *


def test_leaftools_get_nth_leaf_in_thread_from_leaf_01():

    staff = Staff(2 * Voice("c'8 d'8 e'8 f'8"))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(staff)
    f(staff)

    r'''
    \new Staff {
      \new Voice {
            c'8
            d'8
            e'8
            f'8
      }
      \new Voice {
            g'8
            a'8
            b'8
            c''8
      }
    }
    '''

    leaves = staff.leaves
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 0) is leaves[0]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 1) is leaves[1]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 2) is leaves[2]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 3) is leaves[3]
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 4) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 5) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 6) is None
    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], 7) is None

    assert leaftools.get_nth_leaf_in_thread_from_leaf(staff.leaves[0], -1) is None
