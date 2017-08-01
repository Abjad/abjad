# -*- coding: utf-8 -*-
import abjad


def test_spannertools_TrillSpanner___init___01():
    r'''Initialize empty trill spanner.
    '''

    trill = abjad.TrillSpanner()
    assert isinstance(trill, abjad.TrillSpanner)
