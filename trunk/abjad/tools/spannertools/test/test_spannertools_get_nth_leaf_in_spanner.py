from abjad import *
import py.test


def test_spannertools_get_nth_leaf_in_spanner_01():

    t = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
    p = spannertools.BeamSpanner(t[:])

    r'''
    \new Staff {
        {
            \time 2/8
            c'8 [
            d'8
        }
        {
            \time 2/8
            e'8
            f'8 ]
        }
    }
    '''

    leaves = t.leaves

    assert spannertools.get_nth_leaf_in_spanner(p, 0) is leaves[0]
    assert spannertools.get_nth_leaf_in_spanner(p, 1) is leaves[1]
    assert spannertools.get_nth_leaf_in_spanner(p, 2) is leaves[2]
    assert spannertools.get_nth_leaf_in_spanner(p, 3) is leaves[3]

    assert spannertools.get_nth_leaf_in_spanner(p, -1) is leaves[-1]
    assert spannertools.get_nth_leaf_in_spanner(p, -2) is leaves[-2]
    assert spannertools.get_nth_leaf_in_spanner(p, -3) is leaves[-3]
    assert spannertools.get_nth_leaf_in_spanner(p, -4) is leaves[-4]

    assert py.test.raises(IndexError, 'spannertools.get_nth_leaf_in_spanner(p, 99)')
    assert py.test.raises(IndexError, 'spannertools.get_nth_leaf_in_spanner(p, -99)')
