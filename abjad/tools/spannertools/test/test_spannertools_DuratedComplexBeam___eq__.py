# -*- coding: utf-8 -*-
import abjad


def test_spannertools_DuratedComplexBeam___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = abjad.DuratedComplexBeam()
    spanner_2 = abjad.DuratedComplexBeam()

    assert not spanner_1 == spanner_2
