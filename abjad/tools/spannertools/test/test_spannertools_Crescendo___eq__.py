# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Crescendo___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = Crescendo()
    spanner_2 = Crescendo()

    assert not spanner_1 == spanner_2
