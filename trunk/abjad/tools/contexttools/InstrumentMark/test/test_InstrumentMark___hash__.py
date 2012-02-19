from abjad import *
from abjad.tools.contexttools import InstrumentMark


def test_InstrumentMark___hash___01():
    '''If two marks compare equally, their hashes also compare equally.'''
    one = InstrumentMark('Guitar', 'gtr.')
    two = InstrumentMark('Guitar', 'gtr.')
    three = InstrumentMark('Flute', 'fl.')
    assert one == two
    assert hash(one) == hash(two)
    assert one != three
    assert hash(one) != hash(three)
