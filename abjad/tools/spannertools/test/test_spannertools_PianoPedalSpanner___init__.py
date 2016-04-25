# -*- coding: utf-8 -*-
from abjad import *


def test_spannertools_PianoPedalSpanner___init___01():
    r'''Initialize empty piano pedal spanner.
    '''

    pedal = spannertools.PianoPedalSpanner()
    assert isinstance(pedal, spannertools.PianoPedalSpanner)
