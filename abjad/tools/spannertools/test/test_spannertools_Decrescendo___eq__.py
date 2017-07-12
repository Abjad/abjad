# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Decrescendo___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Decrescendo()
    spanner_2 = abjad.Decrescendo()

    assert not spanner_1 == spanner_2
