# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_PhrasingSlur___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.PhrasingSlur()
    spanner_2 = spannertools.PhrasingSlur()

    assert not spanner_1 == spanner_2
