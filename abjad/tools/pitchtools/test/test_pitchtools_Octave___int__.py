# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave___int___01():

    assert int(pitchtools.Octave('')) == 3
    assert int(pitchtools.Octave(',')) == 2
    assert int(pitchtools.Octave(',,')) == 1
    assert int(pitchtools.Octave(',,,')) == 0
    assert int(pitchtools.Octave("'")) == 4
    assert int(pitchtools.Octave("''")) == 5
    assert int(pitchtools.Octave("'''")) == 6
