# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_GlissandoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.GlissandoSpanner()
    spanner_2 = spannertools.GlissandoSpanner()

    assert not spanner_1 == spanner_2
