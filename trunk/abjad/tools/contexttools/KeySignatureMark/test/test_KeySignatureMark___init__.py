from abjad import *
from abjad.tools import tonalanalysistools


def test_KeySignatureMark___init___01():
    r'''Initialize with pitch-class letter string and mode string.
    '''

    ks = contexttools.KeySignatureMark('g', 'major')

    assert ks.tonic == pitchtools.NamedChromaticPitchClass('g')
    assert ks.mode == tonalanalysistools.Mode('major')
