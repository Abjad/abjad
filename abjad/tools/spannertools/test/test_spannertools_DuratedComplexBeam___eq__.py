# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_DuratedComplexBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.DuratedComplexBeam()
    spanner_2 = spannertools.DuratedComplexBeam()

    assert not spanner_1 == spanner_2
