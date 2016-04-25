# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_Spanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    class MockSpanner(spannertools.Spanner):

        def __init__(self, components=None):
            spannertools.Spanner.__init__(self, components)

    spanner_1 = MockSpanner()
    spanner_2 = MockSpanner()

    assert not spanner_1 == spanner_2
