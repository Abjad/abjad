# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_name_01():

    assert pitchtools.NamedPitch("c'").pitch_name == "c'"
    assert pitchtools.NamedPitch("c''").pitch_name == "c''"
    assert pitchtools.NamedPitch("c,").pitch_name == "c,"
    assert pitchtools.NamedPitch("d'").pitch_name == "d'"
    assert pitchtools.NamedPitch("d''").pitch_name == "d''"
    assert pitchtools.NamedPitch("d,").pitch_name == "d,"


def test_NamedPitch_pitch_name_02():

    assert pitchtools.NamedPitch('C#+2').pitch_name == 'ctqs,'
    assert pitchtools.NamedPitch('A4').pitch_name == "a'"
    assert pitchtools.NamedPitch('Dbb6').pitch_name == "dff'''"
    assert pitchtools.NamedPitch('C-1').pitch_name == 'c,,,,'
