from abjad import *


def test_DuratedComplexBeamSpanner___init___01():
    '''Init empty durated complex beam spanner.
    '''

    beam = beamtools.DuratedComplexBeamSpanner()
    assert isinstance(beam, beamtools.DuratedComplexBeamSpanner)
