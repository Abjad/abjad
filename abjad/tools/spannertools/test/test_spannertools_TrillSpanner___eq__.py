# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_TrillSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.TrillSpanner()
    spanner_2 = spannertools.TrillSpanner()

    assert not spanner_1 == spanner_2
