# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_TrillSpanner___init___01():
    r'''Initialize empty trill spanner.
    '''

    trill = spannertools.TrillSpanner()
    assert isinstance(trill, spannertools.TrillSpanner)
