# -*- encoding: utf-8 -*-
from abjad import *


def test_OctaveIndication_from_pitch_name_01():

    assert pitchtools.OctaveIndication.from_pitch_name("cs'") == 4
    assert pitchtools.OctaveIndication.from_pitch_name('cs') == 3
    assert pitchtools.OctaveIndication.from_pitch_name('cs,') == 2
