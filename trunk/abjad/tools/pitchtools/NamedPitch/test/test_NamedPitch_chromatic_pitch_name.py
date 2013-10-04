# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch_pitch_name_01():

    assert pitchtools.NamedPitch("cs''").pitch_name == "cs''"
