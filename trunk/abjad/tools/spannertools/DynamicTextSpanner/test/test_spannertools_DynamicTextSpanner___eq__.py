# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_DynamicTextSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.DynamicTextSpanner()
    spanner_2 = spannertools.DynamicTextSpanner()

    assert not spanner_1 == spanner_2
