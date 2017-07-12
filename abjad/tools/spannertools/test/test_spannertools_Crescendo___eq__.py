# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Crescendo___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Crescendo()
    spanner_2 = abjad.Crescendo()

    assert not spanner_1 == spanner_2
