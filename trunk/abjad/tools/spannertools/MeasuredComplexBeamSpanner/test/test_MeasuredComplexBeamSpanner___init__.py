from abjad import *


def test_MeasuredComplexBeamSpanner___init___01():
    '''Init empty measured complex beam spanner.
    '''

    beam = spannertools.MeasuredComplexBeamSpanner()
    assert isinstance(beam, spannertools.MeasuredComplexBeamSpanner)
