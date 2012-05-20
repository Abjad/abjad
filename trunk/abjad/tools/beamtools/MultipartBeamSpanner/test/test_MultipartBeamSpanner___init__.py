from abjad import *


def test_MultipartBeamSpanner___init___01():
    '''Init empty multipart beam spanner.
    '''

    beam = beamtools.MultipartBeamSpanner()
    assert isinstance(beam, beamtools.MultipartBeamSpanner)
