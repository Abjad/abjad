# -*- encoding: utf-8 -*-
from abjad import *


def test_DuratedComplexBeamSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.DuratedComplexBeamSpanner()
    spanner_2 = spannertools.DuratedComplexBeamSpanner()

    assert not spanner_1 == spanner_2
