# -*- encoding: utf-8 -*-
from abjad import *


def test_PianoPedalSpanner___init___01():
    r'''Init empty piano pedal spanner.
    '''

    pedal = spannertools.PianoPedalSpanner()
    assert isinstance(pedal, spannertools.PianoPedalSpanner)
