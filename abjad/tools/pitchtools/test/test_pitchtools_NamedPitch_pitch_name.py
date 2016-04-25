# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch_pitch_name_01():

    assert NamedPitch("c'").pitch_name == "c'"
    assert NamedPitch("c''").pitch_name == "c''"
    assert NamedPitch("c,").pitch_name == "c,"
    assert NamedPitch("d'").pitch_name == "d'"
    assert NamedPitch("d''").pitch_name == "d''"
    assert NamedPitch("d,").pitch_name == "d,"


def test_pitchtools_NamedPitch_pitch_name_02():

    assert NamedPitch('C#+2').pitch_name == 'ctqs,'
    assert NamedPitch('A4').pitch_name == "a'"
    assert NamedPitch('Dbb6').pitch_name == "dff'''"
    assert NamedPitch('C-1').pitch_name == 'c,,,,'
