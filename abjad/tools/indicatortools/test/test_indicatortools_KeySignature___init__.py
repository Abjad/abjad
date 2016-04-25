# -*- coding: utf-8 -*-
from abjad import *


def test_indicatortools_KeySignature___init___01():
    r'''Initializes with pitch-class letter string and mode string.
    '''

    key_signature = KeySignature('g', 'major')

    assert key_signature.tonic == pitchtools.NamedPitchClass('g')
    assert key_signature.mode == tonalanalysistools.Mode('major')
