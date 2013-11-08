# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_BeamSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = BeamSpanner()
    spanner_2 = BeamSpanner()

    assert not spanner_1 == spanner_2
