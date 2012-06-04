from abjad import *


def test_MeasuredComplexBeamSpanner___init___01():
    '''Init empty measured complex beam spanner.
    '''

    beam = beamtools.MeasuredComplexBeamSpanner()
    assert isinstance(beam, beamtools.MeasuredComplexBeamSpanner)
