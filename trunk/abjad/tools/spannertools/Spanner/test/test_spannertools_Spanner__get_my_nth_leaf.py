# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_spannertools_Spanner__get_my_nth_leaf_01():

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    beam = spannertools.BeamSpanner()
    beam.attach(staff[:])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
        }
        '''
        )

    leaves = staff.select_leaves()

    assert beam._get_my_nth_leaf(0) is leaves[0]
    assert beam._get_my_nth_leaf(1) is leaves[1]
    assert beam._get_my_nth_leaf(2) is leaves[2]
    assert beam._get_my_nth_leaf(3) is leaves[3]

    assert beam._get_my_nth_leaf(-1) is leaves[-1]
    assert beam._get_my_nth_leaf(-2) is leaves[-2]
    assert beam._get_my_nth_leaf(-3) is leaves[-3]
    assert beam._get_my_nth_leaf(-4) is leaves[-4]

    assert py.test.raises(IndexError, 'beam._get_my_nth_leaf(99)')
    assert py.test.raises(IndexError, 'beam._get_my_nth_leaf(-99)')
