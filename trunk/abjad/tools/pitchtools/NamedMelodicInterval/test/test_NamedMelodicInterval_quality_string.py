# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedMelodicInterval_quality_string_01():

    assert pitchtools.NamedMelodicInterval('perfect', 1).quality_string == \
        'perfect'
    assert pitchtools.NamedMelodicInterval('minor', 2).quality_string == \
        'minor'
    assert pitchtools.NamedMelodicInterval('major', 2).quality_string == \
        'major'
    assert pitchtools.NamedMelodicInterval('minor', 3).quality_string == \
        'minor'
    assert pitchtools.NamedMelodicInterval('major', 3).quality_string == \
        'major'
    assert pitchtools.NamedMelodicInterval('perfect', 4).quality_string == \
        'perfect'
    assert pitchtools.NamedMelodicInterval('augmented', 4).quality_string == \
        'augmented'
    assert pitchtools.NamedMelodicInterval('diminished', 5).quality_string ==\
        'diminished'
    assert pitchtools.NamedMelodicInterval('perfect', 5).quality_string == \
        'perfect'
