# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_KeySignature_tonic_01():
    r'''Key signature tonic is read / write.
    '''

    key_signature = marktools.KeySignature('e', 'major')
    key_signature.tonic = pitchtools.NamedPitchClass('e')

    key_signature.tonic = 'd'
    key_signature.tonic = pitchtools.NamedPitchClass('d')
