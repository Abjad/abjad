from abjad import *


def test_PianoPedalSpanner___init___01():
    '''Init empty piano pedal spanner.
    '''

    pedal = spannertools.PianoPedalSpanner()
    assert isinstance(pedal, spannertools.PianoPedalSpanner)
