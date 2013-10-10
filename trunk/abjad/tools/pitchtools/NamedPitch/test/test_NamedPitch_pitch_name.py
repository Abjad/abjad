# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_name_01():

    assert pitchtools.NamedPitch("c'").pitch_name == "c'"
    assert pitchtools.NamedPitch("c''").pitch_name == "c''"
    assert pitchtools.NamedPitch("c,").pitch_name == "c,"
    assert pitchtools.NamedPitch("d'").pitch_name == "d'"
    assert pitchtools.NamedPitch("d''").pitch_name == "d''"
    assert pitchtools.NamedPitch("d,").pitch_name == "d,"
