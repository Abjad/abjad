# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_OctavationSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.OctavationSpanner()
    spanner_2 = spannertools.OctavationSpanner()

    assert not spanner_1 == spanner_2
