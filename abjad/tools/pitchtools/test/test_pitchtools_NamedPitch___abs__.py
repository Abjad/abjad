# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch___abs___01():

    assert abs(NamedPitch(11)) == 11
    assert abs(NamedPitch(11.5)) == 11.5
    assert abs(NamedPitch(13)) == 13
    assert abs(NamedPitch(13.5)) == 13.5
