# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRangeInventory___format___01():

    inventory = pitchtools.PitchRangeInventory(['[A0, C8]', '[C4, D5]'])

    assert format(inventory) == stringtools.normalize(
        r'''
        pitchtools.PitchRangeInventory(
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
