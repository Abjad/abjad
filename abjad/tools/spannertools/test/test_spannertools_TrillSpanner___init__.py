# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_TrillSpanner___init___01():
    r'''Initializeempty trill spanner.
    '''

    trill = spannertools.TrillSpanner()
    assert isinstance(trill, spannertools.TrillSpanner)
