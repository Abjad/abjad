# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_StaffLinesSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.StaffLinesSpanner()
    spanner_2 = spannertools.StaffLinesSpanner()

    assert not spanner_1 == spanner_2
