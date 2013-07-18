from abjad import *
from abjad.tools import tonalanalysistools


def test_KeySignatureMark_mode_01():
    '''Key signature mode is read / write.
    '''

    key_signature = contexttools.KeySignatureMark('e', 'major')
    assert key_signature.mode == tonalanalysistools.Mode('major')

    key_signature.mode = 'minor'
    assert key_signature.mode == tonalanalysistools.Mode('minor')
