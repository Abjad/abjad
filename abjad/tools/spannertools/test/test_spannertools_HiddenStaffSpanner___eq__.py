# -*- coding: utf-8 -*-
import abjad


def test_spannertools_HiddenStaffSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.HiddenStaffSpanner()
    spanner_2 = abjad.HiddenStaffSpanner()

    assert not spanner_1 == spanner_2
