# -*- coding: utf-8 -*-
import abjad


def test_spannertools_OctavationSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.OctavationSpanner()
    spanner_2 = abjad.OctavationSpanner()

    assert not spanner_1 == spanner_2
