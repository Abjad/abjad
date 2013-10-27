# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch___abs___01():

    assert abs(pitchtools.NamedPitch(11)) == 11
    assert abs(pitchtools.NamedPitch(11.5)) == 11.5
    assert abs(pitchtools.NamedPitch(13)) == 13
    assert abs(pitchtools.NamedPitch(13.5)) == 13.5
