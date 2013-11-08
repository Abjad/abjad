# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DecrescendoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = DecrescendoSpanner()
    spanner_2 = DecrescendoSpanner()

    assert not spanner_1 == spanner_2
