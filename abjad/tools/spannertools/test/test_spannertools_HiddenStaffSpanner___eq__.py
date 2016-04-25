# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_HiddenStaffSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.HiddenStaffSpanner()
    spanner_2 = spannertools.HiddenStaffSpanner()

    assert not spanner_1 == spanner_2
