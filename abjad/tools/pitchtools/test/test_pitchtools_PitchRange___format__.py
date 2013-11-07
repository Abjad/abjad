# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___format___01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert format(pitch_range) == "pitchtools.PitchRange(\n\t'[A0, C8]'\n\t)"
