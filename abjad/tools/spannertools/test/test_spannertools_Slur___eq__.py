# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Slur___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = Slur()
    spanner_2 = Slur()

    assert not spanner_1 == spanner_2
