# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedDiatonicPitch___init___01():

    assert isinstance(pitchtools.NamedDiatonicPitch("c''"), pitchtools.NamedDiatonicPitch)
