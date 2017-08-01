# -*- coding: utf-8 -*-
import abjad


def test_spannertools_Spanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    class MockSpanner(abjad.Spanner):

        def __init__(self, components=None):
            abjad.Spanner.__init__(self, components)

    spanner_1 = MockSpanner()
    spanner_2 = MockSpanner()

    assert not spanner_1 == spanner_2
