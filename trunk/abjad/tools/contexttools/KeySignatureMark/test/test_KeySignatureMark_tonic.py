from abjad import *


def test_KeySignatureMark_tonic_01():
    '''Key signature tonic is read / write.
    '''

    key_signature = contexttools.KeySignatureMark('e', 'major')
    key_signature.tonic = pitchtools.NamedChromaticPitchClass('e')

    key_signature.tonic = 'd'
    key_signature.tonic = pitchtools.NamedChromaticPitchClass('d')
