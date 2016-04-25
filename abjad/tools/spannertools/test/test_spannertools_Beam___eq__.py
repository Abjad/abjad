# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Beam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = Beam()
    spanner_2 = Beam()

    assert not spanner_1 == spanner_2
