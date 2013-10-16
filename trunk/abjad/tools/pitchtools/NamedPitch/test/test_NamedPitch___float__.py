# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch___float___01():
    r'''Return pitch number of 12-ET named pitch as float.
    '''

    named_pitch = pitchtools.NamedPitch(13)
    assert isinstance(float(named_pitch), float)
    assert float(named_pitch) == 13.0


def test_NamedPitch___float___02():
    r'''Return pitch number of 24-ET named pitch as float.
    '''

    named_pitch = pitchtools.NamedPitch(13.5)
    assert isinstance(float(named_pitch), float)
    assert float(named_pitch) == 13.5
