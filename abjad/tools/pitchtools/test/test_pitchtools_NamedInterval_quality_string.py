# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInterval_quality_string_01():

    assert pitchtools.NamedInterval('perfect', 1).quality_string == \
        'perfect'
    assert pitchtools.NamedInterval('minor', 2).quality_string == \
        'minor'
    assert pitchtools.NamedInterval('major', 2).quality_string == \
        'major'
    assert pitchtools.NamedInterval('minor', 3).quality_string == \
        'minor'
    assert pitchtools.NamedInterval('major', 3).quality_string == \
        'major'
    assert pitchtools.NamedInterval('perfect', 4).quality_string == \
        'perfect'
    assert pitchtools.NamedInterval('augmented', 4).quality_string == \
        'augmented'
    assert pitchtools.NamedInterval('diminished', 5).quality_string ==\
        'diminished'
    assert pitchtools.NamedInterval('perfect', 5).quality_string == \
        'perfect'
