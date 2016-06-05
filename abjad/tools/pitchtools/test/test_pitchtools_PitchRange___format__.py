# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange___format___01():

    pitch_range = pitchtools.PitchRange('[A0, C8]')

    assert format(pitch_range) == stringtools.normalize(
        r'''
        pitchtools.PitchRange(
            range_string='[A0, C8]',
            )
        ''',
        )
