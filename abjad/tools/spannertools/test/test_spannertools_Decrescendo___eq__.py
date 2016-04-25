# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Decrescendo___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = Decrescendo()
    spanner_2 = Decrescendo()

    assert not spanner_1 == spanner_2
