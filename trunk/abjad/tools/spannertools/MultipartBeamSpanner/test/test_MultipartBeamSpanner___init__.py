from abjad import *


def test_MultipartBeamSpanner___init___01():
    '''Init empty multipart beam spanner.
    '''

    beam = spannertools.MultipartBeamSpanner()
    assert isinstance(beam, spannertools.MultipartBeamSpanner)
