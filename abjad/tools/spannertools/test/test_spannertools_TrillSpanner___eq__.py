# -*- coding: utf-8 -*-
import abjad


def test_spannertools_TrillSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.TrillSpanner()
    spanner_2 = abjad.TrillSpanner()

    assert not spanner_1 == spanner_2
