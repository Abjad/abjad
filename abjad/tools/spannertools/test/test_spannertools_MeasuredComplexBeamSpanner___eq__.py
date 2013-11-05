# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_MeasuredComplexBeamSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.MeasuredComplexBeamSpanner()
    spanner_2 = spannertools.MeasuredComplexBeamSpanner()

    assert not spanner_1 == spanner_2
