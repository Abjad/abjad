# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_TextScriptSpanner___eq___01():
    r'''Spanner is strict comparator.
    '''

    spanner_1 = spannertools.TextScriptSpanner()
    spanner_2 = spannertools.TextScriptSpanner()

    assert not spanner_1 == spanner_2
