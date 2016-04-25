# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Glissando___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.Glissando()
    spanner_2 = spannertools.Glissando()

    assert not spanner_1 == spanner_2
