# -*- encoding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature_mode_01():
    r'''Key signature mode is read / write.
    '''

    key_signature = KeySignature('e', 'major')
    assert key_signature.mode == tonalanalysistools.Mode('major')

    key_signature.mode = 'minor'
    assert key_signature.mode == tonalanalysistools.Mode('minor')
