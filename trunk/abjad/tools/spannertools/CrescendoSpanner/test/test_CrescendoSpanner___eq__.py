# -*- encoding: utf-8 -*-
from abjad import *


def test_CrescendoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.CrescendoSpanner()
    spanner_2 = spannertools.CrescendoSpanner()

    assert not spanner_1 == spanner_2
