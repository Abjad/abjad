# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___format___01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert systemtools.TestManager.compare(
        format(pitch_range),
        r'''
        pitchtools.PitchRange(
            '[A0, C8]'
            )
        ''',
        )
