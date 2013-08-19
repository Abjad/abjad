# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitch___float___01():
    r'''Return chromatic pitch number of 12-ET named chromatic pitch as float.
    '''

    named_chromatic_pitch = pitchtools.NamedPitch(13)
    assert isinstance(float(named_chromatic_pitch), float)
    assert float(named_chromatic_pitch) == 13.0


def test_NamedPitch___float___02():
    r'''Return chromatic pitch number of 24-ET named chromatic pitch as float.
    '''

    named_chromatic_pitch = pitchtools.NamedPitch(13.5)
    assert isinstance(float(named_chromatic_pitch), float)
    assert float(named_chromatic_pitch) == 13.5
