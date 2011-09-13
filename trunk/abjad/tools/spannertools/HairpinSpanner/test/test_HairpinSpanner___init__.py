from abjad import *


def test_HairpinSpanner___init___01():
    '''Init empty hairpin spanner.
    '''

    hairpin = spannertools.HairpinSpanner()
    assert isinstance(hairpin, spannertools.HairpinSpanner)
