# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_spannertools_Spanner__get_my_nth_leaf_01():

    staff = Staff()
    staff.append(Measure((2, 8), "c'8 d'8"))
    staff.append(Measure((2, 8), "e'8 f'8"))
    leaves = select(staff).by_leaf()
    beam = Beam()
    attach(beam, leaves)

    assert format(staff) == stringtools.normalize(
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

    selector = select().by_leaf(flatten=True)
    leaves = selector(staff)

    assert beam._get_my_nth_leaf(0) is leaves[0]
    assert beam._get_my_nth_leaf(1) is leaves[1]
    assert beam._get_my_nth_leaf(2) is leaves[2]
    assert beam._get_my_nth_leaf(3) is leaves[3]

    assert beam._get_my_nth_leaf(-1) is leaves[-1]
    assert beam._get_my_nth_leaf(-2) is leaves[-2]
    assert beam._get_my_nth_leaf(-3) is leaves[-3]
    assert beam._get_my_nth_leaf(-4) is leaves[-4]

    assert pytest.raises(IndexError, 'beam._get_my_nth_leaf(99)')
    assert pytest.raises(IndexError, 'beam._get_my_nth_leaf(-99)')
