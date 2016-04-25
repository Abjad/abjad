# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitch___add___01():

    pitch = NamedPitch(12)
    named_interval = pitchtools.NamedInterval('minor', 2)

    assert pitch + named_interval == NamedPitch('df', 5)


def test_pitchtools_NamedPitch___add___02():

    pitch = NamedPitch(12)
    numbered_interval = pitchtools.NumberedInterval(1)

    assert pitch + numbered_interval == NamedPitch('df', 5)
