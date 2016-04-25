# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_Octave___str___01():


    assert str(pitchtools.Octave(-1)) == ',,,,'
    assert str(pitchtools.Octave(0)) == ',,,'
    assert str(pitchtools.Octave(1)) == ',,'
    assert str(pitchtools.Octave(2)) == ','
    assert str(pitchtools.Octave(3)) == ''
    assert str(pitchtools.Octave(4)) == "'"
    assert str(pitchtools.Octave(5)) == "''"
    assert str(pitchtools.Octave(6)) == "'''"
    assert str(pitchtools.Octave(7)) == "''''"
