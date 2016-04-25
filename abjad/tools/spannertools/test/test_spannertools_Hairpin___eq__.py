# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Hairpin___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = Hairpin()
    spanner_2 = Hairpin()

    assert not spanner_1 == spanner_2
