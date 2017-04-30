# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRangeList___format___01():

    ranges = pitchtools.PitchRangeList(['[A0, C8]', '[C4, D5]'])

    assert format(ranges) == stringtools.normalize(
        r'''
        pitchtools.PitchRangeList(
            [
                pitchtools.PitchRange(
                    range_string='[A0, C8]',
                    ),
                pitchtools.PitchRange(
                    range_string='[C4, D5]',
                    ),
                ]
            )
        ''',
        )
