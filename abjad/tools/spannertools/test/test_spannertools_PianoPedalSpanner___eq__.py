# -*- coding: utf-8 -*-
import abjad


def test_spannertools_PianoPedalSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.PianoPedalSpanner()
    spanner_2 = abjad.PianoPedalSpanner()

    assert not spanner_1 == spanner_2
