# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_HairpinSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = HairpinSpanner()
    spanner_2 = HairpinSpanner()

    assert not spanner_1 == spanner_2
