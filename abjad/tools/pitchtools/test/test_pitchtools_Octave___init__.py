# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave___init___01():
    r'''Initializes octave from empty input.
    '''

    octave = pitchtools.Octave()

    assert octave == pitchtools.Octave(4)
