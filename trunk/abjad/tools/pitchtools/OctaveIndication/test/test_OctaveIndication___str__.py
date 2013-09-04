# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveIndication___str___01():


    assert str(pitchtools.OctaveIndication(-1)) == ',,,,'
    assert str(pitchtools.OctaveIndication(0)) == ',,,'
    assert str(pitchtools.OctaveIndication(1)) == ',,'
    assert str(pitchtools.OctaveIndication(2)) == ','
    assert str(pitchtools.OctaveIndication(3)) == ''
    assert str(pitchtools.OctaveIndication(4)) == "'"
    assert str(pitchtools.OctaveIndication(5)) == "''"
    assert str(pitchtools.OctaveIndication(6)) == "'''"
    assert str(pitchtools.OctaveIndication(7)) == "''''"
