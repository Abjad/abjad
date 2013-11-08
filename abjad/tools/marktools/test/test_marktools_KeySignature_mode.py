# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import tonalanalysistools


def test_marktools_KeySignature_mode_01():
    r'''Key signature mode is read / write.
    '''

    key_signature = marktools.KeySignature('e', 'major')
    assert key_signature.mode == tonalanalysistools.Mode('major')

    key_signature.mode = 'minor'
    assert key_signature.mode == tonalanalysistools.Mode('minor')
