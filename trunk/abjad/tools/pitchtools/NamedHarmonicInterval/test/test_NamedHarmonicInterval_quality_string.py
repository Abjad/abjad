# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedHarmonicInterval_quality_string_01():

    assert pitchtools.NamedHarmonicInterval('perfect', 1).quality_string == 'perfect'
    assert pitchtools.NamedHarmonicInterval('minor', 2).quality_string == 'minor'
    assert pitchtools.NamedHarmonicInterval('major', 2).quality_string == 'major'
    assert pitchtools.NamedHarmonicInterval('minor', 3).quality_string == 'minor'
    assert pitchtools.NamedHarmonicInterval('major', 3).quality_string == 'major'
    assert pitchtools.NamedHarmonicInterval('perfect', 4).quality_string == 'perfect'
    assert pitchtools.NamedHarmonicInterval('augmented', 4).quality_string == \
        'augmented'
    assert pitchtools.NamedHarmonicInterval('diminished', 5).quality_string == \
        'diminished'
    assert pitchtools.NamedHarmonicInterval('perfect', 5).quality_string == 'perfect'
