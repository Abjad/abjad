# -*- encoding: utf-8 -*-
from abjad import *


def test_CrescendoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = CrescendoSpanner()
    spanner_2 = CrescendoSpanner()

    assert not spanner_1 == spanner_2
