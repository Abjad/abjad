# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexBeamSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.ComplexBeamSpanner()
    spanner_2 = spannertools.ComplexBeamSpanner()

    assert not spanner_1 == spanner_2
