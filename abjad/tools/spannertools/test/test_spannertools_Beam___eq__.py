# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Beam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Beam()
    spanner_2 = abjad.Beam()

    assert not spanner_1 == spanner_2
