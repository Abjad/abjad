# -*- encoding: utf-8 -*-
from abjad import *


def test_ComplexGlissandoSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.ComplexGlissandoSpanner()
    spanner_2 = spannertools.ComplexGlissandoSpanner()

    assert not spanner_1 == spanner_2
