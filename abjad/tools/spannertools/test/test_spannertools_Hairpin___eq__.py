# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Hairpin___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.Hairpin()
    spanner_2 = abjad.Hairpin()

    assert not spanner_1 == spanner_2
