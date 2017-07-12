# -*- coding: utf-8 -*-
import abjad


def test_spannertools_PianoPedalSpanner___init___01():
    r'''Initialize empty piano pedal spanner.
    '''

    pedal = abjad.PianoPedalSpanner()
    assert isinstance(pedal, abjad.PianoPedalSpanner)
