# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_TextSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.TextSpanner()
    spanner_2 = spannertools.TextSpanner()

    assert not spanner_1 == spanner_2
