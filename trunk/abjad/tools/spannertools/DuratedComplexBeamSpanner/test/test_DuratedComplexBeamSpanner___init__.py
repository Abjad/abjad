from abjad import *


def test_DuratedComplexBeamSpanner___init___01():
    '''Init empty durated complex beam spanner.
    '''

    beam = spannertools.DuratedComplexBeamSpanner()
    assert isinstance(beam, spannertools.DuratedComplexBeamSpanner)
